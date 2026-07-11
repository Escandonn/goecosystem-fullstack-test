# 04 - Endpoint: GET /api/v1/pacientes

## Descripción

Lista todos los pacientes con paginación. Soporta los parámetros `skip` y `limit` para controlar la paginación.

---

## Diagrama de Secuencia

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Cliente │     │ FastAPI │     │  Route  │     │ Service │     │  Repo   │
└────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘
     │               │               │               │               │
     │ GET /pacientes│               │               │               │
     │ ?skip=0&limit=10               │               │               │
     │──────────────▶│               │               │               │
     │               │               │               │               │
     │               │ routing       │               │               │
     │               │──────────────▶│               │               │
     │               │               │               │               │
     │               │               │ get_all(skip, limit)          │
     │               │               │──────────────▶│               │
     │               │               │               │               │
     │               │               │               │ get_all()     │
     │               │               │               │──────────────▶│
     │               │               │               │               │
     │               │               │               │ SELECT *      │
     │               │               │               │ LIMIT 10      │
     │               │               │               │◀──────────────│
     │               │               │               │ [Patient, ...]│
     │               │               │◀──────────────│               │
     │               │◀──────────────│               │               │
     │ 200 OK       │               │               │               │
     │ [pacientes]  │               │               │               │
     │◀──────────────│               │               │               │
```

---

## Diagrama de Flujo

```
                    ┌─────────────────────┐
                    │        INICIO       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ GET /api/v1/pacientes│
                    │ Query params:        │
                    │ skip (default: 0)   │
                    │ limit (default: 10)  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ ¿skip < 0?          │
                    └──────────┬──────────┘
                         │          │
                    Sí    │          │ No
                         ▼          │
                    ┌─────────────────────┐
                    │ Error 422:          │
                    │ Validation Error    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Service.get_all()   │
                    │ skip, limit         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Repository.get_all()│
                    │ Query:              │
                    │ SELECT * FROM       │
                    │ patients            │
                    │ ORDER BY id DESC    │
                    │ LIMIT limit         │
                    │ OFFSET skip         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Transformar a      │
                    │ PatientResponse[]  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Return 200 OK      │
                    │ [pacientes]        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │        FIN          │
                    └─────────────────────┘
```

---

## Ejemplo de Request/Response

### Request

```http
GET /api/v1/pacientes?skip=0&limit=5 HTTP/1.1
Host: localhost:8000
Accept: application/json
```

### Response Exitoso (200 OK)

```json
[
  {
    "id": 5,
    "tipo_documento": "CC",
    "numero_documento": "12345678",
    "nombres": "Juan",
    "apellidos": "Pérez García",
    "fecha_nacimiento": "1990-05-15",
    "sexo": "M",
    "telefono": "3001234567",
    "correo": "juan.perez@email.com",
    "direccion": "Calle 123 #45-67",
    "estado": "Activo",
    "created_at": "2025-01-15T10:30:00",
    "updated_at": "2025-01-15T10:30:00"
  },
  {
    "id": 4,
    "tipo_documento": "TI",
    "numero_documento": "98765432",
    "nombres": "María",
    "apellidos": "López Hernández",
    "fecha_nacimiento": "2005-08-22",
    "sexo": "F",
    "telefono": "3009876543",
    "correo": "maria.lopez@email.com",
    "direccion": "Carrera 45 #12-34",
    "estado": "Activo",
    "created_at": "2025-01-14T09:15:00",
    "updated_at": "2025-01-14T09:15:00"
  }
]
```

### Response Vacío (200 OK)

```json
[]
```

---

## Parámetros de Query

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| skip | int | 0 | Número de registros a omitir (paginación) |
| limit | int | 10 | Número máximo de registros a retornar |

---

## Códigos de Estado HTTP

| Código | Estado | Descripción |
|--------|--------|-------------|
| 200 | OK | Lista de pacientes retornada exitosamente |
| 422 | Unprocessable Entity | Parámetros inválidos (skip < 0, limit <= 0) |

---

## Código del Endpoint

```python
# backend/routes/patient.py
@router.get("/pacientes", response_model=List[PatientResponse])
async def listar_pacientes(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    service: PatientService = Depends(get_patient_service)
):
    return service.get_all(skip=skip, limit=limit)
```

---

## Validaciones

1. **skip >= 0** - No puede ser negativo
2. **limit >= 1** - Debe ser al menos 1
3. **limit <= 100** - Máximo 100 registros por запрос

---

**Anterior:** [03-endpoint-health.md](./03-endpoint-health.md) | **Siguiente:** [05-endpoint-buscar-pacientes.md](./05-endpoint-buscar-pacientes.md)