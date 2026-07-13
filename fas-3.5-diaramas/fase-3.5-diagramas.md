# Fase 3.5 - Diagramas de Arquitectura

## Índice
1. [Arquitectura en Capas](#1-arquitectura-en-capas)
2. [Flujo de una Request](#2-flujo-de-una-request)
3. [Manejo de Excepciones](#3-manejo-de-excepciones)
4. [Diagrama de Clases - Pacientes](#4-diagrama-de-clases---pacientes)
5. [Diagrama de Secuencia - Crear Paciente](#5-diagrama-de-secuencia---crear-paciente)
6. [Diagrama de Secuencia - Importar Excel](#6-diagrama-de-secuencia---importar-excel)
7. [Estructura de Errores Consistente](#7-estructura-de-errores-consistente)

---

## 1. Arquitectura en Capas

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (Astro + React)                          │
│                    Componentes React → API Calls → /api/v1/*               │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API LAYER (Routes)                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐   │
│  │  routes/health  │  │ routes/patient │  │     routes/__init__.py      │   │
│  │  GET /health    │  │ GET  /pacientes │  │                             │   │
│  │                 │  │ POST /pacientes │  │  - Router definitions       │   │
│  │                 │  │ GET  /{id}      │  │  - API versioning          │   │
│  │                 │  │ PUT  /{id}      │  │                             │   │
│  │                 │  │DELETE /{id}     │  │                             │   │
│  │                 │  │POST /importar   │  │                             │   │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘   │
│                                      │                                      │
│                              Swagger Docs (@router)                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SERVICE LAYER (Lógica de Negocio)                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        patient_service.py                            │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │   │
│  │  │ get_all_patients │  │ get_patient_by_id│  │ create_patient   │   │   │
│  │  │                  │  │                  │  │                  │   │   │
│  │  │ - Filtra por     │  │ - Busca por ID   │  │ - Valida datos   │   │   │
│  │  │   estado         │  │ - Lanza 404 si   │  │ - Checkea dni    │   │   │
│  │  │ - Paginación     │  │   no existe      │  │ - Crea en repo   │   │   │
│  │  │                  │  │                  │  │                  │   │   │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘   │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │   │
│  │  │ update_patient   │  │ delete_patient  │  │import_from_excel │   │   │
│  │  │                  │  │                  │  │                  │   │   │
│  │  │ - Checkea 404    │  │ - Checkea 404   │  │ - Lee archivo    │   │   │
│  │  │ - Checkea dni    │  │ - Soft delete    │  │ - Valida datos   │   │   │
│  │  │ - Update         │  │ - Lanza 409 si   │  │ - Batch insert   │   │   │
│  │  │                  │  │   tiene turnos   │  │ - Retorna stats  │   │   │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                      │
│                              Custom Exceptions (errors)                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         REPOSITORY LAYER (Acceso a Datos)                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      patient_repository.py                           │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │   │
│  │  │ find_all()       │  │ find_by_id()     │  │ find_by_dni()    │   │   │
│  │  │                  │  │                  │  │                  │   │   │
│  │  │ SELECT *         │  │ SELECT * WHERE   │  │ SELECT * WHERE   │   │   │
│  │  │ FROM patients    │  │ id = :id         │  │ dni = :dni       │   │   │
│  │  │ WHERE estado=?   │  │                  │  │                  │   │   │
│  │  │ LIMIT ? OFFSET ?│  │                  │  │                  │   │   │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘   │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │   │
│  │  │ create()         │  │ update()         │  │ delete()         │   │   │
│  │  │                  │  │                  │  │                  │   │   │
│  │  │ INSERT INTO      │  │ UPDATE patients  │  │ UPDATE patients  │   │   │
│  │  │ patients (...)   │  │ SET ... WHERE id │  │ SET estado=0     │   │   │
│  │  │                  │  │                  │  │ WHERE id=?       │   │   │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘   │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │ create_batch()                                                  │ │   │
│  │  │                                                                 │ │   │
│  │  │ INSERT INTO patients (...) VALUES (...), (...), (...)           │ │   │
│  │  │                                                                 │ │   │
│  │  │ Retorna: (inserted_count, duplicate_count, error_count,        │ │   │
│  │  │          inserted_ids, db_errors)                               │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MODEL LAYER (SQLAlchemy)                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                           patient.py (Model)                          │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │ class Patient(Base):                                            │ │   │
│  │  │     __tablename__ = "patients"                                  │ │   │
│  │  │                                                                 │ │   │
│  │  │     id: Mapped[int] = mapped_column(Integer, primary_key=True)  │ │   │
│  │  │     nombre: Mapped[str] = mapped_column(String(100))            │ │   │
│  │  │     apellidos: Mapped[str] = mapped_column(String(200))        │ │   │
│  │  │     dni: Mapped[str] = mapped_column(String(9), unique=True)   │ │   │
│  │  │     fecha_nacimiento: Mapped[date]                             │ │   │
│  │  │     telefono: Mapped[Optional[str]]                            │ │   │
│  │  │     email: Mapped[Optional[str]]                               │ │   │
│  │  │     direccion: Mapped[Optional[str]]                           │ │   │
│  │  │     observaciones: Mapped[Optional[str]]                       │ │   │
│  │  │     estado: Mapped[bool] = mapped_column(Boolean, default=True)│ │   │
│  │  │     created_at: Mapped[datetime]                               │ │   │
│  │  │     updated_at: Mapped[datetime]                               │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATABASE (SQLite)                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         patients.db                                 │   │
│  │  ┌─────────┬──────────┬──────┬────────────┬───────────────────┐   │   │
│  │  │   id   │  nombre  │ dni  │    email   │      estado       │   │   │
│  │  ├─────────┼──────────┼──────┼────────────┼───────────────────┤   │   │
│  │  │   1    │  Juan    │123456│juan@email  │        1         │   │   │
│  │  │   2    │  María   │789012 │maria@email │        1         │   │   │
│  │  │   3    │  Pedro   │345678 │pedro@email │        0         │   │   │
│  │  └─────────┴──────────┴──────┴────────────┴───────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Flujo de una Request

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT (Frontend)                               │
│                                                                              │
│   fetch('/api/v1/pacientes', { method: 'POST', body: {...} })                │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        │ HTTP POST /api/v1/pacientes
                                        │ Content-Type: application/json
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                           FASTAPI APPLICATION                                │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                        MIDDLEWARE STACK                                  │  │
│  │                                                                         │  │
│  │   ┌─────────────────────────────────────────────────────────────────┐   │  │
│  │   │  RequestTimingMiddleware                                       │   │  │
│  │   │  ─────────────────────────────────────────────────────────────│   │  │
│  │   │  • Genera X-Request-ID único (UUID)                           │   │  │
│  │   │  • Registra timestamp de inicio                               │   │  │
│  │   │  • Procesa request                                             │   │  │
│  │   │  • Calcula tiempo de procesamiento                            │   │  │
│  │   │  • Añade headers: X-Process-Time, X-Request-ID                │   │  │
│  │   │  • Log: [INFO] Request started: POST /api/v1/pacientes        │   │  │
│  │   └─────────────────────────────────────────────────────────────────┘   │  │
│  │                                                                         │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                        │                                      │
│                                        ▼                                      │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                        ROUTING                                         │  │
│  │                                                                         │  │
│  │   API_PREFIX = "/api/v1"                                              │  │
│  │   app.include_router(patient_router, prefix=API_PREFIX)                │  │
│  │                                                                         │  │
│  │   POST /api/v1/pacientes  →  patient_router                           │  │
│  │                                                                         │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                        │                                      │
│                                        ▼                                      │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                     routes/patient.py                                  │  │
│  │                                                                         │  │
│  │   @router.post("/", response_model=PatientResponse, status_code=201)   │  │
│  │   async def create_patient(data: PatientCreate):                       │  │
│  │       """Crea un nuevo paciente"""                                    │  │
│  │       return await patient_service.create_patient(data)                │  │
│  │                                                                         │  │
│  │   • Valida request body contra PatientCreate schema                    │  │
│  │   • Convierte tipos (str → bool para estado)                          │  │
│  │   • Llama al service                                                   │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                        │                                      │
│                                        ▼                                      │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                   services/patient_service.py                          │  │
│  │                                                                         │  │
│  │   async def create_patient(data: PatientCreate):                       │  │
│  │       logger.info("Creating patient", extra={"dni": data.dni})         │  │
│  │                                                                         │  │
│  │       # 1. Verificar si ya existe                                     │  │
│  │       existing = await patient_repository.find_by_dni(data.dni)        │  │
│  │       if existing:                                                    │  │
│  │           logger.warning("Patient already exists", extra={"dni": ...}) │  │
│  │           raise ConflictError("Ya existe un paciente con ese DNI")     │  │
│  │                                                                         │  │
│  │       # 2. Crear paciente                                             │  │
│  │       patient = await patient_repository.create(data)                  │  │
│  │       logger.info("Patient created", extra={"id": patient.id})         │  │
│  │                                                                         │  │
│  │       return patient                                                   │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                        │                                      │
│                                        ▼                                      │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                 repositories/patient_repository.py                       │  │
│  │                                                                         │  │
│  │   async def find_by_dni(dni: str) -> Optional[Patient]:                │  │
│  │       result = await db.execute(                                       │  │
│  │           select(Patient).where(Patient.dni == dni)                    │  │
│  │       )                                                                │  │
│  │       return result.scalar_one_or_none()                               │  │
│  │                                                                         │  │
│  │   async def create(data: PatientCreate) -> Patient:                    │  │
│  │       patient = Patient(**data.model_dump())                          │  │
│  │       db.add(patient)                                                  │  │
│  │       await db.commit()                                                │  │
│  │       await db.refresh(patient)                                       │  │
│  │       return patient                                                   │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                        │                                      │
│                                        ▼                                      │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                      models/patient.py                                 │  │
│  │                                                                         │  │
│  │   class Patient(Base):                                                 │  │
│  │       __tablename__ = "patients"                                       │  │
│  │       id = Column(Integer, primary_key=True)                           │  │
│  │       nombre = Column(String(100), nullable=False)                     │  │
│  │       ...                                                              │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                        │                                      │
│                                        ▼                                      │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                      database.py (Session)                              │  │
│  │                                                                         │  │
│  │   async with get_db() as session:                                      │  │
│  │       await session.execute(...)                                       │  │
│  │       await session.commit()                                           │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                        │                                      │
│                                        ▼                                      │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                         SQLite (patients.db)                            │  │
│  │                                                                         │  │
│  │   INSERT INTO patients (nombre, ...) VALUES ('Juan', ...)               │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                        │                                      │
│                                        ▼                                      │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                    RESPONSE FLOW (reverse)                              │  │
│  │                                                                         │  │
│  │   Patient ← PatientResponse ← patient_service ← patient_repository     │  │
│  │                                                                         │  │
│  │   HTTP 201 Created                                                     │  │
│  │   {                                                                    │  │
│  │     "success": true,                                                  │  │
│  │     "data": { "id": 1, "nombre": "Juan", ... },                        │  │
│  │     "message": "Paciente creado exitosamente"                           │  │
│  │   }                                                                    │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Manejo de Excepciones

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         FLUJO DE EXCEPCIONES                                │
└──────────────────────────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────────────────────┐
   │                     EXCEPTION HIERARCHY                                  │
   │                                                                         │
   │   Exception (built-in)                                                   │
   │       │                                                                 │
   │       └── AppException (base custom)                                     │
   │               │                                                         │
   │               ├── BadRequestError (400)                                 │
   │               │       └── ValidationError (422)                         │
   │               │                                                         │
   │               ├── NotFoundError (404)                                   │
   │               │                                                         │
   │               └── ConflictError (409)                                    │
   │                                                                         │
   └─────────────────────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────────────────────┐
   │                    EXCEPTION RAISING POINTS                             │
   │                                                                         │
   │  services/patient_service.py:                                           │
   │  ┌─────────────────────────────────────────────────────────────────┐  │
   │  │                                                                  │  │
   │  │  if not patient:                                                  │  │
   │  │      raise NotFoundError("Paciente no encontrado")                │  │
   │  │                                                                  │  │
   │  │  if existing_dni:                                                │  │
   │  │      raise ConflictError("Ya existe un paciente con ese DNI")      │  │
   │  │                                                                  │  │
   │  │  if not file:                                                     │  │
   │  │      raise BadRequestError("No se proporcionó archivo")           │  │
   │  │                                                                  │  │
   │  │  if invalid_data:                                                 │  │
   │  │      raise ValidationError("Datos inválidos en fila X")            │  │
   │  │                                                                  │  │
   │  └─────────────────────────────────────────────────────────────────┘  │
   │                                                                         │
   └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │                 GLOBAL EXCEPTION HANDLERS (main.py)                      │
   │                                                                         │
   │   register_exception_handlers(app)                                      │
   │   ┌─────────────────────────────────────────────────────────────────┐  │
   │   │                                                                  │  │
   │   │  @app.exception_handler(AppException)                            │  │
   │   │  async def app_exception_handler(request, exc):                  │  │
   │   │      return JSONResponse(                                       │  │
   │   │          status_code=exc.status_code,                            │  │
   │   │          content=_error_response(exc)                           │  │
   │   │      )                                                          │  │
   │   │                                                                  │  │
   │   │  @app.exception_handler(RequestValidationError)                  │  │
   │   │  async def validation_exception_handler(request, exc):           │  │
   │   │      return JSONResponse(                                       │  │
   │   │          status_code=422,                                       │  │
   │   │          content=_error_response(ValidationError(...))           │  │
   │   │      )                                                          │  │
   │   │                                                                  │  │
   │   │  @app.exception_handler(StarletteHTTPException)                  │  │
   │   │  async def http_exception_handler(request, exc):                  │  │
   │   │      return JSONResponse(                                       │  │
   │   │          status_code=exc.status_code,                           │  │
   │   │          content=_error_response(BadRequestError(exc.detail))   │  │
   │   │      )                                                          │  │
   │   │                                                                  │  │
   │   │  @app.exception_handler(Exception)                              │  │
   │   │  async def general_exception_handler(request, exc):              │  │
   │   │      logger.error("Unhandled exception", exc_info=True)         │  │
   │   │      return JSONResponse(                                       │  │
   │   │          status_code=500,                                       │  │
   │   │          content=_error_response(InternalServerError())         │  │
   │   │      )                                                          │  │
   │   │                                                                  │  │
   │  └─────────────────────────────────────────────────────────────────┘  │
   │                                                                         │
   └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │                    CONSISTENT ERROR RESPONSE FORMAT                     │
   │                                                                         │
   │   {                                                                     │
   │     "success": false,          ← Siempre false en errores               │
   │     "message": "string",        ← Mensaje legible para el cliente        │
   │     "status_code": 400,         ← Código HTTP del error                  │
   │     "timestamp": "ISO8601",     ← Cuándo ocurrió el error                │
   │     "details": {                ← Info adicional (opcional)               │
   │       "field": "error info"                                            │
   │     }                                                                    │
   │   }                                                                     │
   │                                                                         │
   └─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Diagrama de Clases - Pacientes

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          DIAGRAMA DE CLASES                                  │
│                          MÓDULO DE PACIENTES                                 │
└──────────────────────────────────────────────────────────────────────────────┘

   ┌──────────────────────────────────────────────────────────────────────────┐
   │                              SCHEMAS                                      │
   │  ┌─────────────────────────┐    ┌─────────────────────────────────────┐ │
   │  │    PatientBase           │    │         PatientResponse             │ │
   │  ├─────────────────────────┤    ├─────────────────────────────────────┤ │
   │  │ + nombre: str           │    │ + success: bool = True              │ │
   │  │ + apellidos: str        │    │ + data: PatientBase                 │ │
   │  │ + dni: str              │    │ + message: str                     │ │
   │  │ + fecha_nacimiento: date│    │ + id: int                          │ │
   │  │ + telefono: str|None    │    │ + created_at: datetime            │ │
   │  │ + email: str|None       │    │ + updated_at: datetime            │ │
   │  │ + direccion: str|None   │    └──────────────┬──────────────────────┘ │
   │  │ + observaciones: str|None│                   │ inherits              │
   │  │ + estado: bool          │                   ▼                       │
   │  └───────────┬─────────────┘    ┌─────────────────────────────────────┐ │
   │              │                   │         PatientCreate               │ │
   │              │ inherits         ├─────────────────────────────────────┤ │
   │              ▼                   │ + nombre: str                        │ │
   │  ┌─────────────────────────┐    │ + apellidos: str                     │ │
   │  │    PatientUpdate        │    │ + dni: str                           │ │
   │  ├─────────────────────────┤    │ + fecha_nacimiento: date             │ │
   │  │ + nombre: str|None      │    │ + telefono: str|None = None         │ │
   │  │ + apellidos: str|None   │    │ + email: str|None = None             │ │
   │  │ + telefono: str|None    │    │ + direccion: str|None = None        │ │
   │  │ + email: str|None       │    │ + observaciones: str|None = None   │ │
   │  │ + direccion: str|None   │    │ + estado: bool = True                │ │
   │  │ + observaciones: str|None│   └─────────────────────────────────────┘ │
   │  │ + estado: bool|None     │                                             │
   │  └─────────────────────────┘    ┌─────────────────────────────────────┐ │
   │                                 │       PatientListResponse           │ │
   │                                 ├─────────────────────────────────────┤ │
   │                                 │ + items: list[PatientResponse]      │ │
   │                                 │ + total: int                        │ │
   │                                 │ + page: int                         │ │
   │                                 │ + per_page: int                     │ │
   │                                 └─────────────────────────────────────┘ │
   │                                                                         │
   │  ┌─────────────────────────────────────────────────────────────────┐   │
   │  │                    PatientExcelRow (for import)                  │   │
   │  ├─────────────────────────────────────────────────────────────────┤   │
   │  │ + row_num: int                                                   │   │
   │  │ + nombre: str                                                    │   │
   │  │ + apellidos: str                                                 │   │
   │  │ + dni: str                                                       │   │
   │  │ + fecha_nacimiento: date                                        │   │
   │  │ + telefono: str|None                                             │   │
   │  │ + email: str|None                                                │   │
   │  │ + direccion: str|None                                            │   │
   │  │ + observaciones: str|None                                        │   │
   │  │ + estado: bool                                                   │   │
   │  │ + is_valid: bool                                                 │   │
   │  │ + errors: list[str]                                              │   │
   │  └─────────────────────────────────────────────────────────────────┘   │
   └──────────────────────────────────────────────────────────────────────────┘

   ┌──────────────────────────────────────────────────────────────────────────┐
   │                               MODEL                                       │
   │  ┌─────────────────────────────────────────────────────────────────────┐│
   │  │                            Patient                                   ││
   │  ├─────────────────────────────────────────────────────────────────────┤│
   │  │ + id: int [PK]                                                     ││
   │  │ + nombre: str                                                      ││
   │  │ + apellidos: str                                                   ││
   │  │ + dni: str [unique]                                                ││
   │  │ + fecha_nacimiento: date                                           ││
   │  │ + telefono: str|None                                               ││
   │  │ + email: str|None                                                  ││
   │  │ + direccion: str|None                                              ││
   │  │ + observaciones: str|None                                          ││
   │  │ + estado: bool                                                     ││
   │  │ + created_at: datetime                                             ││
   │  │ + updated_at: datetime                                             ││
   │  ├─────────────────────────────────────────────────────────────────────┤│
   │  │ + to_dict(): dict                                                  ││
   │  │ + from_dict(): Patient                                             ││
   │  └─────────────────────────────────────────────────────────────────────┘│
   └──────────────────────────────────────────────────────────────────────────┘

   ┌──────────────────────────────────────────────────────────────────────────┐
   │                            REPOSITORY                                     │
   │  ┌─────────────────────────────────────────────────────────────────────┐ │
   │  │                      PatientRepository                              │ │
   │  ├─────────────────────────────────────────────────────────────────────┤ │
   │  │ - db: AsyncSession                                                  │ │
   │  ├─────────────────────────────────────────────────────────────────────┤ │
   │  │ + find_all(skip, limit, estado) -> list[Patient]                    │ │
   │  │ + find_by_id(id) -> Patient|None                                    │ │
   │  │ + find_by_dni(dni) -> Patient|None                                  │ │
   │  │ + create(data) -> Patient                                           │ │
   │  │ + update(id, data) -> Patient|None                                  │ │
   │  │ + delete(id) -> bool                                                │ │
   │  │ + create_batch(items) -> BatchResult                                │ │
   │  │ + count(estado) -> int                                               │ │
   │  └─────────────────────────────────────────────────────────────────────┘ │
   └──────────────────────────────────────────────────────────────────────────┘

   ┌──────────────────────────────────────────────────────────────────────────┐
   │                             SERVICE                                       │
   │  ┌─────────────────────────────────────────────────────────────────────┐ │
   │  │                     PatientService                                   │ │
   │  ├─────────────────────────────────────────────────────────────────────┤ │
   │  │ - logger: Logger                                                    │ │
   │  ├─────────────────────────────────────────────────────────────────────┤ │
   │  │ + get_all_patients(page, per_page, estado) -> PatientListResponse   │ │
   │  │ + get_patient_by_id(id) -> PatientResponse                           │ │
   │  │ + create_patient(data) -> PatientResponse                            │ │
   │  │ + update_patient(id, data) -> PatientResponse                        │ │
   │  │ + delete_patient(id) -> dict                                         │ │
   │  │ + import_from_excel(file) -> ImportResult                            │ │
   │  └─────────────────────────────────────────────────────────────────────┘ │
   └──────────────────────────────────────────────────────────────────────────┘

   ┌──────────────────────────────────────────────────────────────────────────┐
   │                              ROUTE                                        │
   │  ┌─────────────────────────────────────────────────────────────────────┐ │
   │  │                       patient_router                                │ │
   │  ├─────────────────────────────────────────────────────────────────────┤ │
   │  │ + GET /                    → get_patients()                        │ │
   │  │ + POST /                   → create_patient()                      │ │
   │  │ + GET /{patient_id}        → get_patient()                          │ │
   │  │ + PUT /{patient_id}       → update_patient()                        │ │
   │  │ + DELETE /{patient_id}    → delete_patient()                        │ │
   │  │ + POST /importar           → import_patients()                      │ │
   │  └─────────────────────────────────────────────────────────────────────┘ │
   └──────────────────────────────────────────────────────────────────────────┘

   ┌──────────────────────────────────────────────────────────────────────────┐
   │                           RELACIONES                                     │
   │                                                                         │
   │   Route ──calls──▶ Service ──calls──▶ Repository ──uses──▶ Model      │
   │                                                                         │
   │   Schema ──validates──▶ Service                                         │
   │   Schema ◀──returns── Service                                           │
   │   Schema ◀──returns── Route                                             │
   │                                                                         │
   └──────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Diagrama de Secuencia - Crear Paciente

```
┌─────────┐     ┌─────────────┐     ┌──────────────┐     ┌───────────────┐     ┌─────────┐     ┌────────┐
│ Client  │     │  FastAPI    │     │   Route     │     │   Service     │     │  Repo   │     │   DB   │
└────┬────┘     └──────┬──────┘     └──────┬──────┘     └───────┬───────┘     └───┬─────┘     └───┬────┘
     │                 │                    │                     │                │            │
     │ POST /api/v1/   │                    │                     │                │            │
     │ pacientes       │                    │                     │                │            │
     │────────────────▶│                    │                     │                │            │
     │                 │                    │                     │                │            │
     │                 │ Route handler      │                     │                │            │
     │                 │───────────────────▶│                     │                │            │
     │                 │                    │                     │                │            │
     │                 │                    │ Validate schema     │                │            │
     │                 │                    │────────────────────▶│                │            │
     │                 │                    │                     │                │            │
     │                 │                    │                     │ Check DNI      │            │
     │                 │                    │                     │ exists?        │            │
     │                 │                    │                     │───────────────▶│            │
     │                 │                    │                     │                │            │
     │                 │                    │                     │     SELECT *   │            │
     │                 │                    │                     │     WHERE dni=?│            │
     │                 │                    │                     │                │───────────▶│
     │                 │                    │                     │                │            │
     │                 │                    │                     │     None       │            │
     │                 │                    │                     │◀───────────────│            │
     │                 │                    │                     │                │            │
     │                 │                    │                     │ Create patient│            │
     │                 │                    │                     │───────────────▶│            │
     │                 │                    │                     │                │            │
     │                 │                    │                     │     INSERT     │            │
     │                 │                    │                     │                │───────────▶│
     │                 │                    │                     │                │            │
     │                 │                    │                     │     Patient   │            │
     │                 │                    │                     │◀───────────────│            │
     │                 │                    │                     │                │            │
     │                 │                    │     PatientResponse│◀───────────────│            │
     │                 │    201 Created     │◀────────────────────│                │            │
     │◀────────────────│◀───────────────────│                     │                │            │
     │                 │                    │                     │                │            │
     │  {              │                    │                     │                │            │
     │    "success":   │                    │                     │                │            │
     │      true,      │                    │                     │                │            │
     │    "data": {...}│                    │                     │                │            │
     │  }              │                    │                     │                │            │
     │                 │                    │                     │                │            │
```

---

## 6. Diagrama de Secuencia - Importar Excel

```
┌─────────┐     ┌─────────────┐     ┌──────────────┐     ┌───────────────┐     ┌─────────┐     ┌────────┐
│ Client  │     │  FastAPI    │     │   Route     │     │   Service     │     │  Repo   │     │   DB   │
└────┬────┘     └──────┬──────┘     └──────┬──────┘     └───────┬───────┘     └───┬─────┘     └───┬────┘
     │                 │                    │                     │                │            │
     │ POST /api/v1/   │                    │                     │                │            │
     │ pacientes/      │                    │                     │                │            │
     │ importar         │                    │                     │                │            │
     │ (multipart)      │                    │                     │                │            │
     │────────────────▶│                    │                     │                │            │
     │                 │                    │                     │                │            │
     │                 │ Route handler      │                     │                │            │
     │                 │───────────────────▶│                     │                │            │
     │                 │                    │                     │                │            │
     │                 │                    │ Validate file      │                │            │
     │                 │                    │────────────────────▶│                │            │
     │                 │                    │                     │                │            │
     │                 │                    │                     │ Read Excel    │            │
     │                 │                    │                     │───────────────│            │
     │                 │                    │                     │                │            │
     │                 │                    │                     │ Parse rows    │            │
     │                 │                    │                     │                │            │
     │                 │                    │                     │ Validate rows │            │
     │                 │                    │                     │                │            │
     │                 │                    │                     │ For each row: │            │
     │                 │                    │                     │   Check DNI   │            │
     │                 │                    │                     │   ────────────│            │
     │                 │                    │                     │   if exists:  │            │
     │                 │                    │                     │     skip      │            │
     │                 │                    │                     │   else:       │            │
     │                 │                    │                     │     add to    │            │
     │                 │                    │                     │     batch     │            │
     │                 │                    │                     │                │            │
     │                 │                    │                     │ Batch insert  │            │
     │                 │                    │                     │───────────────▶│            │
     │                 │                    │                     │                │            │
     │                 │                    │                     │     INSERT     │            │
     │                 │                    │                     │     BATCH      │            │
     │                 │                    │                     │                │───────────▶│
     │                 │                    │                     │                │            │
     │                 │                    │                     │     Result     │            │
     │                 │                    │                     │◀───────────────│            │
     │                 │                    │                     │                │            │
     │                 │                    │     ImportResult    │◀───────────────│            │
     │                 │    200 OK          │◀────────────────────│                │            │
     │◀────────────────│◀───────────────────│                     │                │            │
     │                 │                    │                     │                │            │
     │  {              │                    │                     │                │            │
     │    "success":   │                    │                     │                │            │
     │      true,      │                    │                     │                │            │
     │    "message":   │                    │                     │                │            │
     │      "...",     │                    │                     │                │            │
     │    "data": {    │                    │                     │                │            │
     │      inserted:  │                    │                     │                │            │
     │        95,      │                    │                     │                │            │
     │      duplicates:│                    │                     │                │            │
     │        5,       │                    │                     │                │            │
     │      errors: 0  │                    │                     │                │            │
     │    }            │                    │                     │                │            │
     │  }              │                    │                     │                │            │
     │                 │                    │                     │                │            │
```

---

## 7. Estructura de Errores Consistente

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    CONSISTENT ERROR RESPONSE FORMAT                           │
│                                                                              │
│  All exceptions are transformed to this JSON structure:                     │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                                                                         │  │
│  │   {                                                                     │  │
│  │     "success": false,          ← BOOLEAN: Always false for errors    │  │
│  │     "message": "string",        ← STRING: Human-readable message      │  │
│  │     "status_code": 400,         ← INTEGER: HTTP status code           │  │
│  │     "timestamp": "ISO8601",     ← STRING: When error occurred        │  │
│  │     "details": {                ← OBJECT: Additional info (optional) │  │
│  │       "field": "error info",    │                                    │  │
│  │       "errors": ["list"]        │                                    │  │
│  │     }                                                                    │  │
│  │   }                                                                     │  │
│  │                                                                         │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                         EXAMPLE RESPONSES                               │  │
│  │                                                                         │  │
│  │  400 Bad Request:                                                       │  │
│  │  ─────────────────                                                      │  │
│  │  {                                                                      │  │
│  │    "success": false,                                                   │  │
│  │    "message": "No se proporcionó ningún archivo",                     │  │
│  │    "status_code": 400,                                                 │  │
│  │    "timestamp": "2024-01-15T10:30:00.000Z",                            │  │
│  │    "details": {}                                                        │  │
│  │  }                                                                      │  │
│  │                                                                         │  │
│  │  404 Not Found:                                                         │  │
│  │  ──────────────                                                         │  │
│  │  {                                                                      │  │
│  │    "success": false,                                                   │  │
│  │    "message": "Paciente no encontrado con ID: 999",                    │  │
│  │    "status_code": 404,                                                 │  │
│  │    "timestamp": "2024-01-15T10:30:00.000Z",                            │  │
│  │    "details": {"patient_id": 999}                                       │  │
│  │  }                                                                      │  │
│  │                                                                         │  │
│  │  409 Conflict:                                                         │  │
│  │  ──────────────                                                         │  │
│  │  {                                                                      │  │
│  │    "success": false,                                                   │  │
│  │    "message": "Ya existe un paciente con el DNI: 12345678A",           │  │
│  │    "status_code": 409,                                                  │  │
│  │    "timestamp": "2024-01-15T10:30:00.000Z",                             │  │
│  │    "details": {"dni": "12345678A"}                                      │  │
│  │  }                                                                      │  │
│  │                                                                         │  │
│  │  422 Validation Error:                                                  │  │
│  │  ──────────────────────                                                  │  │
│  │  {                                                                      │  │
│  │    "success": false,                                                    │  │
│  │    "message": "Error de validación en los datos proporcionados",       │  │
│  │    "status_code": 422,                                                  │  │
│  │    "timestamp": "2024-01-15T10:30:00.000Z",                             │  │
│  │    "details": {                                                         │  │
│  │      "errors": [                                                        │  │
│  │        {"loc": ["body", "dni"], "msg": "DNI inválido"}                  │  │
│  │      ]                                                                  │  │
│  │    }                                                                    │  │
│  │  }                                                                      │  │
│  │                                                                         │  │
│  │  500 Internal Server Error:                                             │  │
│  │  ──────────────────────────                                              │  │
│  │  {                                                                      │  │
│  │    "success": false,                                                    │  │
│  │    "message": "Error interno del servidor",                             │  │
│  │    "status_code": 500,                                                  │  │
│  │    "timestamp": "2024-01-15T10:30:00.000Z",                             │  │
│  │    "details": {}                                                        │  │
│  │  }                                                                      │  │
│  │                                                                         │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Resumen de Archivos Creados/Modificados

| Archivo | Propósito | Estado |
|---------|-----------|--------|
| `backend/.env` | Variables de entorno | ✅ Creado |
| `backend/core/config.py` | Configuración centralizada | ✅ Creado |
| `backend/core/logging.py` | Sistema de logging | ✅ Creado |
| `backend/core/exceptions.py` | Excepciones custom y handlers | ✅ Creado |
| `backend/core/middleware.py` | Middleware de timing | ✅ Creado |
| `backend/main.py` | Entry point con setup | ✅ Modificado |
| `backend/routes/patient.py` | Endpoints con Swagger | ✅ Modificado |
| `backend/routes/health.py` | Health check mejorado | ✅ Modificado |
| `backend/services/patient_service.py` | Lógica con logging | ✅ Modificado |
| `backend/logs/` | Directorio de logs | ✅ Creado |
| `docs/fase-3.5-diagramas.md` | Este documento | ✅ Creado |

---

*Documento generado para Fase 3.5 - Hardening del Backend*