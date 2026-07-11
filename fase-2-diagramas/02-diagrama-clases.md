# 02 - Diagrama de Clases UML

## Diagrama de Clases Completo

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PAQUETE: models                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                              <<class>>                                   │    │
│  │                              Patient                                     │    │
│  ├─────────────────────────────────────────────────────────────────────────┤    │
│  │  - __tablename__: str = "patients"                                       │    │
│  ├─────────────────────────────────────────────────────────────────────────┤    │
│  │  + id: int (PK)                                                         │    │
│  │  + tipo_documento: str                                                  │    │
│  │  + numero_documento: str                                                │    │
│  │  + nombres: str                                                        │    │
│  │  + apellidos: str                                                       │    │
│  │  + fecha_nacimiento: str                                                 │    │
│  │  + sexo: str                                                            │    │
│  │  + telefono: str                                                        │    │
│  │  + correo: str                                                          │    │
│  │  + direccion: str                                                       │    │
│  │  + estado: str                                                          │    │
│  │  + created_at: datetime                                                  │    │
│  │  + updated_at: datetime                                                  │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      ▲
                                      │ hereda
                                      │
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PAQUETE: database                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                              <<class>>                                   │    │
│  │                               Base                                       │    │
│  ├─────────────────────────────────────────────────────────────────────────┤    │
│  │  - declarative_base()                                                   │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PAQUETE: schemas                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────┐  │
│  │    <<class>>          │  │    <<class>>          │  │    <<class>>      │  │
│  │    PatientBase        │  │  PatientCreate        │  │ PatientUpdate     │  │
│  ├───────────────────────┤  ├───────────────────────┤  ├───────────────────┤  │
│  │  - tipo_documento     │  │  - tipo_documento     │  │ - tipo_documento? │  │
│  │  - numero_documento   │  │  - numero_documento   │  │ - numero_documento?│  │
│  │  - nombres            │  │  - nombres            │  │ - nombres?        │  │
│  │  - apellidos         │  │  - apellidos         │  │ - apellidos?      │  │
│  │  - fecha_nacimiento   │  │  - fecha_nacimiento   │  │ - fecha_nacimiento?│  │
│  │  - sexo              │  │  - sexo              │  │ - sexo?           │  │
│  │  - telefono          │  │  - telefono          │  │ - telefono?       │  │
│  │  - correo            │  │  - correo            │  │ - correo?         │  │
│  │  - direccion         │  │  - direccion         │  │ - direccion?      │  │
│  │  - estado            │  │                      │  │ - estado?         │  │
│  ├───────────────────────┤  ├───────────────────────┤  ├───────────────────┤  │
│  │  + model_dump()       │  │  + model_dump()       │  │ + model_dump()   │  │
│  └───────────┬───────────┘  └───────────┬───────────┘  └─────────┬─────────┘  │
│              │                          │                        │            │
│              │  hereda                  │  hereda                │ hereda     │
│              ▼                          ▼                        ▼            │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                         <<class>>                                      │  │
│  │                    PatientResponse                                     │  │
│  ├─────────────────────────────────────────────────────────────────────────┤  │
│  │  + id: int                                                             │  │
│  │  + created_at: datetime                                                 │  │
│  │  + updated_at: datetime                                                 │  │
│  ├─────────────────────────────────────────────────────────────────────────┤  │
│  │  + model_dump()                                                        │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PAQUETE: repositories                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                         <<class>>                                      │  │
│  │                    PatientRepository                                   │  │
│  ├─────────────────────────────────────────────────────────────────────────┤  │
│  │  - db: Session                                                         │  │
│  ├─────────────────────────────────────────────────────────────────────────┤  │
│  │  + get_all(skip, limit) → List[Patient]                                │  │
│  │  + get_by_id(id) → Patient | None                                      │  │
│  │  + get_by_documento(numero) → Patient | None                          │  │
│  │  + search(query) → List[Patient]                                       │  │
│  │  + count() → int                                                       │  │
│  │  + create(patient) → Patient                                          │  │
│  │  + update(patient) → Patient                                          │  │
│  │  + delete(patient) → None                                              │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      ▲
                                      │ usa
                                      │
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PAQUETE: services                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                         <<class>>                                      │  │
│  │                       PatientService                                    │  │
│  ├─────────────────────────────────────────────────────────────────────────┤  │
│  │  - repository: PatientRepository                                       │  │
│  ├─────────────────────────────────────────────────────────────────────────┤  │
│  │  + get_all(skip, limit) → List[Patient]                                │  │
│  │  + get_by_id(id) → Patient | HTTPException(404)                        │  │
│  │  + search(query) → List[Patient]                                       │  │
│  │  + count() → int                                                       │  │
│  │  + create(data) → Patient | HTTPException(409)                         │  │
│  │  + update(id, data) → Patient | HTTPException(404, 409)                │  │
│  │  + delete(id) → None | HTTPException(404)                              │  │
│  ├─────────────────────────────────────────────────────────────────────────┤  │
│  │  - _validate_sexo(sexo) → None | ValueError                           │  │
│  │  - _validate_estado(estado) → None | ValueError                        │  │
│  │  - _check_duplicates(data, exclude_id) → None | HTTPException(409)    │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      ▲
                                      │ usa
                                      │
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PAQUETE: routes                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                         <<class>>                                      │  │
│  │                       patient_router                                   │  │
│  │                    (APIRouter de FastAPI)                              │  │
│  ├─────────────────────────────────────────────────────────────────────────┤  │
│  │  + GET    /pacientes              → listar_pacientes()                 │  │
│  │  + GET    /pacientes/search       → buscar_pacientes()                │  │
│  │  + GET    /pacientes/count        → contar_pacientes()                │  │
│  │  + GET    /pacientes/{id}         → obtener_paciente()                │  │
│  │  + POST   /pacientes              → crear_paciente()                 │  │
│  │  + PUT    /pacientes/{id}         → actualizar_paciente()             │  │
│  │  + DELETE /pacientes/{id}         → eliminar_paciente()              │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                         <<class>>                                      │  │
│  │                        health_router                                   │  │
│  │                    (APIRouter de FastAPI)                              │  │
│  ├─────────────────────────────────────────────────────────────────────────┤  │
│  │  + GET /health → health_check()                                        │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Relaciones entre Clases

```
                    ┌──────────────┐
                    │     Base     │
                    │ (SQLAlchemy) │
                    └──────┬───────┘
                           │ declarative_base()
                           │ crea
                           ▼
                    ┌──────────────┐
                    │   Patient    │
                    │   (Model)    │
                    └──────┬───────┘
                           │ mapea a
                           ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│PatientBase   │◀───│PatientResponse│    │   Session    │
│(Schema)      │    │   (Schema)    │    │ (SQLAlchemy) │
└──────────────┘    └──────────────┘    └──────┬───────┘
       ▲                    ▲                    │
       │ hereda            │ hereda              │ usa
       │                   │                    ▼
       │                   │            ┌──────────────┐
       │                   │            │PatientRepo  │
       │                   │            └──────┬───────┘
       │                   │                   │
       │                   │                   │ usa
       │                   │                   ▼
       │                   │            ┌──────────────┐
       │                   │            │PatientService│
       │                   │            └──────┬───────┘
       │                   │                   │
       │                   │                   │ usa
       │                   │                   ▼
       │                   │            ┌──────────────┐
       └───────────────────┴───────────▶│patient_router│
                                        │   (Routes)   │
                                        └──────────────┘
```

## Modelo de Datos (Tabla patients)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              TABLA: patients                                     │
├──────────────────────┬─────────────────┬──────────────────────────────────────┤
│ Columna              │ Tipo            │ Restricciones                          │
├──────────────────────┼─────────────────┼──────────────────────────────────────┤
│ id                   │ INTEGER         │ PRIMARY KEY, AUTOINCREMENT             │
│ tipo_documento      │ VARCHAR(10)     │ NOT NULL                               │
│ numero_documento    │ VARCHAR(20)     │ NOT NULL, UNIQUE                      │
│ nombres             │ VARCHAR(100)    │ NOT NULL                               │
│ apellidos           │ VARCHAR(100)    │ NOT NULL                               │
│ fecha_nacimiento     │ VARCHAR(10)     │ NOT NULL                               │
│ sexo                 │ VARCHAR(10)     │ NOT NULL                               │
│ telefono             │ VARCHAR(20)     │ NOT NULL                               │
│ correo               │ VARCHAR(100)    │ NOT NULL                               │
│ direccion            │ VARCHAR(200)    │ NOT NULL                               │
│ estado               │ VARCHAR(20)     │ NOT NULL, DEFAULT 'Activo'             │
│ created_at           │ DATETIME        │ NOT NULL                               │
│ updated_at           │ DATETIME        │ NOT NULL                               │
└──────────────────────┴─────────────────┴──────────────────────────────────────┘
```

## Schemas Pydantic

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           PatientBase (Base Schema)                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│  tipo_documento: str     (requerido)                                           │
│  numero_documento: str   (requerido)                                           │
│  nombres: str            (requerido)                                           │
│  apellidos: str         (requerido)                                           │
│  fecha_nacimiento: str   (requerido)                                           │
│  sexo: str               (requerido, valores válidos: M, F, Otro)              │
│  telefono: str           (requerido)                                           │
│  correo: str            (requerido, formato email)                             │
│  direccion: str          (requerido)                                           │
│  estado: str             (requerido, valores válidos: Activo, Inactivo)         │
└─────────────────────────────────────────────────────────────────────────────────┘
                    │
                    │ hereda todos los campos
                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        PatientCreate (Hereda de PatientBase)                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│  (Todos los campos de PatientBase son requeridos)                              │
│  + Validaciones adicionales:                                                   │
│    - numero_documento debe ser único en la base de datos                      │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                       PatientUpdate (Hereda de PatientBase)                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│  (Todos los campos son OPCIONALES - todos opcionales)                          │
│  - Permite actualización parcial (PATCH semantics con PUT)                       │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                    PatientResponse (Hereda de PatientBase)                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│  (Todos los campos de PatientBase + campos adicionales)                        │
│  id: int              (requerido, del modelo)                                  │
│  created_at: datetime (requerido, del modelo)                                 │
│  updated_at: datetime (requerido, del modelo)                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Métodos del Repository

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          PatientRepository                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  get_all(skip: int, limit: int)                                                │
│  ├── db.query(Patient)                                                         │
│  ├── .offset(skip)                                                             │
│  ├── .limit(limit)                                                             │
│  ├── .order_by(Patient.id.desc())                                             │
│  └── return: List[Patient]                                                     │
│                                                                                 │
│  get_by_id(id: int)                                                            │
│  ├── db.query(Patient).filter(Patient.id == id).first()                        │
│  └── return: Patient | None                                                   │
│                                                                                 │
│  get_by_documento(numero: str)                                                 │
│  ├── db.query(Patient).filter(Patient.numero_documento == numero).first()      │
│  └── return: Patient | None                                                   │
│                                                                                 │
│  search(query: str)                                                           │
│  ├── filter: nombres ILIKE %query% OR numero_documento ILIKE %query%           │
│  └── return: List[Patient]                                                    │
│                                                                                 │
│  count()                                                                       │
│  ├── db.query(func.count(Patient.id)).scalar()                                 │
│  └── return: int                                                               │
│                                                                                 │
│  create(patient: Patient)                                                      │
│  ├── db.add(patient)                                                           │
│  ├── db.commit()                                                               │
│  ├── db.refresh(patient)                                                      │
│  └── return: Patient                                                           │
│                                                                                 │
│  update(patient: Patient)                                                      │
│  ├── db.commit()                                                               │
│  ├── db.refresh(patient)                                                       │
│  └── return: Patient                                                           │
│                                                                                 │
│  delete(patient: Patient)                                                     │
│  ├── db.delete(patient)                                                        │
│  ├── db.commit()                                                               │
│  └── return: None                                                              │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

**Anterior:** [01-arquitectura-general.md](./01-arquitectura-general.md) | **Siguiente:** [03-endpoint-health.md](./03-endpoint-health.md)