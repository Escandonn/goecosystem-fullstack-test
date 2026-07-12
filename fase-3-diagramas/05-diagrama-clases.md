# Fase 3 — Diagrama de Clases

## Arquitectura de la Importación Excel

```
═══════════════════════════════════════════════════════════════════════════════════════
                           DIAGRAMA DE CLASES - FASE 3
═══════════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    ROUTES                                          │
│                              (patient.py)                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  + POST /pacientes/importar(file: UploadFile) → ImportResult                      │
│    └── Llama a: patient_service.import_from_excel(file)                           │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                   SERVICES                                         │
│                             (patient_service.py)                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  + import_from_excel(file: UploadFile) → ImportResult                              │
│    ├── 1. Guarda archivo temporal en uploads/                                      │
│    ├── 2. Crea ExcelReader(temp_path)                                              │
│    ├── 3. reader.read() → List[Dict]                                               │
│    ├── 4. Valida cada registro                                                     │
│    ├── 5. repository.create_batch(valid_records)                                   │
│    └── 6. Retorna ImportResult                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                    ┌─────────────────────┴─────────────────────┐
                    ▼                                           ▼
┌─────────────────────────────────────┐    ┌─────────────────────────────────────────┐
│           REPOSITORY                 │    │           UTILS                         │
│      (patient_repository.py)         │    │        (excel_reader.py)                 │
├─────────────────────────────────────┤    ├─────────────────────────────────────────┤
│  + create_batch(patients_data)      │    │  class ExcelReader                      │
│    ├── get_existing_documents()     │    │  ├── REQUIRED_COLUMNS                   │
│    ├── Verifica duplicados           │    │  ├── OPTIONAL_COLUMNS                    │
│    ├── Inserta en batch             │    │  ├── __init__(file_path)                │
│    ├── Maneja IntegrityError        │    │  ├── _validate_file()                   │
│    └── Retorna métricas             │    │  ├── read() → List[Dict]                │
│                                     │    │  ├── _validate_columns()                 │
│                                     │    │  ├── _normalize_records()                │
│                                     │    │  └── _normalize_record()                 │
│                                     │    │                                         │
│                                     │    │  class ExcelReaderError(Exception)      │
└─────────────────────────────────────┘    └─────────────────────────────────────────┘
                    │                                           │
                    │                                           ▼
                    │           ┌─────────────────────────────────────────┐
                    │           │           SCHEMAS                       │
                    │           │        (import_result.py)                │
                    │           ├─────────────────────────────────────────┤
                    │           │  class ImportResult                     │
                    │           │    ├── archivo: str                      │
                    │           │    ├── total_registros: int              │
                    │           │    ├── insertados: int                   │
                    │           │    ├── duplicados: int                  │
                    │           │    ├── errores: int                     │
                    │           │    ├── detalles_errores: List[ImportError]
                    │           │    ├── ids_insertados: List[int]        │
                    │           │    ├── mensaje: str                      │
                    │           │    ├── success: bool (property)         │
                    │           │    └── has_errors: bool (property)      │
                    │           │                                         │
                    │           │  class ImportError                      │
                    │           │    ├── row: int                         │
                    │           │    ├── column: Optional[str]            │
                    │           │    ├── value: Optional[str]             │
                    │           │    └── error: str                      │
                    │           │                                         │
                    │           │  class BatchImportResult                │
                    │           │    ├── success: bool                    │
                    │           │    ├── total_rows: int                 │
                    │           │    ├── processed: int                  │
                    │           │    ├── inserted: int                   │
                    │           │    ├── updated: int                     │
                    │           │    ├── skipped: int                     │
                    │           │    ├── errors: List[ImportValidationError]
                    │           │    ├── summary: str                     │
                    │           │    └── timestamp: datetime             │
                    │           └─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    MODELS                                          │
│                              (patient.py)                                           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  class Patient(Base)                                                                │
│    ├── id: int (PK)                                                                 │
│    ├── tipo_documento: str                                                          │
│    ├── numero_documento: str (unique)                                               │
│    ├── nombres: str                                                                  │
│    ├── apellidos: str                                                                │
│    ├── fecha_nacimiento: date                                                       │
│    ├── sexo: str                                                                     │
│    ├── telefono: str (optional)                                                      │
│    ├── correo: str (optional)                                                        │
│    ├── direccion: str (optional)                                                     │
│    ├── estado: bool                                                                  │
│    ├── created_at: datetime                                                          │
│    └── updated_at: datetime                                                          │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                   DATABASE                                          │
│                                  (SQLite)                                           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  Tabla: patients                                                                    │
│  ┌────────────┬──────────────┬────────────────────────────────────────────────┐   │
│  │ Columna    │ Tipo         │ Constraints                                    │   │
│  ├────────────┼──────────────┼────────────────────────────────────────────────┤   │
│  │ id         │ INTEGER      │ PRIMARY KEY, AUTOINCREMENT                       │   │
│  │ tipo_doc   │ VARCHAR(10)  │ NOT NULL                                        │   │
│  │ num_doc    │ VARCHAR(50)  │ NOT NULL, UNIQUE                                │   │
│  │ nombres    │ VARCHAR(100) │ NOT NULL                                        │   │
│  │ apellidos  │ VARCHAR(100) │ NOT NULL                                        │   │
│  │ fecha_nac  │ DATE         │ NOT NULL                                        │   │
│  │ sexo       │ VARCHAR(1)   │ NOT NULL                                        │   │
│  │ telefono   │ VARCHAR(20)  │ NULLABLE                                        │   │
│  │ correo     │ VARCHAR(100) │ NULLABLE                                        │   │
│  │ direccion  │ VARCHAR(255) │ NULLABLE                                        │   │
│  │ estado     │ BOOLEAN      │ DEFAULT TRUE                                    │   │
│  │ created_at │ DATETIME     │ DEFAULT CURRENT_TIMESTAMP                       │   │
│  │ updated_at │ DATETIME     │ ON UPDATE CURRENT_TIMESTAMP                     │   │
│  └────────────┴──────────────┴────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════════════
                           FLUJO DE DATOS
═══════════════════════════════════════════════════════════════════════════════════════

┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Excel      │     │  ExcelReader │     │   Service    │     │  Repository  │
│   (.xlsx)    │────▶│  (Pandas)    │────▶│  (Logic)     │────▶│  (DB)        │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                           │                    │                    │
                           ▼                    ▼                    ▼
                    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
                    │ List[Dict]   │     │ ImportResult │     │ Patient[]    │
                    │ Normalizado  │     │ (Respuesta)  │     │ (Entidades)  │
                    └──────────────┘     └──────────────┘     └──────────────┘


═══════════════════════════════════════════════════════════════════════════════════════
                           VALIDACIONES POR CAPA
═══════════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  CAPA: ExcelReader (utils/excel_reader.py)                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  ✓ Validar extensión .xlsx                                                          │
│  ✓ Validar que el archivo no esté vacío                                             │
│  ✓ Validar columnas requeridas                                                      │
│  ✓ Normalizar nombres de columnas                                                  │
│  ✓ Convertir fechas al formato correcto                                             │
│  ✓ Normalizar strings (mayúsculas, trim)                                           │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  CAPA: Service (services/patient_service.py)                                        │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  ✓ Validar número de documento no vacío                                            │
│  ✓ Validar nombres no vacíos                                                       │
│  ✓ Validar formato de fecha                                                        │
│  ✓ Validar tipo de documento válido                                                 │
│  ✓ Validar sexo válido (M/F/Otro)                                                  │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  CAPA: Repository (repositories/patient_repository.py)                             │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  ✓ Verificar documento no existe en BD                                             │
│  ✓ Manejar IntegrityError (duplicados)                                             │
│  ✓ Transacción atómica (rollback si error)                                          │
└─────────────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════════════
                           RELACIONES ENTRE CLASES
═══════════════════════════════════════════════════════════════════════════════════════

     ┌─────────────────┐
     │  FastAPI Route  │
     └────────┬────────┘
              │ inyeccón de dependencias
              ▼
     ┌─────────────────┐
     │ PatientService  │◀────────────┐
     └────────┬────────┘            │
              │ usa                 │ tiene
              ▼                     ▼
     ┌─────────────────┐   ┌─────────────────┐
     │PatientRepository│   │  ExcelReader    │
     └────────┬────────┘   └─────────────────┘
              │
              │ persiste
              ▼
     ┌─────────────────┐
     │     Patient     │
     └─────────────────┘


═══════════════════════════════════════════════════════════════════════════════════════
                           MÉTODOS PRINCIPALES
═══════════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  ExcelReader                                                                         │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  __init__(file_path: str)                                                            │
│    └── Valida que el archivo exista y sea .xlsx                                     │
│                                                                                      │
│  read() → List[Dict[str, Any]]                                                       │
│    └── Lee el Excel, valida columnas, normaliza y retorna registros                 │
│                                                                                      │
│  _validate_columns(columns: List[str])                                               │
│    └── Verifica que estén todas las columnas requeridas                             │
│                                                                                      │
│  _normalize_records(records: List[Dict]) → List[Dict]                               │
│    └── Normaliza cada registro y maneja errores por fila                            │
│                                                                                      │
│  _normalize_record(record: Dict, row_num: int) → Dict                               │
│    └── Convierte formato Excel a formato Patient                                    │
│                                                                                      │
│  @staticmethod get_template_columns() → List[str]                                    │
│    └── Retorna lista de columnas del template                                        │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  PatientService                                                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  import_from_excel(file: UploadFile) → ImportResult                                  │
│    └── Orchestrar toda la importación                                               │
│                                                                                      │
│  create_batch(patients_data: List[Dict]) → tuple                                     │
│    └── Delegado al repository                                                       │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  PatientRepository                                                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  get_existing_documents(documentos: List[str]) → set                                 │
│    └── Busca documentos existentes en BD para evitar duplicados                     │
│                                                                                      │
│  create_batch(patients_data: List[Dict]) → tuple                                     │
│    └── Inserta múltiples pacientes, retorna métricas                                │
└─────────────────────────────────────────────────────────────────────────────────────┘
```