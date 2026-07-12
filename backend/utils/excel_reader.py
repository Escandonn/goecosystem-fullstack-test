"""Utilitario para leer archivos Excel con pacientes."""

from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
from pathlib import Path


class ExcelReaderError(Exception):
    """Excepción personalizada para errores del lector Excel."""
    pass


class ExcelReader:
    """Lee archivos Excel y los convierte a lista de diccionarios."""

    # Columnas esperadas en el Excel
    REQUIRED_COLUMNS = [
        "TipoDocumento",
        "NumeroDocumento",
        "Nombres",
        "Apellidos",
        "FechaNacimiento",
        "Sexo",
    ]

    OPTIONAL_COLUMNS = [
        "Telefono",
        "Correo",
        "Direccion",
        "Estado",
    ]

    ALL_COLUMNS = REQUIRED_COLUMNS + OPTIONAL_COLUMNS

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._validate_file()

    def _validate_file(self) -> None:
        """Valida que el archivo exista y tenga extensión correcta."""
        if not self.file_path.exists():
            raise ExcelReaderError(f"El archivo no existe: {self.file_path}")

        if self.file_path.suffix.lower() != ".xlsx":
            raise ExcelReaderError(
                f"Formato de archivo no válido. Solo se acepta .xlsx, recibido: {self.file_path.suffix}"
            )

    def read(self) -> List[Dict[str, Any]]:
        """
        Lee el archivo Excel y retorna una lista de diccionarios.
        
        Returns:
            Lista de diccionarios con los datos de pacientes.
            
        Raises:
            ExcelReaderError: Si hay errores al leer el archivo.
        """
        try:
            # Leer el archivo Excel
            df = pd.read_excel(self.file_path, engine='openpyxl')
            
            # Verificar que no esté vacío
            if df.empty:
                raise ExcelReaderError("El archivo está vacío")
            
            # Normalizar nombres de columnas (quitar espacios, mayúsculas)
            df.columns = df.columns.str.strip()
            
            # Verificar columnas requeridas
            self._validate_columns(df.columns.tolist())
            
            # Convertir a lista de diccionarios
            records = df.to_dict(orient='records')
            
            # Normalizar datos
            return self._normalize_records(records)
            
        except pd.errors.ExcelFileError as e:
            raise ExcelReaderError(f"Error al leer el archivo Excel: {str(e)}")
        except Exception as e:
            raise ExcelReaderError(f"Error al procesar el archivo: {str(e)}")

    def _validate_columns(self, columns: List[str]) -> None:
        """Valida que estén presentes las columnas requeridas."""
        # Normalizar columnas del Excel
        normalized_columns = {col.strip().lower(): col for col in columns}
        
        missing_columns = []
        for required in self.REQUIRED_COLUMNS:
            if required.lower() not in normalized_columns:
                missing_columns.append(required)
        
        if missing_columns:
            raise ExcelReaderError(
                f"Columnas faltantes en el Excel: {', '.join(missing_columns)}"
            )

    def _normalize_records(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normaliza los registros para que coincidan con el schema."""
        normalized = []
        
        for i, record in enumerate(records, start=2):  # start=2 porque la fila 1 es encabezado
            try:
                normalized_record = self._normalize_record(record, i)
                normalized.append(normalized_record)
            except Exception as e:
                # Si hay error en una fila, la agregamos con el error
                normalized_record = {
                    "_row": i,
                    "_error": str(e),
                    **record
                }
                normalized.append(normalized_record)
        
        return normalized

    def _normalize_record(self, record: Dict[str, Any], row_num: int) -> Dict[str, Any]:
        """Normaliza un registro individual."""
        # Crear mapping de columnas normalizadas
        columns_map = {col.strip().lower(): col for col in record.keys()}
        
        def get_value(std_name: str, default=None):
            """Obtiene el valor de una columna por su nombre estándar."""
            normalized = std_name.lower()
            if normalized in columns_map:
                return record.get(columns_map[normalized])
            return default
        
        # Extraer y normalizar valores
        tipo_doc = get_value("TipoDocumento", "").strip().upper() if get_value("TipoDocumento") else None
        numero_doc = str(get_value("NumeroDocumento", "")).strip()
        nombres = get_value("Nombres", "").strip().upper() if get_value("Nombres") else None
        apellidos = get_value("Apellidos", "").strip().upper() if get_value("Apellidos") else None
        fecha_nac = get_value("FechaNacimiento")
        sexo = get_value("Sexo", "").strip().upper() if get_value("Sexo") else None
        telefono = str(get_value("Telefono", "")).strip() if get_value("Telefono") else None
        correo = get_value("Correo", "").strip().lower() if get_value("Correo") else None
        direccion = get_value("Direccion", "").strip() if get_value("Direccion") else None
        estado = get_value("Estado", True)
        
        # Normalizar estado
        if isinstance(estado, str):
            estado = estado.lower() in ('true', '1', 'si', 'sí', 'activo')
        
        # Normalizar fecha
        if isinstance(fecha_nac, str):
            try:
                fecha_nac = pd.to_datetime(fecha_nac).date()
            except:
                fecha_nac = None
        elif isinstance(fecha_nac, datetime):
            fecha_nac = fecha_nac.date()
        
        return {
            "tipo_documento": tipo_doc,
            "numero_documento": numero_doc,
            "nombres": nombres,
            "apellidos": apellidos,
            "fecha_nacimiento": fecha_nac,
            "sexo": sexo,
            "telefono": telefono if telefono else None,
            "correo": correo if correo else None,
            "direccion": direccion if direccion else None,
            "estado": estado,
            "_row": row_num,
        }

    @staticmethod
    def get_template_columns() -> List[str]:
        """Retorna las columnas del template de Excel."""
        return ExcelReader.ALL_COLUMNS