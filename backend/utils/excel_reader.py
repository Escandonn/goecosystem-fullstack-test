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
        "Documento",
        "NombreCompleto",
        "FechaNacimiento",
        "Genero",
        "Telefono",
        "EpsCodigo",
        "EpsNombre",
        "Prioridad",
        "Estado",
    ]

    OPTIONAL_COLUMNS = [
        "Correo",
        "Ciudad",
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
                val = record.get(columns_map[normalized])
                if pd.isna(val):
                    return default
                return val
            return default
        
        # Extraer y normalizar valores
        tipo_doc = get_value("TipoDocumento", "").strip().upper() if get_value("TipoDocumento") else None
        documento = str(get_value("Documento", "")).strip() if get_value("Documento") else None
        if documento and documento.endswith(".0"):
            documento = documento[:-2]
            
        nombre_completo = get_value("NombreCompleto", "").strip() if get_value("NombreCompleto") else None
        fecha_nac = get_value("FechaNacimiento")
        genero = get_value("Genero", "").strip() if get_value("Genero") else None
        
        telefono = str(get_value("Telefono", "")).strip() if get_value("Telefono") else None
        if telefono and telefono.endswith(".0"):
            telefono = telefono[:-2]
            
        correo = get_value("Correo", "").strip().lower() if get_value("Correo") else None
        
        eps_codigo = str(get_value("EpsCodigo", "")).strip() if get_value("EpsCodigo") else None
        if eps_codigo and eps_codigo.endswith(".0"):
            eps_codigo = eps_codigo[:-2]
            
        eps_nombre = get_value("EpsNombre", "").strip() if get_value("EpsNombre") else None
        ciudad = get_value("Ciudad", "").strip() if get_value("Ciudad") else None
        prioridad = get_value("Prioridad", "").strip() if get_value("Prioridad") else None
        estado = get_value("Estado", "").strip() if get_value("Estado") else None
        
        # Normalizar fecha
        if isinstance(fecha_nac, str):
            try:
                fecha_nac = pd.to_datetime(fecha_nac).date()
            except:
                fecha_nac = None
        elif isinstance(fecha_nac, datetime):
            fecha_nac = fecha_nac.date()
        elif hasattr(fecha_nac, "date"):
            fecha_nac = fecha_nac.date()
        
        return {
            "tipo_documento": tipo_doc,
            "documento": documento,
            "nombre_completo": nombre_completo,
            "fecha_nacimiento": fecha_nac,
            "genero": genero,
            "telefono": telefono if telefono else None,
            "correo": correo if correo else None,
            "eps_codigo": eps_codigo,
            "eps_nombre": eps_nombre,
            "ciudad": ciudad if ciudad else None,
            "prioridad": prioridad,
            "estado": estado,
            "_row": row_num,
        }

    @staticmethod
    def get_template_columns() -> List[str]:
        """Retorna las columnas del template de Excel."""
        return ExcelReader.ALL_COLUMNS