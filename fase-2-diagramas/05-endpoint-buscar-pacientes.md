# 05 - Endpoint: GET /api/v1/pacientes/search

## Descripción

Busca pacientes por número de documento o nombres. Utiliza búsqueda case-insensitive (ILIKE en SQLite).

---

## Diagrama de Secuencia

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Cliente │     │ FastAPI │     │  Route  │     │ Service │     │  Repo   │
└────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘
     │               │               │               │               │
     │ GET /search   │               │               │               │
     │ ?q=juan       │               │               │               │
     │──────────────▶│               │               │               │
     │               │               │               │               │
     │               │ routing       │               │               │
     │               │──────────────▶│               │               │
     │               │               │               │               │
     │               │               │ search(q)     │               │
     │               │               │──────────────▶│               │
     │               │               │               │               │
     │               │               │               │ search(q)     │
     │               │               │               │──────────────▶│
     │               │               │               │               │
     │               │               │               │ WHERE         │
     │               │               │               │ nombres ILIKE │
     │               │               │               │ %juan% OR     │
     │               │               │               │ numero_doc    │
     │               │               │               │ ILIKE %juan%  │
     │               │               │               │◀──────────────│
     │               │               │               │ [matches]     │
     │               │               │◀──────────────│               │
     │               │◀──────────────│               │               │
     │ 200 OK       │               │               │               │
     │ [resultados]  │               │               │               │
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
                    │ GET /pacientes/search│
                    │ Query param: q       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ ¿q está vacío?      │
                    └──────────┬──────────┘
                         │          │
                    Sí   │          │ No
                         ▼          │
                    ┌─────────────────────┐
                    │ Return 200 []       │
                    │ (lista vacía)       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Service.search(q)   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Repository.search()│
                    │ SQL:                │
                    │ WHERE nombres       │
                    │ ILIKE '%q%' OR      │
                    │ numero_documento    │
                    │ ILIKE '%q%'         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Transformar a       │
                    │ PatientResponse[]   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Return 200 OK      │
                    │ [resultados]        │
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
GET /api/v1/pacientes/search?q=juan HTTP/1.1
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
  },
  {
    "id": 8,
    "tipo_documento": "CC",
    "numero_documento": "55555555",
    "nombres": "Juana",
    "apellidos": "Martínez",
    "fecha_nacimiento": "1985-03-20",
    "sexo": "F",
    "telefono": "3005555555",
    "correo": "juana.martinez@email.com",
    "direccion": "Av. Principal #100",
    "estado": "Activo",
    "created_at": "2025-01-16T14:00:00",
    "updated_at": "2025-01-16T14:00:00"
  }
]
```

### Response Sin Resultados (200 OK)

```json
[]
```

---

## Parámetros de Query

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|----------|-------------|
| q | string | Sí | Texto a buscar en nombres o número de documento |

---

## Códigos de Estado HTTP

| Código | Estado | Descripción |
|--------|--------|-------------|
| 200 | OK | Búsqueda completada (puede retornar array vacío) |
| 422 | Unprocessable Entity | Parámetro q faltante |

---

## Código del Endpoint

```python
# backend/routes/patient.py
@router.get("/pacientes/search", response_model=List[PatientResponse])
async def buscar_pacientes(
    q: str = Query(..., min_length=1),
    service: PatientService = Depends(get_patient_service)
):
    return service.search(query=q)
```

---

## Validaciones

1. **q es requerido** - No puede estar vacío
2. **min_length=1** - Al menos 1 carácter

---

## Notas de Implementación

- La búsqueda usa `ILIKE` en SQLite (case-insensitive)
- Busca en dos campos: `nombres` y `numero_documento`
- Retorna todos los matches sin límite (cuidado con datasets grandes)

---

**Anterior:** [04-endpoint-listar-pacientes.md](./04-endpoint-listar-pacientes.md) | **Siguiente:** [06-endpoint-contar-pacientes.md](./06-endpoint-contar-pacientes.md)