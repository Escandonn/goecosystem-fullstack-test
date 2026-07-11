# 06 - Endpoint: GET /api/v1/pacientes/count

## Descripción

Retorna el conteo total de pacientes en la base de datos. Útil para paginación y dashboards.

---

## Diagrama de Secuencia

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Cliente │     │ FastAPI │     │  Route  │     │ Service │     │  Repo   │
└────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘
     │               │               │               │               │
     │ GET /count    │               │               │               │
     │──────────────▶│               │               │               │
     │               │               │               │               │
     │               │ routing       │               │               │
     │               │──────────────▶│               │               │
     │               │               │               │               │
     │               │               │ count()       │               │
     │               │               │──────────────▶│               │
     │               │               │               │               │
     │               │               │               │ count()      │
     │               │               │               │──────────────▶│
     │               │               │               │               │
     │               │               │               │ SELECT COUNT  │
     │               │               │               │ (*) FROM       │
     │               │               │               │ patients      │
     │               │               │               │◀──────────────│
     │               │               │               │ 42            │
     │               │               │◀──────────────│               │
     │               │◀──────────────│               │               │
     │ 200 OK       │               │               │               │
     │ {"count": 42} │               │               │               │
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
                    │ GET /pacientes/count│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Service.count()    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Repository.count() │
                    │ SQL:                │
                    │ SELECT COUNT(*)     │
                    │ FROM patients       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Return count       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Return 200 OK      │
                    │ {"count": N}       │
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
GET /api/v1/pacientes/count HTTP/1.1
Host: localhost:8000
Accept: application/json
```

### Response Exitoso (200 OK)

```json
{
  "count": 42
}
```

---

## Códigos de Estado HTTP

| Código | Estado | Descripción |
|--------|--------|-------------|
| 200 | OK | Conteo retornado exitosamente |

---

## Código del Endpoint

```python
# backend/routes/patient.py
@router.get("/pacientes/count")
async def contar_pacientes(
    service: PatientService = Depends(get_patient_service)
):
    count = service.count()
    return {"count": count}
```

---

## Casos de Uso

1. **Paginación** - Calcular total de páginas
2. **Dashboard** - Mostrar estadísticas
3. **Validación** - Verificar si hay pacientes registrados

---

**Anterior:** [05-endpoint-buscar-pacientes.md](./05-endpoint-buscar-pacientes.md) | **Siguiente:** [07-endpoint-obtener-paciente.md](./07-endpoint-obtener-paciente.md)