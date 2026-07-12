"""Schema para el resultado de importación de pacientes desde Excel."""

from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime


class ImportError(BaseModel):
    """Error individual en una fila del Excel."""
    row: int
    column: Optional[str] = None
    value: Optional[str] = None
    error: str


class ImportResult(BaseModel):
    """Resultado de la importación de pacientes desde Excel."""
    archivo: str
    total_registros: int
    insertados: int
    duplicados: int
    errores: int
    detalles_errores: List[ImportError] = []
    ids_insertados: List[int] = []
    mensaje: str = ""
    
    @property
    def success(self) -> bool:
        """Indica si la importación fue exitosa."""
        return self.errores == 0 and self.insertados > 0
    
    @property
    def has_errors(self) -> bool:
        """Indica si hubo errores en la importación."""
        return self.errores > 0


class ImportValidationError(BaseModel):
    """Error de validación durante la importación."""
    row: int
    field: str
    value: Any
    message: str


class BatchImportResult(BaseModel):
    """Resultado de importación en batch con más detalles."""
    success: bool
    total_rows: int
    processed: int
    inserted: int
    updated: int
    skipped: int
    errors: List[ImportValidationError] = []
    summary: str = ""
    timestamp: datetime = datetime.now()