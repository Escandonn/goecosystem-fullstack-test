# 09 - Endpoint: PUT /api/v1/pacientes/{id}

## Descripción

Actualiza un paciente existente. Valida que el paciente exista y que no haya conflicto de documento.

---

## Diagrama de Secuencia

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Cliente │     │ FastAPI │     │  Route  │     │ Service │     │  Repo   │
└────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘
     │               │               │               │               │
     │ PUT /5        │               │               │               │
     │ {body}        │               │               │               │
     │──────────────▶│               │               │               │
     │               │               │               │               │
     │               │ Pydantic      │               │               │
     │               │ validation    │               │               │
     │               │               │               │               │
     │               │ routing       │               │               │
     │               │──────────────▶│               │               │
     │               │               │               │               │
     │               │               │ update(5, data)               │
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
     │               │               │ update()     │               │
     │               │               │──────────────▶│               │
     │               │               │               │               │
     │               │               │               │ UPDATE        │
     │               │               │               │ patients SET  │
     │               │               │               │ ...           │
     │               │               │               │◀──────────────│
     │               │               │               │ Patient       │
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
                    │ PUT /pacientes/{id} │
                    │ Path: id=5          │
                    │ Body: PatientUpdate │
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
                    │ Service.update()   │
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
                    │ ¿Cambió documento? │
                    └──────────┬──────────┘
                         │          │
                    Sí   │          │ No
                         ▼          │
                    ┌─────────────────────┐
                    │ ¿Doc ya existe?    │
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
                    │ Repository.update()│
                    │ UPDATE patients    │
                    │ SET ...            │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Transformar a       │
                    │ PatientResponse    │
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
PUT /api/v1/pacientes/5 HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Accept: application/json

{
  "nombres": "Juan Carlos",
  "apellidos": "Pérez García",
  "telefono": "3001234567",
  "correo": "juan.carlos@email.com",
  "direccion": "Calle 123 #45-67 Apto 301",
  "estado": "Activo"
}
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
  "correo": "juan.carlos@email.com",
  "direccion": "Calle 123 #45-67 Apto 301",
  "estado": "Activo",
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-16T15:45:00"
}
```

### Response Error (404 Not Found)

```json
{
  "detail": "Patient with id 999 not found"
}
```

### Response Error (409 Conflict)

```json
{
  "detail": "Patient with documento 98765432 already exists"
}
```

---

## Parámetros de Path

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| id | int | ID único del paciente a actualizar |

---

## Body (PatientUpdate Schema - Todos opcionales)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| tipo_documento | string | CC, TI, PP, CE, RC, NIT |
| numero_documento | string | 5-20 caracteres, único |
| nombres | string | 2-100 caracteres |
| apellidos | string | 2-100 caracteres |
| fecha_nacimiento | date | Formato YYYY-MM-DD |
| sexo | string | M, F, O |
| telefono | string | 7-20 caracteres |
| correo | string | Formato email válido |
| direccion | string | Máximo 255 caracteres |
| estado | string | Estado del paciente |

---

## Códigos de Estado HTTP

| Código | Estado | Descripción |
|--------|--------|-------------|
| 200 | OK | Paciente actualizado exitosamente |
| 404 | Not Found | Paciente con el ID especificado no existe |
| 409 | Conflict | Número de documento ya existe en otro paciente |
| 422 | Unprocessable Entity | Datos inválidos según schema |

---

## Código del Endpoint

```python
# backend/routes/patient.py
@router.put("/pacientes/{patient_id}", response_model=PatientResponse)
async def actualizar_paciente(
    patient_id: int = Path(..., gt=0),
    patient_data: PatientUpdate = ...,
    service: PatientService = Depends(get_patient_service)
):
    return service.update(patient_id, patient_data)
```

---

## Validaciones

1. **patient_id > 0** - Debe ser un entero positivo
2. **Todos los campos opcionales** - Solo se actualizan los campos enviados
3. **Validación de documento** - Si cambia el número, verifica que no exista
4. **Schema validation** - Validaciones de formato por campo

---

**Anterior:** [08-endpoint-crear-paciente.md](./08-endpoint-crear-paciente.md) | **Siguiente:** [10-endpoint-eliminar-paciente.md](./10-endpoint-eliminar-paciente.md)