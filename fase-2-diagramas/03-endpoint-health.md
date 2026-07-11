# 03 - Endpoint: GET /health

## Descripción

Endpoint de verificación de salud del servidor. No requiere autenticación ni parámetros.

---

## Diagrama de Secuencia

```
┌─────────┐         ┌─────────┐         ┌─────────┐         ┌─────────┐
│ Cliente │         │ FastAPI │         │  Route  │         │ Response│
└────┬────┘         └────┬────┘         └────┬────┘         └────┬────┘
     │                    │                    │                    │
     │  GET /health       │                    │                    │
     │───────────────────▶│                    │                    │
     │                    │                    │                    │
     │                    │  routing           │                    │
     │                    │───────────────────▶│                    │
     │                    │                    │                    │
     │                    │                    │  health_check()    │
     │                    │                    │───────────────────▶│
     │                    │                    │                    │
     │                    │                    │  return {          │
     │                    │                    │    "status":       │
     │                    │                    │      "healthy",    │
     │                    │                    │    "message":      │
     │                    │                    │      "API running"  │
     │                    │                    │  }                 │
     │                    │                    │◀───────────────────│
     │                    │                    │                    │
     │                    │◀───────────────────│                    │
     │                    │                    │                    │
     │  200 OK            │                    │                    │
     │  {                 │                    │                    │
     │    "status":      │                    │                    │
     │      "healthy",   │                    │                    │
     │    "message":     │                    │                    │
     │      "API running"│                    │                    │
     │  }                 │                    │                    │
     │◀───────────────────│                    │                    │
     │                    │                    │                    │
```

---

## Diagrama de Flujo

```
                    ┌─────────────────┐
                    │      INICIO     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ GET /health     │
                    │ Request recibido│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Routing match   │
                    │ /health → OK    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Ejecutar       │
                    │ health_check() │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Crear response │
                    │ JSON con       │
                    │ status y message│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Retornar 200   │
                    │ {status, msg}  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      FIN       │
                    └─────────────────┘
```

---

## Ejemplo de Request/Response

### Request

```http
GET /health HTTP/1.1
Host: localhost:8000
Accept: application/json
```

### Response Exitoso (200 OK)

```json
{
  "status": "healthy",
  "message": "API running"
}
```

### Headers de Response

```
HTTP/1.1 200 OK
content-type: application/json
content-length: 45
date: Thu, 01 Jan 2025 12:00:00 GMT
server: uvicorn
```

---

## Código del Endpoint

```python
# backend/routes/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "API running"
    }
```

---

## Códigos de Estado HTTP

| Código | Estado | Descripción |
|--------|--------|-------------|
| 200 | OK | El servidor está funcionando correctamente |
| 500 | Internal Server Error | Error interno del servidor (raro para este endpoint) |

---

## Características

- **Autenticación:** No requerida
- **Parámetros:** Ninguno
- **Rate Limit:** Sin límite específico
- **Cache:** No cacheable
- ** idempotente:** Sí (GET es idempotente por naturaleza)

---

## Casos de Uso

1. **Health Check** - Verificar que el servidor está activo
2. **Load Balancer** - Los balanceadores lo usan para verificar nodos
3. **Monitoring** - Sistemas de monitoreo lo consultan periódicamente
4. **Startup** - Verificar que la aplicación inició correctamente

---

## Validaciones

No aplica - este endpoint no tiene validaciones.

---

**Anterior:** [02-diagrama-clases.md](./02-diagrama-clases.md) | **Siguiente:** [04-endpoint-listar-pacientes.md](./04-endpoint-listar-pacientes.md)