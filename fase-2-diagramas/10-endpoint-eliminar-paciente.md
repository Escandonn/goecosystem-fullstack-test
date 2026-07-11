# 10 - Endpoint: DELETE /api/v1/pacientes/{id}

## Descripción

Elimina un paciente existente. Valida que el paciente exista antes de eliminar.

---

## Diagrama de Secuencia

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Cliente │     │ FastAPI │     │  Route  │     │ Service │     │  Repo   │
└────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘
     │               │               │               │               │
     │ DELETE /5     │               │               │               │
     │──────────────▶│               │               │               │
     │               │               │               │               │
     │               │ routing       │               │               │
     │               │──────────────▶│               │               │
     │               │               │               │               │
     │               │               │ delete(5)     │               │
     │               │               │──────────────▶│               │
     │               │               │               │               │
     │               │               │ check exists │               │
     │               │               │ get_by_id(5)  │               │
     │               │               │──────────────▶│               │
     │               │               │               │               │
     │               │               │               │ SELECT *      │
     │               │               │               │ WHERE id = 5  │
     │               │               │               │◀──────────────│
     │               │               │               │ Patient      │
     │               │               │◀──────────────│               │
     │               │               │               │               │
     │               │               │ delete(5)     │               │
     │               │               │──────────────▶│               │
     │               │               │               │               │
     │               │               │               │ DELETE FROM   │
     │               │               │               │ patients      │
     │               │               │               │ WHERE id = 5  │
     │               │               │               │◀──────────────│
     │               │               │               │ True          │
     │               │               │◀──────────────│               │
     │               │◀──────────────│               │               │
     │ 204 No Content│               │               │               │
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
                    │ DELETE /pacientes/  │
                    │ {id}                │
                    │ Path param: id=5    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ ¿id es válido?      │
                    │ (int positivo)      │
                    └──────────┬──────────┘
                         │          │
                    No   │          │ Sí
                         ▼          │
                    ┌─────────────────────┐
                    │ Error 422:         │
                    │ Validation Error   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Service.delete()   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ ¿Existe paciente?  │
                    │ get_by_id(id)      │
                    └──────────┬──────────┘
                         │          │
                    No   │          │ Sí
                         ▼          │
                    ┌─────────────────────┐
                    │ Error 404:         │
                    │ Patient not found  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Repository.delete()│
                    │ SQL:                │
                    │ DELETE FROM        │
                    │ patients           │
                    │ WHERE id = 5       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Return True        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Return 204         │
                    │ No Content         │
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
DELETE /api/v1/pacientes/5 HTTP/1.1
Host: localhost:8000
Accept: application/json
```

### Response Exitoso (204 No Content)

```
HTTP/1.1 204 No Content
```

No retorna body en caso de éxito.

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
| id | int | ID único del paciente a eliminar |

---

## Códigos de Estado HTTP

| Código | Estado | Descripción |
|--------|--------|-------------|
| 204 | No Content | Paciente eliminado exitosamente (sin body) |
| 404 | Not Found | Paciente con el ID especificado no existe |
| 422 | Unprocessable Entity | ID inválido (no es número entero) |

---

## Código del Endpoint

```python
# backend/routes/patient.py
@router.delete("/pacientes/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_paciente(
    patient_id: int = Path(..., gt=0),
    service: PatientService = Depends(get_patient_service)
):
    service.delete(patient_id)
    return None
```

---

## Validaciones

1. **patient_id > 0** - Debe ser un entero positivo
2. **Debe existir** - Retorna 404 si no se encuentra

---

## Notas de Implementación

- Retorna 204 No Content (sin body) para indicar éxito
- La eliminación es **permanente** e **irreversible**
- No hay soft delete - se elimina físicamente de la base de datos

---

**Anterior:** [09-endpoint-actualizar-paciente.md](./09-endpoint-actualizar-paciente.md)