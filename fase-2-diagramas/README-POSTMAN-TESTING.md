# 🧪 Guía Completa de Pruebas con Postman - Fase 2

## 🚀 Iniciar el servidor

```powershell
cd "c:\Users\ADMINSTRADOR\Documents\prueba-tecnica\goecosystem-fullstack-test\backend"
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: **http://localhost:8000**

---

## 🌐 Documentación automática

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📋 Endpoints disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/pacientes` | Listar pacientes (paginado) |
| GET | `/api/v1/pacientes/search?q=` | Buscar pacientes |
| GET | `/api/v1/pacientes/count` | Contar pacientes |
| GET | `/api/v1/pacientes/{id}` | Obtener por ID |
| POST | `/api/v1/pacientes` | Crear paciente |
| PUT | `/api/v1/pacientes/{id}` | Actualizar paciente |
| DELETE | `/api/v1/pacientes/{id}` | Eliminar paciente |

---

## 📝 Pasos para probar cada endpoint en Postman

---

## 1️⃣ Health Check

**En Postman:**
- Método: `GET`
- URL: `http://localhost:8000/health`
- Headers: _(ninguno)_
- Body: _(ninguno)_

**Respuesta esperada:**
```json
{
    "status": "ok"
}
```

**Código de respuesta:** `200 OK`

---

## 2️⃣ Crear Paciente (POST)

**En Postman:**
- Método: `POST`
- URL: `http://localhost:8000/api/v1/pacientes`
- Headers:
  - `Content-Type`: `application/json`
- Body: Seleccionar **raw** → **JSON**

**JSON a enviar:**
```json
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

**Respuesta esperada (201 Created):**
```json
{
    "id": 1,
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
    "fecha_creacion": "2026-07-11T10:30:00",
    "fecha_actualizacion": "2026-07-11T10:30:00"
}
```

**Código de respuesta:** `201 Created`

---

## 3️⃣ Listar Pacientes (GET con paginación)

**En Postman:**
- Método: `GET`
- URL: `http://localhost:8000/api/v1/pacientes?skip=0&limit=10`
- Headers: _(ninguno)_
- Body: _(ninguno)_

**Parámetros:**
- `skip`: número de registros a omitir (para paginación)
- `limit`: número máximo de registros a devolver

**Respuesta esperada:**
```json
[
    {
        "id": 1,
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
        "fecha_creacion": "2026-07-11T10:30:00",
        "fecha_actualizacion": "2026-07-11T10:30:00"
    }
]
```

**Código de respuesta:** `200 OK`

---

## 4️⃣ Buscar Pacientes (GET)

**En Postman:**
- Método: `GET`
- URL: `http://localhost:8000/api/v1/pacientes/search?q=juan`
- Headers: _(ninguno)_
- Body: _(ninguno)_

**Parámetros:**
- `q`: texto de búsqueda (busca en nombres y número de documento)

**Respuesta esperada:**
```json
[
    {
        "id": 1,
        "tipo_documento": "CC",
        "numero_documento": "12345678",
        "nombres": "Juan Carlos",
        "apellidos": "Pérez García",
        ...
    }
]
```

**Código de respuesta:** `200 OK`

---

## 5️⃣ Contar Pacientes (GET)

**En Postman:**
- Método: `GET`
- URL: `http://localhost:8000/api/v1/pacientes/count`
- Headers: _(ninguno)_
- Body: _(ninguno)_

**Respuesta esperada:**
```json
{
    "total": 1
}
```

**Código de respuesta:** `200 OK`

---

## 6️⃣ Obtener Paciente por ID (GET)

**En Postman:**
- Método: `GET`
- URL: `http://localhost:8000/api/v1/pacientes/1`
- Headers: _(ninguno)_
- Body: _(ninguno)_

**Respuesta esperada:**
```json
{
    "id": 1,
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
    "fecha_creacion": "2026-07-11T10:30:00",
    "fecha_actualizacion": "2026-07-11T10:30:00"
}
```

**Código de respuesta:** `200 OK`

**Si el ID no existe (404 Not Found):**
```json
{
    "detail": "Paciente no encontrado"
}
```

---

## 7️⃣ Actualizar Paciente (PUT)

**En Postman:**
- Método: `PUT`
- URL: `http://localhost:8000/api/v1/pacientes/1`
- Headers:
  - `Content-Type`: `application/json`
- Body: Seleccionar **raw** → **JSON**

**JSON a enviar (solo campos a actualizar):**
```json
{
    "nombres": "Juan Carlos",
    "apellidos": "Pérez García",
    "telefono": "3009999999",
    "correo": "juan.carlos@email.com"
}
```

**Respuesta esperada:**
```json
{
    "id": 1,
    "tipo_documento": "CC",
    "numero_documento": "12345678",
    "nombres": "Juan Carlos",
    "apellidos": "Pérez García",
    "fecha_nacimiento": "1990-05-15",
    "sexo": "M",
    "telefono": "3009999999",
    "correo": "juan.carlos@email.com",
    "direccion": "Calle 123 #45-67",
    "estado": "Activo",
    "fecha_creacion": "2026-07-11T10:30:00",
    "fecha_actualizacion": "2026-07-11T10:35:00"
}
```

**Código de respuesta:** `200 OK`

---

## 8️⃣ Eliminar Paciente (DELETE)

**En Postman:**
- Método: `DELETE`
- URL: `http://localhost:8000/api/v1/pacientes/1`
- Headers: _(ninguno)_
- Body: _(ninguno)_

**Respuesta esperada:** _(vacío)_

**Código de respuesta:** `204 No Content`

---

## ⚠️ Probar casos de error

### Crear paciente duplicado (409 Conflict)

Envía el mismo `numero_documento` que ya creaste:

```json
{
    "tipo_documento": "CC",
    "numero_documento": "12345678",
    "nombres": "Otro Nombre",
    "apellidos": "Otra Apellido",
    "fecha_nacimiento": "1985-01-01",
    "sexo": "F",
    "telefono": "3100000000",
    "correo": "otro@email.com",
    "direccion": "Calle 1",
    "estado": "Activo"
}
```

**Respuesta:**
```json
{
    "detail": "Ya existe un paciente con este número de documento"
}
```

**Código:** `409 Conflict`

---

### Crear paciente con datos inválidos (422 Unprocessable Entity)

Envía solo el tipo de documento (faltan campos obligatorios):

```json
{
    "tipo_documento": "CC"
}
```

**Respuesta:**
```json
{
    "detail": [
        {
            "loc": ["body", "numero_documento"],
            "msg": "Field required",
            "type": "missing"
        },
        {
            "loc": ["body", "nombres"],
            "msg": "Field required",
            "type": "missing"
        }
    ]
}
```

**Código:** `422 Unprocessable Entity`

---

### Obtener paciente que no existe (404 Not Found)

```
GET http://localhost:8000/api/v1/pacientes/9999
```

**Respuesta:**
```json
{
    "detail": "Paciente no encontrado"
}
```

**Código:** `404 Not Found`

---

## 🔄 Flujo completo de prueba

1. ✅ `GET /health` - Verificar que el servidor funciona
2. ➕ `POST /api/v1/pacientes` - Crear paciente 1
3. ➕ `POST /api/v1/pacientes` - Crear paciente 2
4. 📋 `GET /api/v1/pacientes` - Listar todos
5. 🔍 `GET /api/v1/pacientes/search?q=` - Buscar por nombre
6. 🔢 `GET /api/v1/pacientes/count` - Contar total
7. 👁️ `GET /api/v1/pacientes/1` - Obtener por ID
8. ✏️ `PUT /api/v1/pacientes/1` - Actualizar paciente
9. ❌ `DELETE /api/v1/pacientes/2` - Eliminar paciente 2
10. 🔄 `GET /api/v1/pacientes` - Verificar cambios

---

## 💡 Comandos curl (alternativa a Postman)

```bash
# Health check
curl http://localhost:8000/health

# Crear paciente
curl -X POST http://localhost:8000/api/v1/pacientes ^
  -H "Content-Type: application/json" ^
  -d "{\"tipo_documento\":\"CC\",\"numero_documento\":\"99999999\",\"nombres\":\"María\",\"apellidos\":\"López\",\"fecha_nacimiento\":\"1985-03-20\",\"sexo\":\"F\",\"telefono\":\"3105551234\",\"correo\":\"maria@email.com\",\"direccion\":\"Carrera 10 #20-30\",\"estado\":\"Activo\"}"

# Listar pacientes
curl http://localhost:8000/api/v1/pacientes

# Buscar pacientes
curl "http://localhost:8000/api/v1/pacientes/search?q=maria"

# Contar pacientes
curl http://localhost:8000/api/v1/pacientes/count

# Obtener paciente por ID
curl http://localhost:8000/api/v1/pacientes/1

# Actualizar paciente
curl -X PUT http://localhost:8000/api/v1/pacientes/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"nombres\":\"María Elena\",\"telefono\":\"3109999999\"}"

# Eliminar paciente
curl -X DELETE http://localhost:8000/api/v1/pacientes/1
```

---

## 📊 Códigos de respuesta HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado |
| 204 | No Content - Eliminado exitosamente |
| 400 | Bad Request - Solicitud inválida |
| 404 | Not Found - Recurso no encontrado |
| 409 | Conflict - Conflicto (ej: duplicado) |
| 422 | Unprocessable Entity - Error de validación |
| 500 | Internal Server Error - Error del servidor |