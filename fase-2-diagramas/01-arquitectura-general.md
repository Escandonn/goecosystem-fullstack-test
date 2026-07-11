# 01 - Arquitectura General de la Fase 2

## Diagrama de Arquitectura en Capas

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           ARQUITECTURA DEL BACKEND                           ║
║                         GoEcosystem Fullstack Test                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────────┐
│                              CAPA 1: CLIENTE                                 │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                         FRONTEND (Astro)                               │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │  │
│  │  │   Pages     │  │ Components  │  │   Hooks     │  │   Services   │  │  │
│  │  │  index.astro│  │ PatientForm │  │ usePatients │  │ patientApi   │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └──────────────┘  │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ HTTP/REST (JSON)
                                     │ http://localhost:8000/api/v1/pacientes
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                           CAPA 2: API (Routes)                                │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                           main.py                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │  │
│  │  │  FastAPI App                                                     │ │  │
│  │  │  ├── CORS Middleware (permite peticiones del frontend)          │ │  │
│  │  │  ├── include_router(health.router, prefix="/")                  │ │  │
│  │  │  └── include_router(patient.router, prefix="/api/v1")            │ │  │
│  │  └──────────────────────────────────────────────────────────────────┘ │  │
│  │                                                                       │ │  │
│  │  ┌─────────────────────────┐    ┌─────────────────────────────────┐ │  │
│  │  │      health.py          │    │         patient.py              │ │  │
│  │  │  GET /health            │    │  GET    /pacientes              │ │  │
│  │  │  → Sin dependencias     │    │  GET    /pacientes/search        │ │  │
│  │  │  → Retorna estado app   │    │  GET    /pacientes/count        │ │  │
│  │  │                         │    │  GET    /pacientes/{id}        │ │  │
│  │  │                         │    │  POST   /pacientes              │ │  │
│  │  │                         │    │  PUT    /pacientes/{id}        │ │  │
│  │  │                         │    │  DELETE /pacientes/{id}        │ │  │
│  │  └─────────────────────────┘    └─────────────────────────────────┘ │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ Llama métodos del Service
                                     │ patient_service.get_all(skip, limit)
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        CAPA 3: SERVICE (Lógica de Negocio)                    │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                        patient_service.py                            │  │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │  │
│  │  │  class PatientService                                           │ │  │
│  │  │                                                               │ │  │
│  │  │  Métodos:                                                      │ │  │
│  │  │  ├── get_all(skip, limit) → Lista pacientes paginada         │ │  │
│  │  │  ├── get_by_id(id) → Un paciente o 404                        │ │  │
│  │  │  ├── search(q) → Lista filtrada por nombre/documento          │ │  │
│  │  │  ├── count() → Total de pacientes                             │ │  │
│  │  │  ├── create(data) → Crea paciente (valida duplicados)        │ │  │
│  │  │  ├── update(id, data) → Actualiza (valida duplicados)        │ │  │
│  │  │  └── delete(id) → Elimina paciente                            │ │  │
│  │  │                                                               │ │  │
│  │  │  Validaciones de Negocio:                                     │ │  │
│  │  │  ├── sexo ∈ {M, F, Otro}                                      │ │  │
│  │  │  ├── estado ∈ {Activo, Inactivo}                              │ │  │
│  │  │  ├── numero_documento único                                   │ │  │
│  │  │  └── correo con formato válido                                │ │  │
│  │  └──────────────────────────────────────────────────────────────────┘ │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ Llama métodos del Repository
                                     │ patient_repository.get_all(skip, limit)
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                       CAPA 4: REPOSITORY (Acceso a Datos)                     │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                      patient_repository.py                            │  │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │  │
│  │  │  class PatientRepository                                        │ │  │
│  │  │                                                               │ │  │
│  │  │  Métodos (usan db: Session):                                   │ │  │
│  │  │  ├── get_all(skip, limit) → SELECT * FROM patients LIMIT      │ │  │
│  │  │  ├── get_by_id(id) → SELECT * FROM patients WHERE id=?        │ │  │
│  │  │  ├── get_by_documento(doc) → SELECT * WHERE numero_doc=?     │ │  │
│  │  │  ├── search(q) → SELECT * WHERE nombres ILIKE %q%            │ │  │
│  │  │  ├── count() → SELECT COUNT(*) FROM patients                 │ │  │
│  │  │  ├── create(patient) → INSERT INTO patients VALUES(...)       │ │  │
│  │  │  ├── update(patient) → UPDATE patients SET ... WHERE id=?    │ │  │
│  │  │  └── delete(patient) → DELETE FROM patients WHERE id=?       │ │  │
│  │  │                                                               │ │  │
│  │  │  Usa SQLAlchemy ORM:                                          │ │  │
│  │  │  ├── select(Patient)                                          │ │  │
│  │  │  ├── where()                                                  │ │  │
│  │  │  ├── order_by()                                               │ │  │
│  │  │  └── offset().limit()                                         │ │  │
│  │  └──────────────────────────────────────────────────────────────────┘ │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ SQLAlchemy traduce a SQL
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         CAPA 5: MODEL (Entidades)                             │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                          patient.py (models/)                          │  │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │  │
│  │  │  class Patient(Base):                                           │ │  │
│  │  │      __tablename__ = "patients"                                 │ │  │
│  │  │                                                               │ │  │
│  │  │      id = Column(Integer, primary_key=True)                    │ │  │
│  │  │      tipo_documento = Column(String(10))                       │ │  │
│  │  │      numero_documento = Column(String(20), unique=True)        │ │  │
│  │  │      nombres = Column(String(100))                             │ │  │
│  │  │      apellidos = Column(String(100))                            │ │  │
│  │  │      fecha_nacimiento = Column(String(10))                     │ │  │
│  │  │      sexo = Column(String(10))                                 │ │  │
│  │  │      telefono = Column(String(20))                             │ │  │
│  │  │      correo = Column(String(100))                              │ │  │
│  │  │      direccion = Column(String(200))                           │ │  │
│  │  │      estado = Column(String(20), default="Activo")             │ │  │
│  │  │      created_at = Column(DateTime)                             │ │  │
│  │  │      updated_at = Column(DateTime)                             │ │  │
│  │  └──────────────────────────────────────────────────────────────────┘ │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ SQLAlchemy genera SQL
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         CAPA 6: DATABASE (SQLite)                             │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                         patients.db                                   │  │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │  │
│  │  │  Tabla: patients                                                │ │  │
│  │  │  ┌────┬────────────┬───────────────┬─────────┬──────────────┐ │ │  │
│  │  │  │ id │ tipo_doc   │ numero_doc    │ nombres │ apellidos    │ │ │  │
│  │  │  ├────┼────────────┼───────────────┼─────────┼──────────────┤ │ │  │
│  │  │  │ 1  │ CC         │ 12345678      │ Juan    │ Pérez        │ │ │  │
│  │  │  │ 2  │ TI         │ 98765432      │ María   │ García       │ │ │  │
│  │  │  │ 3  │ CE         │ 55555555      │ Carlos  │ López        │ │ │  │
│  │  │  └────┴────────────┴───────────────┴─────────┴──────────────┘ │ │  │
│  │  └──────────────────────────────────────────────────────────────────┘ │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Flujo de Datos Completo

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Request │────▶│  Route  │────▶│ Service │────▶│Repository│────▶│   DB    │
│  HTTP   │     │ Handler │     │         │     │         │     │ SQLite  │
└─────────┘     └─────────┘     └─────────┘     └─────────┘     └─────────┘
     ▲              │              │              │              │
     │              │              │              │              │
     │              │              │              │              │
     │              ▼              ▼              ▼              ▼
     │         ┌─────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐
     │         │ Validar │  │ Validar   │  │ Traducir  │  │ Ejecutar  │
     │         │ Ruta    │  │ Negocio   │  │ a SQL     │  │ Query     │
     │         └─────────┘  └───────────┘  └───────────┘  └───────────┘
     │              │              │              │              │
     │              │              │              │              │
     │              ▼              ▼              ▼              ▼
     │         ┌─────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐
     └─────────│ Response│  │ Transform│  │ Retornar  │  │ Retornar  │
               │  JSON    │  │ Pydantic │  │ Modelo    │  │ Resultado │
               └─────────┘  └───────────┘  └───────────┘  └───────────┘
```

## Archivos del Backend

```
backend/
├── main.py                    # App FastAPI + startup event
├── config.py                  # Configuración legacy (no usado)
├── database.py                # Database legacy (no usado)
├── requirements.txt           # Dependencias Python
├── .env                       # Variables de entorno
│
├── core/
│   ├── __init__.py
│   └── config.py              # Settings con pydantic-settings
│
├── database/
│   ├── __init__.py
│   ├── base.py                # Base = declarative_base()
│   ├── session.py             # Engine, SessionLocal, get_db()
│   └── init_db.py             # init_db() - crea tablas
│
├── models/
│   ├── __init__.py
│   └── patient.py             # Clase Patient (SQLAlchemy)
│
├── schemas/
│   ├── __init__.py
│   └── patient.py             # PatientBase, PatientCreate, PatientUpdate, PatientResponse
│
├── repositories/
│   ├── __init__.py
│   └── patient_repository.py  # PatientRepository
│
├── services/
│   ├── __init__.py
│   └── patient_service.py     # PatientService
│
└── routes/
    ├── __init__.py
    ├── health.py              # GET /health
    └── patient.py             # CRUD /api/v1/pacientes
```

## Middleware y Configuración

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Middleware Stack                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Request ──▶ CORS ──▶ GZip ──▶ Routing ──▶ Endpoint       │
│                                                             │
│  CORS: Permite peticiones desde http://localhost:4321      │
│  (Frontend Astro)                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Inicialización de la Aplicación

```
┌─────────────────────────────────────────────────────────────┐
│                    Startup Event (main.py)                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. load_dotenv() → Lee .env                               │
│  2. create_engine() → Conecta a SQLite                     │
│  3. init_db() → Crea tablas si no existen                  │
│  4. Server listo en http://127.0.0.1:8000                  │
│                                                             │
│  Swagger UI: http://127.0.0.1:8000/docs                    │
│  ReDoc:      http://127.0.0.1:8000/redoc                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**Anterior:** [README.md](./README.md) | **Siguiente:** [02-diagrama-clases.md](./02-diagrama-clases.md)