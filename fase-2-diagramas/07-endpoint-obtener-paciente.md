# 07 - Endpoint: GET /api/v1/pacientes/{id}

## Descripción

Obtiene un paciente específico por su ID. Retorna 404 si no existe.

---

## Diagrama de Secuencia

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Cliente │     │ FastAPI │     │  Route  │     │ Service │     │  Repo   │
└────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘
     │               │               │               │               │
     │ GET /5        │               │               │               │
     │──────────────▶│               │               │               │
     │               │               │               │               │
     │               │ routing       │               │               │
     │               │──────────────▶│               │               │
     │               │               │               │               │
     │               │               │ get_by_id(5)  │               │
     │               │               │──────────────▶│               │
     │               │               │               │               │
     │               │               │               │ get_by_id(5)  │
     │               │               │               │──────────────▶│
     │               │               │               │               │
     │               │               │               │ SELECT *      │
     │               │               │               │ WHERE id = 5 │
     │               │               │               │◀──────────────│
     │               │               │               │ Patient      │
     │               │               │               │◀──────────────│
     │               │               │◀──────────────│               │
     │               │◀──────────────│               │               │
     │ 200 OK       │               │               │               │
     │ {patient}    │               │               │               │
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
                    │ GET /pacientes/{id} │
                    │ Path param: id=5    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ ¿id es válido?      │
                    │ (int positivo)      │
                    └──────────┬──────────┘
                         │          │
                    No    │          │ Sí
                         ▼          │
                    ┌─────────────────────┐
                    │ Error 422:          │
                    │ Validation Error    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Service.get_by_id() │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Repository.get_    │
                    │ by_id(id)           │
                    │ SQL:                │
                    │ SELECT * FROM       │
                    │ patients WHERE id=5 │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ ¿Paciente existe?  │
                    └──────────┬──────────┘
                         │          │
                    No    │          │ Sí
                         ▼          │
                    ┌─────────────────────┐
                    │ Error 404:          │
                    │ Patient not found   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Transformar a       │
                    │ PatientResponse     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Return 200 OK      │
                    │ {patient}          │
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
GET /api/v1/pacientes/5 HTTP/1.1
Host: localhost:8000
Accept: application/json
```

### Response Exitoso (200 OK)

```json
{
  "id": 5,
  "tipo_documento": "CC",
  "numero_documento": "12345678",
  "nombres": "Juan Carlos",
  "apellidos": "Pérez García",
  "fecha_nacimiento": "1990-05-15",
  "sexo": "M",
  "telefono": "3001234567",
  "correo": "juan.perez@email.com",
  "direccion": "Calle 123 #45-67",
  "estado": "Activo",
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-15T10:30:00"
}
```

### Response Error (404 Not Found)

```json
{
  "detail": "Patient with id 999 not found"
}
```

---

## Parámetros de Path

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| id | int | ID único del paciente |

---

## Códigos de Estado HTTP

| Código | Estado | Descripción |
|--------|--------|-------------|
| 200 | OK | Paciente encontrado |
| 404 | Not Found | Paciente con el ID especificado no existe |
| 422 | Unprocessable Entity | ID inválido (no es número entero) |

---

## Código del Endpoint

```python
# backend/routes/patient.py
@router.get("/pacientes/{patient_id}", response_model=PatientResponse)
async def obtener_paciente(
    patient_id: int = Path(..., gt=0),
    service: PatientService = Depends(get_patient_service)
):
    return service.get_by_id(patient_id)
```

---

## Validaciones

1. **patient_id > 0** - Debe ser un entero positivo
2. **Debe existir** - Retorna 404 si no se encuentra

---

**Anterior:** [06-endpoint-contar-pacientes.md](./06-endpoint-contar-pacientes.md) | **Siguiente:** [08-endpoint-crear-paciente.md](./08-endpoint-crear-paciente.md)