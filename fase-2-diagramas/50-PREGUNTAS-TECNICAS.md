# 50 Preguntas Técnicas - GoEcosystem API

## Formato Radar de Conocimiento

Este documento contiene 50 preguntas técnicas fundamentales sobre el stack tecnológico usado en el proyecto, con respuestas concisas y referencias al código.

---

## 🟢 FUNDAMENTOS FASTAPI (1-10)

### 1. ¿Qué es FastAPI y qué motor WSGI usa por defecto?
**Respuesta:** FastAPI es un framework web moderno y rápido para construir APIs con Python. Usa **Uvicorn** como servidor ASGI por defecto (también puede usar Starlette como framework base).
**Referencia:** `backend/main.py` - `from fastapi import FastAPI`

### 2. ¿Qué son los `response_model` en FastAPI?
**Respuesta:** Definen el esquema Pydantic de la respuesta. FastAPI valida automáticamente el retorno contra este modelo y genera la documentación OpenAPI.
**Referencia:** `routes/patient.py` - `@router.get("/", response_model=list[PatientResponse])`

### 3. ¿Qué son las `Dependencies` en FastAPI?
**Respuesta:** Sistema de inyección de dependencias que permite compartir lógica entre endpoints (como sesiones de BD, autenticación, etc.). Se accede mediante `Depends()`.
**Referencia:** `routes/patient.py` - `db: Session = Depends(get_db)`

### 4. ¿Qué es el sistema de routing en FastAPI?
**Respuesta:** Permite definir endpoints mediante decoradores (`@router.get()`, `@router.post()`, etc.) que mapean URLs a funciones handler. Soporta parámetros de path, query y body.
**Referencia:** `routes/patient.py` - `@router.get("/{patient_id}")`

### 5. ¿Qué es el middleware CORS en FastAPI?
**Respuesta:** Configuración que permite o restringe solicitudes de orígenes diferentes (cross-origin). Protege contra ataques CSRF y controla qué dominios pueden acceder a la API.
**Referencia:** `main.py` - `CORSMiddleware(allow_origins=settings.BACKEND_CORS_ORIGINS)`

### 6. ¿Qué son los status codes en FastAPI?
**Respuesta:** Códigos HTTP de respuesta (200, 201, 400, 404, 409, 422, 500). Se usan mediante `status=` en los decoradores o `HTTPException`.
**Referencia:** `routes/patient.py` - `status_code=status.HTTP_201_CREATED`

### 7. ¿Qué es `Query` en FastAPI?
**Respuesta:** Parámetro de función que extrae y valida query parameters de la URL. Permite definir defaults, restricciones (ge, le, min_length).
**Referencia:** `routes/patient.py` - `skip: int = Query(0, ge=0)`

### 8. ¿Qué es `UploadFile` en FastAPI?
**Respuesta:** Tipo especial para manejar archivos subidos. Proporciona acceso al archivo, filename, content_type y un file-like object.
**Referencia:** `routes/patient.py` - `file: UploadFile = File(...)`

### 9. ¿Qué es `HTTPException` en FastAPI?
**Respuesta:** Excepción que permite lanzar errores HTTP controlados con código de estado y mensaje personalizado.
**Referencia:** `services/patient_service.py` - `raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)`

### 10. ¿Qué son los tags en FastAPI?
**Respuesta:** Etiquetas para organizar endpoints en la documentación Swagger/OpenAPI. Mejoran la legibilidad de la API.
**Referencia:** `routes/patient.py` - `tags=["Pacientes"]`

---

## 🟢 SQLALCHEMY & ORM (11-20)

### 11. ¿Qué es SQLAlchemy ORM?
**Respuesta:** Mapeador objeto-relacional que permite trabajar con bases de datos usando objetos Python en lugar de SQL directo. Proporciona abstracción y seguridad.
**Referencia:** `models/patient.py` - `from sqlalchemy.orm import relationship`

### 12. ¿Qué es `Column` en SQLAlchemy?
**Respuesta:** Define una columna de la tabla. Especifica tipo de dato (Integer, String, DateTime), constraints (nullable, unique, default) y si es primary key.
**Referencia:** `models/patient.py` - `id = Column(Integer, primary_key=True, index=True)`

### 13. ¿Qué es `Session` en SQLAlchemy?
**Respuesta:** Representa una conexión/transacción con la base de datos. Permite hacer queries, inserts, updates y deletes. Se crea mediante `SessionLocal`.
**Referencia:** `database/session.py` - `SessionLocal = sessionmaker(...)`

### 14. ¿Qué es `relationship` en SQLAlchemy?
**Respuesta:** Define relaciones entre modelos (1:1, 1:N, N:N). Permite acceder a objetos relacionados como atributos.
**Referencia:** `models/patient.py` - `from sqlalchemy.orm import relationship`

### 15. ¿Qué es `query.filter()` en SQLAlchemy?
**Respuesta:** Método para filtrar resultados de consulta. Soporta múltiples condiciones con `and_`, `or_`, `ilike` para case-insensitive.
**Referencia:** `repositories/patient_repository.py` - `.filter(Patient.numero_documento == numero_documento)`

### 16. ¿Qué es `offset()` y `limit()`?
**Respuesta:** Métodos de paginación: `offset` salta registros, `limit` define cuántos traer. Esenciales para rendimiento en tablas grandes.
**Referencia:** `repositories/patient_repository.py` - `.offset(skip).limit(limit).all()`

### 17. ¿Qué es `commit()` en SQLAlchemy?
**Respuesta:** Confirma la transacción actual a la base de datos. Sin `commit()`, los cambios no persisten.
**Referencia:** `repositories/patient_repository.py` - `self.db.commit()`

### 18. ¿Qué es `refresh()` en SQLAlchemy?
**Respuesta:** Actualiza el objeto con datos actuales de la BD (útil después de un insert para obtener IDs generados).
**Referencia:** `repositories/patient_repository.py` - `self.db.refresh(patient)`

### 19. ¿Qué es `IntegrityError`?
**Respuesta:** Excepción lanzada cuando una operación viola constraints de la BD (unique, foreign key, not null). Se captura para manejar duplicados.
**Referencia:** `repositories/patient_repository.py` - `from sqlalchemy.exc import IntegrityError`

### 20. ¿Qué es `ilike` en SQLAlchemy?
**Respuesta:** Búsqueda case-insensitive con patrones. Usa `%` como wildcard. Más flexible que `==` para búsquedas parciales.
**Referencia:** `repositories/patient_repository.py` - `.ilike(f"%{query}%")`

---

## 🟢 PYDANTIC & VALIDACIÓN (21-30)

### 21. ¿Qué es Pydantic?
**Respuesta:** Biblioteca de validación de datos usando type hints de Python. Define schemas con validación automática y conversión de tipos.
**Referencia:** `schemas/patient.py` - `from pydantic import BaseModel, EmailStr, Field`

### 22. ¿Qué es `BaseModel` en Pydantic?
**Respuesta:** Clase base para todos los schemas Pydantic. Proporciona validación, serialización y documentación automática.
**Referencia:** `schemas/patient.py` - `class PatientBase(BaseModel)`

### 23. ¿Qué es `Field` en Pydantic?
**Respuesta:** Define metadata adicional para campos: descripción, max_length, default, constraints de validación.
**Referencia:** `schemas/patient.py` - `Field(..., max_length=20, description="Tipo de documento")`

### 24. ¿Qué es `EmailStr` en Pydantic?
**Respuesta:** Tipo especial que valida que el string sea un email válido. Se valida en runtime.
**Referencia:** `schemas/patient.py` - `correo: Optional[EmailStr]`

### 25. ¿Qué es `@field_validator`?
**Respuesta:** Decorador para crear validaciones personalizadas en campos. Permite transformar y rechazar valores.
**Referencia:** `schemas/patient.py` - `@field_validator("estado")`

### 26. ¿Qué es `model_dump()` en Pydantic?
**Respuesta:** Convierte el modelo a diccionario. `exclude_unset=True` excluye campos no proporcionados (útil para updates parciales).
**Referencia:** `services/patient_service.py` - `patient_data.model_dump(exclude_unset=True)`

### 27. ¿Qué es `Optional` en Python?
**Respuesta:** Indica que un campo puede ser `None`. No es un tipo real, sino un wrapper de `Union[T, None]`.
**Referencia:** `schemas/patient.py` - `telefono: Optional[str]`

### 28. ¿Qué es `List` de typing?
**Respuesta:** Tipo genérico que indica una colección de elementos. Se usa para listas tipadas en schemas y funciones.
**Referencia:** `services/patient_service.py` - `List[Dict[str, Any]]`

### 29. ¿Qué diferencia hay entre `PatientBase` y `PatientCreate`?
**Respuesta:** `PatientBase` tiene campos requeridos, `PatientCreate` hereda de él pero puede agregar validaciones específicas para creación.
**Referencia:** `schemas/patient.py` - `class PatientCreate(PatientBase)`

### 30. ¿Qué es `response_model` en FastAPI?
**Respuesta:** Especifica el schema de respuesta. FastAPI serializa el retorno y lo valida contra este modelo antes de enviarlo.
**Referencia:** `routes/patient.py` - `response_model=PatientResponse`

---

## 🟢 ARQUITECTURA & PATRONES (31-40)

### 31. ¿Qué es el patrón Repository?
**Respuesta:** Capa de abstracción que aísla la lógica de acceso a datos. El servicio usa el repositorio sin conocer detalles de la BD.
**Referencia:** `repositories/patient_repository.py` - `class PatientRepository`

### 32. ¿Qué es el patrón Service Layer?
**Respuesta:** Capa que contiene lógica de negocio. Separa las reglas de negocio de los endpoints HTTP.
**Referencia:** `services/patient_service.py` - `class PatientService`

### 33. ¿Qué es la inyección de dependencias?
**Respuesta:** Patrón donde las dependencias se pasan como parámetros en lugar de crearse internamente. Facilita testing y modularidad.
**Referencia:** `services/patient_service.py` - `def __init__(self, db: Session)`

### 34. ¿Qué es el principio de responsabilidad única (SRP)?
**Respuesta:** Cada clase/módulo debe tener una sola razón para cambiar. Las rutas solo routen, servicios solo lógica de negocio, repositorios solo acceso a datos.
**Referencia:** Estructura: `routes/`, `services/`, `repositories/`, `models/`

### 35. ¿Qué es DRY (Don't Repeat Yourself)?
**Respuesta:** Principio que evita duplicación de código. `PatientBase` es reutilizado por `PatientCreate`, `PatientUpdate`, `PatientResponse`.
**Referencia:** `schemas/patient.py` - `class PatientBase(BaseModel)`

### 36. ¿Qué es una API RESTful?
**Respuesta:** Estilo de arquitectura que usa HTTP correctamente: GET (leer), POST (crear), PUT (actualizar), DELETE (eliminar) con URLs significativas.
**Referencia:** `routes/patient.py` - `@router.get()`, `@router.post()`, `@router.put()`, `@router.delete()`

### 37. ¿Qué es el prefijo de API versioning?
**Respuesta:** `/api/v1/` indica la versión de la API. Permite evolucionar la API sin romper clientes existentes.
**Referencia:** `core/config.py` - `API_V1_PREFIX: str = "/api/v1"`

### 38. ¿Qué es el middleware?
**Respuesta:** Componente que procesa requests/responses antes/después del handler. CORS, logging, autenticación son ejemplos.
**Referencia:** `main.py` - `app.add_middleware(CORSMiddleware, ...)`

### 39. ¿Qué es una DTO (Data Transfer Object)?
**Respuesta:** Objeto para transferir datos entre capas. En este proyecto, los schemas Pydantic actúan como DTOs.
**Referencia:** `schemas/patient.py` - `class PatientCreate`, `class PatientResponse`

### 40. ¿Qué es la separación de concerns?
**Respuesta:** Principio de separar diferentes responsabilidades en módulos distintos. Este proyecto separa routes, services, repositories, models.
**Referencia:** Estructura de carpetas: `routes/`, `services/`, `repositories/`, `models/`, `schemas/`

---

## 🟢 PYTHON & BEST PRACTICES (41-50)

### 41. ¿Qué es `typing.Optional`?
**Respuesta:** Indica que un valor puede ser del tipo especificado o `None`. Equivale a `Union[T, None]`.
**Referencia:** `schemas/patient.py` - `telefono: Optional[str]`

### 42. ¿Qué es `pathlib.Path`?
**Respuesta:** API orientada a objetos para manejar rutas de archivos. Más portable y legible que `os.path`.
**Referencia:** `services/patient_service.py` - `upload_dir = Path("backend/uploads")`

### 43. ¿Qué es `shutil.copyfileobj`?
**Respuesta:** Copia contenido de un file-like object a otro de forma eficiente usando chunks.
**Referencia:** `services/patient_service.py` - `shutil.copyfileobj(file.file, buffer)`

### 44. ¿Qué es `datetime.utcnow`?
**Respuesta:** Retorna la fecha/hora actual en UTC. Usado para timestamps de auditoría (created_at, updated_at).
**Referencia:** `models/patient.py` - `default=datetime.utcnow`

### 45. ¿Qué es `__repr__` en Python?
**Respuesta:** Método especial que define la representación de string de un objeto (para debugging).
**Referencia:** `models/patient.py` - `def __repr__(self) -> str`

### 46. ¿Qué es `f-string` en Python?
**Respuesta:** Literal de string con expresiones embebidas precedidas por `f`. Más legible que `.format()`.
**Referencia:** `models/patient.py` - `f"<Patient(id={self.id}, ...)>"`

### 47. ¿Qué es `**kwargs` en Python?
**Respuesta:** Sintaxis para recibir argumentos keyword arbitrarios como diccionario. Útil para pasar parámetros dinámicamente.
**Referencia:** `models/patient.py` - `Patient(**patient_data)`

### 48. ¿Qué es `.env` y `python-dotenv`?
**Respuesta:** Archivo para variables de entorno local. `python-dotenv` las carga automáticamente al proyecto.
**Referencia:** `core/config.py` - `load_dotenv(dotenv_path=env_path)`

### 49. ¿Qué es `List[Dict[str, Any]]`?
**Respuesta:** Tipo que indica una lista de diccionarios con keys strings y values de cualquier tipo. Común para datos estructurados.
**Referencia:** `services/patient_service.py` - `List[Dict[str, Any]]`

### 50. ¿Qué es `setattr` en Python?
**Respuesta:** Función built-in para asignar atributos dinámicamente a objetos. Útil para updates parciales.
**Referencia:** `services/patient_service.py` - `setattr(patient, field, value)`

---

## 📊 DIAGRAMA RADAR DE CONOCIMIENTO

```
                    CONOCIMIENTO TÉCNICO
                    
        Python
         ╱ ╲
        ╱   ╲
       ╱  41-50╲
      ╱    ╲    ╲
     ╱      ╲    ╲
    ╱   31-40 ╲    ╲
   ╱    ╱      ╲    ╲
  ╱    ╱  21-30 ╲    ╲
 ╱    ╱    ╱      ╲    ╲
╱    ╱    ╱  11-20 ╲    ╲
    ╱    ╱    ╱      ╲    ╲
   ╱    ╱    ╱  1-10  ╲    ╲
  ╱    ╱    ╱    ╱      ╲    ╲
 FastAPI  SQLAlchemy  Pydantic
  (1-10)   (11-20)    (21-30)
```

### Leyenda de Niveles de Conocimiento

| Nivel | Descripción | Indicador |
|-------|-------------|-----------|
| 🟢 Básico | Conceptos fundamentales | 1-10 |
| 🟡 Intermedio | Aplicación práctica | 11-30 |
| 🟠 Avanzado | Patrones y arquitectura | 31-40 |
| 🔴 Experto | Best practices Python | 41-50 |

---

## 📈 AUTOEVALUACIÓN

Marca cada pregunta según tu nivel de conocimiento:

| # | Pregunta | 🟢 | 🟡 | 🟠 | 🔴 |
|---|----------|----|----|----|----|
| 1 | FastAPI framework | ○ | ○ | ○ | ○ |
| 2 | response_model | ○ | ○ | ○ | ○ |
| 3 | Dependencies | ○ | ○ | ○ | ○ |
| 4 | Routing | ○ | ○ | ○ | ○ |
| 5 | CORS Middleware | ○ | ○ | ○ | ○ |
| 6 | Status Codes | ○ | ○ | ○ | ○ |
| 7 | Query Parameters | ○ | ○ | ○ | ○ |
| 8 | UploadFile | ○ | ○ | ○ | ○ |
| 9 | HTTPException | ○ | ○ | ○ | ○ |
| 10 | Tags | ○ | ○ | ○ | ○ |
| 11 | SQLAlchemy ORM | ○ | ○ | ○ | ○ |
| 12 | Column | ○ | ○ | ○ | ○ |
| 13 | Session | ○ | ○ | ○ | ○ |
| 14 | relationship | ○ | ○ | ○ | ○ |
| 15 | filter() | ○ | ○ | ○ | ○ |
| 16 | offset/limit | ○ | ○ | ○ | ○ |
| 17 | commit() | ○ | ○ | ○ | ○ |
| 18 | refresh() | ○ | ○ | ○ | ○ |
| 19 | IntegrityError | ○ | ○ | ○ | ○ |
| 20 | ilike | ○ | ○ | ○ | ○ |
| 21 | Pydantic | ○ | ○ | ○ | ○ |
| 22 | BaseModel | ○ | ○ | ○ | ○ |
| 23 | Field | ○ | ○ | ○ | ○ |
| 24 | EmailStr | ○ | ○ | ○ | ○ |
| 25 | field_validator | ○ | ○ | ○ | ○ |
| 26 | model_dump() | ○ | ○ | ○ | ○ |
| 27 | Optional | ○ | ○ | ○ | ○ |
| 28 | List typing | ○ | ○ | ○ | ○ |
| 29 | Herencia schemas | ○ | ○ | ○ | ○ |
| 30 | response_model | ○ | ○ | ○ | ○ |
| 31 | Repository | ○ | ○ | ○ | ○ |
| 32 | Service Layer | ○ | ○ | ○ | ○ |
| 33 | DI | ○ | ○ | ○ | ○ |
| 34 | SRP | ○ | ○ | ○ | ○ |
| 35 | DRY | ○ | ○ | ○ | ○ |
| 36 | RESTful | ○ | ○ | ○ | ○ |
| 37 | API Versioning | ○ | ○ | ○ | ○ |
| 38 | Middleware | ○ | ○ | ○ | ○ |
| 39 | DTO | ○ | ○ | ○ | ○ |
| 40 | Separation | ○ | ○ | ○ | ○ |
| 41 | Optional typing | ○ | ○ | ○ | ○ |
| 42 | pathlib | ○ | ○ | ○ | ○ |
| 43 | shutil | ○ | ○ | ○ | ○ |
| 44 | datetime | ○ | ○ | ○ | ○ |
| 45 | __repr__ | ○ | ○ | ○ | ○ |
| 46 | f-string | ○ | ○ | ○ | ○ |
| 47 | **kwargs | ○ | ○ | ○ | ○ |
| 48 | dotenv | ○ | ○ | ○ | ○ |
| 49 | List[Dict] | ○ | ○ | ○ | ○ |
| 50 | setattr | ○ | ○ | ○ | ○ |

---

## 📝 Resumen por Categoría

| Categoría | Preguntas | Puntuación Máxima |
|-----------|-----------|------------------|
| FastAPI | 1-10 | 10 |
| SQLAlchemy | 11-20 | 10 |
| Pydantic | 21-30 | 10 |
| Arquitectura | 31-40 | 10 |
| Python | 41-50 | 10 |
| **TOTAL** | **1-50** | **50** |

---

*Generado para la prueba técnica GoEcosystem - 2026*