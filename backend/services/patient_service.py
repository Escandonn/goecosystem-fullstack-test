"""Servicio de lógica de negocio para la entidad Paciente."""

from typing import Optional, List, Dict, Any
import shutil
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from core.config import settings
from core.exceptions import NotFoundError, ConflictError, BadRequestError
from core.logging import get_logger
from models.patient import Patient
from repositories.patient_repository import PatientRepository
from schemas.patient import PatientCreate, PatientUpdate
from schemas.import_result import ImportResult, ImportError
from utils.excel_reader import ExcelReader, ExcelReaderError


logger = get_logger("patient_service")


class PatientService:
    """Contiene la lógica de negocio de pacientes."""

    def __init__(self, db: Session):
        self.repository = PatientRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Patient]:
        """Obtiene todos los pacientes."""
        patients = self.repository.get_all(skip=skip, limit=limit)
        logger.debug("get_all | skip=%d limit=%d | %d pacientes", skip, limit, len(patients))
        return patients

    def get_by_id(self, patient_id: int) -> Patient:
        """Obtiene un paciente por ID o lanza 404."""
        patient = self.repository.get_by_id(patient_id)
        if not patient:
            logger.warning("Paciente no encontrado | id=%d", patient_id)
            raise NotFoundError(f"Paciente con ID {patient_id} no encontrado")
        return patient

    def search(self, query: str, skip: int = 0, limit: int = 100) -> list[Patient]:
        """Busca pacientes por nombre, apellido o documento."""
        results = self.repository.search(query, skip=skip, limit=limit)
        logger.debug("search | q='%s' | %d resultados", query, len(results))
        return results

    def count(self) -> int:
        """Cuenta el total de pacientes."""
        total = self.repository.count()
        logger.debug("count | total=%d", total)
        return total

    def create(self, patient_data: PatientCreate) -> Patient:
        """Crea un paciente validando duplicados."""
        existing = self.repository.get_by_documento(patient_data.numero_documento)
        if existing:
            logger.warning("Intento de crear paciente duplicado | doc=%s", patient_data.numero_documento)
            raise ConflictError(
                f"Ya existe un paciente con el documento '{patient_data.numero_documento}'"
            )
        patient = Patient(**patient_data.model_dump())
        result = self.repository.create(patient)
        logger.info("Paciente creado | id=%d doc=%s", result.id, patient_data.numero_documento)
        return result

    def update(self, patient_id: int, patient_data: PatientUpdate) -> Patient:
        """Actualiza un paciente existente."""
        patient = self.get_by_id(patient_id)

        # Si se actualiza el documento, verificar que no exista en otro paciente
        if patient_data.numero_documento and patient_data.numero_documento != patient.numero_documento:
            existing = self.repository.get_by_documento(patient_data.numero_documento)
            if existing and existing.id != patient_id:
                logger.warning("Conflicto al actualizar | id=%d doc=%s ya existe", patient_id, patient_data.numero_documento)
                raise ConflictError(
                    f"Ya existe un paciente con el documento '{patient_data.numero_documento}'"
                )

        update_data = patient_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(patient, field, value)

        result = self.repository.update(patient)
        logger.info("Paciente actualizado | id=%d campos=%s", patient_id, list(update_data.keys()))
        return result

    def delete(self, patient_id: int) -> None:
        """Elimina un paciente."""
        patient = self.get_by_id(patient_id)
        self.repository.delete(patient)
        logger.info("Paciente eliminado | id=%d", patient_id)

    def import_from_excel(self, file: UploadFile, save_file: bool = True) -> ImportResult:
        """
        Importa pacientes desde un archivo Excel.

        Args:
            file: Archivo Excel subido por el usuario
            save_file: Si True, guarda el archivo en uploads/

        Returns:
            ImportResult con el resumen de la importación
        """
        logger.info("Iniciando importación | archivo=%s", file.filename)

        # Guardar archivo temporalmente
        upload_dir = settings.upload_path
        upload_dir.mkdir(parents=True, exist_ok=True)

        temp_path = upload_dir / f"temp_{file.filename}"

        try:
            # Guardar el archivo
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Leer y procesar el Excel
            reader = ExcelReader(str(temp_path))
            records = reader.read()

            # Validar registros
            valid_records = []
            validation_errors = []

            for record in records:
                row_num = record.pop("_row", None)
                error = record.pop("_error", None)

                if error:
                    validation_errors.append(ImportError(
                        row=row_num,
                        error=error
                    ))
                    continue

                # Validaciones básicas
                if not record.get("numero_documento"):
                    validation_errors.append(ImportError(
                        row=row_num,
                        column="NumeroDocumento",
                        error="Número de documento es requerido"
                    ))
                    continue

                if not record.get("nombres"):
                    validation_errors.append(ImportError(
                        row=row_num,
                        column="Nombres",
                        error="Nombres es requerido"
                    ))
                    continue

                valid_records.append(record)

            # Insertar en batch
            if valid_records:
                inserted, duplicates, errors, ids, db_errors = self.repository.create_batch(valid_records)

                # Agregar errores de BD
                for db_error in db_errors:
                    validation_errors.append(ImportError(
                        row=db_error.get("row", 0),
                        error=db_error.get("error", "Error desconocido")
                    ))
            else:
                inserted = duplicates = errors = 0
                ids = []

            # Calcular totales
            total = len(records)
            error_count = len(validation_errors)

            # Generar mensaje
            if inserted > 0 and error_count == 0:
                mensaje = f"Importación exitosa. {inserted} paciente(s) importado(s)."
            elif inserted > 0 and error_count > 0:
                mensaje = f"Importación parcial. {inserted} paciente(s) importado(s), {duplicates} duplicado(s), {error_count} error(es)."
            elif duplicates > 0 and inserted == 0:
                mensaje = f"No se importaron pacientes. {duplicates} documento(s) ya existen."
            else:
                mensaje = f"Importación fallida. {error_count} error(es) encontrado(s)."

            logger.info(
                "Importación completada | archivo=%s | total=%d | insertados=%d | duplicados=%d | errores=%d",
                file.filename, total, inserted, duplicates, error_count
            )

            return ImportResult(
                archivo=file.filename,
                total_registros=total,
                insertados=inserted,
                duplicados=duplicates,
                errores=error_count,
                detalles_errores=validation_errors,
                ids_insertados=ids,
                mensaje=mensaje
            )

        except ExcelReaderError as e:
            logger.error("Error al leer Excel | archivo=%s | error=%s", file.filename, str(e))
            raise BadRequestError(f"Error al leer el archivo: {str(e)}")
        except Exception as e:
            logger.error("Error interno en importación | archivo=%s | error=%s", file.filename, str(e))
            raise
        finally:
            # Limpiar archivo temporal
            if temp_path.exists():
                temp_path.unlink()
