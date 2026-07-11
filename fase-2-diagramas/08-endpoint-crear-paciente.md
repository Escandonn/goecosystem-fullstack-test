# 08 - Endpoint: POST /api/v1/pacientes

## Descripción

Crea un nuevo paciente. Valida que no exista otro paciente con el mismo número de documento.

---

## Diagrama de Secuencia

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Cliente │     │ FastAPI │     │  Route  │     │ Service │     │  Repo   │
└────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘
     │               │               │               │               │
     │ POST /pacientes│               │               │               │
     │ {body}        │               │               │               │
     │──────────────▶│               │               │               │
     │               │               │               │               │
     │               │ Pydantic      │               │               │
     │               │ validation    │               │               │
     │               │               │               │               │
     │               │ routing       │               │               │
     │               │──────────────▶│               │               │
     │               │               │               │               │
     │               │               │ create(data)  │               │
     │               │               │──────────────▶│               │
     │               │               │               │               │
     │               │               │ check duplicate               │
     │               │               │ get_by_documento()            │
     │               │               │──────────────▶│               │
     │               │               │               │               │
     │               │               │               │ SELECT *      │
     │               │               │               │ WHERE numero_ │
     │               │               │               │ documento=... │
     │               │               │               │◀──────────────│
     │               │               │               │ None          │
     │               │               │◀──────────────│               │
     │               │               │               │               │
     │               │               │ create()      │               │
     │               │               │──────────────▶│               │
     │               │               │               │               │
     │               │               │               │ INSERT INTO   │
     │               │               │               │ patients...   │
     │               │               │               │◀──────────────│
     │               │               │               │ Patient       │
     │               │               │◀──────────────│               │
     │               │◀──────────────│               │               │
     │ 201 Created  │               │               │               │
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
                    │ POST /pacientes    │
                    │ Body: PatientCreate│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Validar con        │
                    │ Pydantic schema    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ ¿Validación OK?    │
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
                    │ Service.create()  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ ¿Ya existe doc?   │
                    │ get_by_documento() │
                    └──────────┬──────────┘
                         │          │
                    Sí   │          │ No
                         ▼          │
                    ┌─────────────────────┐
                    │ Error 409:         │
                    │ Documento duplicado │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Repository.create()│
                    │ INSERT INTO        │
                    │ patients (...)     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Transformar a      │
                    │ PatientResponse    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Return 201 Created │
                    │ {patient}         │
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
POST /api/v1/pacientes HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Accept: application/json

{
  "tipo_documento": "CC",
  "numero_documento": "12345678",
  "nombres": "Juan Carlos",
  "apellidos": "Pérez García",
  "fecha_nacimiento": "1990-05-15",
  "sexo": "M",
  "telefono": "3001234567",
  "correo": "juan.perez@email.com",
  "direccion": "Calle 123 #45-67",
  "estado": "Activo"
}
```

### Response Exitoso (201 Created)

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

### Response Error (409 Conflict)

```json
{
  "detail": "Patient with documento 12345678 already exists"
}
```

### Response Error (422 Validation)

```json
{
  "detail": [
    {
      "loc": ["body", "correo"],
      "msg": "Invalid email format",
      "type": "value_error"
    }
  ]
}
```

---

## Body (PatientCreate Schema)

| Campo | Tipo | Requerido | Descripción |
|-------|------|----------|-------------|
| tipo_documento | string | Sí | CC, TI, PP, CE, RC, NIT |
| numero_documento | string | Sí | 5-20 caracteres, único |
| nombres | string | Sí | 2-100 caracteres |
| apellidos | string | Sí | 2-100 caracteres |
| fecha_nacimiento | date | Sí | Formato YYYY-MM-DD |
| sexo | string | Sí | M, F, O |
| telefono | string | No | 7-20 caracteres |
| correo | string | No | Formato email válido |
| direccion | string | No | Max 255 caracteres |
| estado | string | No | Default: "Activo" |

---

## Códigos de Estado HTTP

| Código | Estado | Descripción |
|--------|--------|-------------|
| 201 | Created | Paciente creado exitosamente |
| 409 | Conflict | Ya existe paciente con ese número de documento |
| 422 | Unprocessable Entity | Datos inválidos según schema |

---

## Código del Endpoint

```python
# backend/routes/patient.py
@router.post("/pacientes", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def crear_paciente(
    patient_data: PatientCreate,
    service: PatientService = Depends(get_patient_service)
):
    return service.create(patient_data)
```

---

## Validaciones del Schema

1. **tipo_documento** - Debe ser uno de: CC, TI, PP, CE, RC, NIT
2. **numero_documento** - 5-20 caracteres alfanuméricos
3. **nombres** - 2-100 caracteres
4. **apellidos** - 2-100 caracteres
5. **fecha_nacimiento** - No puede ser fecha futura
6. **sexo** - Debe ser M, F, o O
7. **telefono** - 7-20 dígitos (opcional)
8. **correo** - Formato email válido (opcional)
9. **direccion** - Máximo 255 caracteres (opcional)
10. **estado** - Default "Activo" (opcional)

---

**Anterior:** [07-endpoint-obtener-paciente.md](./07-endpoint-obtener-paciente.md) | **Siguiente:** [09-endpoint-actualizar-paciente.md](./09-endpoint-actualizar-paciente.md)