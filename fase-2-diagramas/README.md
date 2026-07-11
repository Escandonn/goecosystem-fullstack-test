# Fase 2 - Diagramas y Documentación

Este directorio contiene la documentación visual y explicativa de la Fase 2 del proyecto GoEcosystem.

## Estructura de Documentación

```
fase-2-diagramas/
├── README.md                    # Este archivo - índice general
├── 01-arquitectura-general.md   # Diagrama de arquitectura en capas
├── 02-diagrama-clases.md         # Diagrama UML de clases
├── 03-endpoint-health.md        # GET /health
├── 04-endpoint-listar-pacientes.md    # GET /api/v1/pacientes
├── 05-endpoint-buscar-pacientes.md    # GET /api/v1/pacientes/search
├── 06-endpoint-contar-pacientes.md   # GET /api/v1/pacientes/count
├── 07-endpoint-obtener-paciente.md   # GET /api/v1/pacientes/{id}
├── 08-endpoint-crear-paciente.md     # POST /api/v1/pacientes
├── 09-endpoint-actualizar-paciente.md # PUT /api/v1/pacientes/{id}
└── 10-endpoint-eliminar-paciente.md  # DELETE /api/v1/pacientes/{id}
```

## Resumen de Endpoints

| # | Método | Endpoint | Descripción |
|---|--------|----------|-------------|
| 1 | GET | `/health` | Verificación de estado del servidor |
| 2 | GET | `/api/v1/pacientes` | Listar todos los pacientes (paginado) |
| 3 | GET | `/api/v1/pacientes/search` | Buscar pacientes por texto |
| 4 | GET | `/api/v1/pacientes/count` | Contar total de pacientes |
| 5 | GET | `/api/v1/pacientes/{id}` | Obtener un paciente por ID |
| 6 | POST | `/api/v1/pacientes` | Crear un nuevo paciente |
| 7 | PUT | `/api/v1/pacientes/{id}` | Actualizar un paciente existente |
| 8 | DELETE | `/api/v1/pacientes/{id}` | Eliminar un paciente |

## Arquitectura en Capas

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (Frontend)                        │
│                    Astro + TypeScript + CSS                    │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER (Routes)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ health.py    │  │ patient.py   │  │ (futuros routers)    │  │
│  │ GET /health  │  │ CRUD /pacientes│ │                      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SERVICE LAYER (Lógica de Negocio)            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ PatientService                                            │  │
│  │ - get_all()      - create()      - validate_sexo()       │  │
│  │ - get_by_id()    - update()      - validate_estado()      │  │
│  │ - search()       - delete()      - check_duplicates()     │  │
│  │ - count()                                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  REPOSITORY LAYER (Acceso a Datos)              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ PatientRepository                                         │  │
│  │ - get_all()      - create()      - search()               │  │
│  │ - get_by_id()    - update()      - count()                │  │
│  │ - get_by_documento()  - delete()                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MODEL LAYER (SQLAlchemy)                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Patient (Entidad de Base de Datos)                        │  │
│  │ Tabla: patients                                          │  │
│  │ Columnas: id, tipo_documento, numero_documento, etc.     │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE (SQLite)                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Archivo: patients.db                                      │  │
│  │ Tablas: patients                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Tecnologías Utilizadas

| Componente | Tecnología | Versión |
|------------|------------|---------|
| Framework Web | FastAPI | 0.139.0 |
| Servidor ASGI | Uvicorn | 0.51.0 |
| ORM | SQLAlchemy | 2.0.51 |
| Validación | Pydantic | 2.13.4 |
| Base de Datos | SQLite | - |
| Configuración | python-dotenv | 1.2.2 |

## Flujo de una Solicitud Típica

```
1. Cliente envía request HTTP
         │
         ▼
2. FastAPI recibe y valida headers/content-type
         │
         ▼
3. Route handler procesa la ruta y método
         │
         ▼
4. Service valida reglas de negocio
         │
         ▼
5. Repository ejecuta query en BD
         │
         ▼
6. SQLAlchemy traduce a SQL y ejecuta
         │
         ▼
7. SQLite retorna resultado
         │
         ▼
8. Repository retorna datos al Service
         │
         ▼
9. Service transforma al Schema Pydantic
         │
         ▼
10. Route retorna HTTP Response
         │
         ▼
11. Cliente recibe JSON response
```

## Convenciones de los Diagramas

En cada archivo de endpoint encontrarás:

1. **Diagrama de Secuencia** - Muestra la interacción paso a paso entre componentes
2. **Diagrama de Flujo** - Representación visual del algoritmo
3. **Ejemplo de Request/Response** - JSON real de ejemplo
4. **Códigos de Estado HTTP** - Posibles respuestas del endpoint
5. **Validaciones** - Reglas de negocio aplicadas

---

**Ir a:** [01-arquitectura-general.md](./01-arquitectura-general.md)