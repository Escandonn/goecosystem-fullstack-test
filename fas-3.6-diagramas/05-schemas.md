# 📐 Schemas JSON — Fase 3.6 (JWT + RBAC)

> Documentación completa de los esquemas JSON (request/response) de todos los endpoints de la API.
> Incluye validaciones de Pydantic, ejemplos y códigos de error estandarizados.

---

## 📑 Tabla de Contenidos

1. [Esquemas de Autenticación](#1-esquemas-de-autenticación)
2. [Esquemas de Usuario](#2-esquemas-de-usuario)
3. [Esquemas de Paciente](#3-esquemas-de-paciente)
4. [Esquema de Importación](#4-esquema-de-importación)
5. [Esquemas de Error](#5-esquemas-de-error)
6. [Resumen de Endpoints](#6-resumen-de-endpoints)

---

## 1. Esquemas de Autenticación

### 1.1 LoginRequest

> Body JSON para `POST /api/v1/auth/login/json`

| Campo | Tipo | Requerido | Restricciones | Descripción |
|-------|------|-----------|---------------|-------------|
| `username` | `string` | ✅ Sí | — | Nombre de usuario |
| `password` | `string` | ✅ Sí | — | Contraseña en texto plano |

**Ejemplo:**
```json
{
    "username": "admin",
    "password": "Admin123*"
}
```

**Esquema JSON (Draft 07):**
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "LoginRequest",
    "type": "object",
    "required": ["username", "password"],
    "properties": {
        "username": {
            "type": "string",
            "description": "Nombre de usuario"
        },
        "password": {
            "type": "string",
            "description": "Contraseña en texto plano"
        }
    },
    "additionalProperties": false
}
```

---

### 1.2 Login (form-data — OAuth2)

> Body para `POST /api/v1/auth/login` (formato `application/x-www-form-urlencoded`)

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `username` | `string` | ✅ Sí | Nombre de usuario |
| `password` | `string` | ✅ Sí | Contraseña en texto plano |

> ⚠️ Este endpoint **no** usa JSON. En Postman seleccionar **x-www-form-urlencoded**.

**Ejemplo (form-data):**
```
username=admin
password=Admin123*
```

---

### 1.3 Token (Respuesta de Login)

> Respuesta exitosa de `POST /api/v1/auth/login` y `POST /api/v1/auth/login/json`

| Campo | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `access_token` | `string` | — | Token JWT de acceso |
| `token_type` | `string` | `"bearer"` | Tipo de token |
| `username` | `string` | — | Nombre de usuario autenticado |
| `rol` | `string` | — | Rol del usuario (`admin` o `user`) |

**Ejemplo:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbCI6ImFkbWluIiwiZXhwIjoxNzU3OTk5NjAwfQ.signature",
    "token_type": "bearer",
    "username": "admin",
    "rol": "admin"
}
```

**Esquema JSON:**
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Token",
    "type": "object",
    "required": ["access_token", "token_type", "username", "rol"],
    "properties": {
        "access_token": {
            "type": "string",
            "description": "Token JWT de acceso"
        },
        "token_type": {
            "type": "string",
            "enum": ["bearer"],
            "default": "bearer",
            "description": "Tipo de token"
        },
        "username": {
            "type": "string",
            "description": "Nombre de usuario autenticado"
        },
        "rol": {
            "type": "string",
            "enum": ["admin", "user"],
            "description": "Rol del usuario"
        }
    }
}
```

---

### 1.4 TokenData (Interno)

> Datos extraídos del payload del JWT. **No** se expone como endpoint, se usa internamente.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `username` | `string\|null` | ❌ No | Sub del token (username) |
| `rol` | `string\|null` | ❌ No | Rol del usuario |

**Estructura del payload JWT decodificado:**
```json
{
    "sub": "admin",
    "rol": "admin",
    "exp": 1757999600
}
```

---

## 2. Esquemas de Usuario

### 2.1 UserCreate

> Body para `POST /api/v1/users/` — **Requiere rol admin**

| Campo | Tipo | Requerido | Restricciones | Descripción |
|-------|------|-----------|---------------|-------------|
| `nombre` | `string` | ✅ Sí | max 100 chars | Nombres del usuario |
| `apellido` | `string` | ✅ Sí | max 100 chars | Apellidos del usuario |
| `correo` | `string (email)` | ✅ Sí | formato email válido | Correo electrónico único |
| `username` | `string` | ✅ Sí | min 3, max 50 chars | Nombre de usuario único |
| `rol` | `string` | ❌ No | `"admin"` o `"user"`, default `"user"` | Rol del usuario |
| `password` | `string` | ✅ Sí | min 8, max 128 chars | Contraseña |

**Ejemplo:**
```json
{
    "nombre": "María Fernanda",
    "apellido": "Gómez López",
    "correo": "maria.gomez@goecosystem.com",
    "username": "mf_gomez",
    "rol": "user",
    "password": "SecurePass123!"
}
```

**Esquema JSON:**
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "UserCreate",
    "type": "object",
    "required": ["nombre", "apellido", "correo", "username", "password"],
    "properties": {
        "nombre": {
            "type": "string",
            "maxLength": 100,
            "description": "Nombres del usuario"
        },
        "apellido": {
            "type": "string",
            "maxLength": 100,
            "description": "Apellidos del usuario"
        },
        "correo": {
            "type": "string",
            "format": "email",
            "description": "Correo electrónico único"
        },
        "username": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "description": "Nombre de usuario único"
        },
        "rol": {
            "type": "string",
            "enum": ["admin", "user"],
            "default": "user",
            "maxLength": 20,
            "description": "Rol: admin o user"
        },
        "password": {
            "type": "string",
            "minLength": 8,
            "maxLength": 128,
            "description": "Contraseña (mínimo 8 caracteres)"
        }
    },
    "additionalProperties": false
}
```

---

### 2.2 UserUpdate

> Body para `PUT /api/v1/users/{user_id}` — **Requiere rol admin**

> 💡 Todos los campos son **opcionales**. Solo se actualizan los campos enviados.

| Campo | Tipo | Requerido | Restricciones | Descripción |
|-------|------|-----------|---------------|-------------|
| `nombre` | `string\|null` | ❌ No | max 100 chars | Nombres del usuario |
| `apellido` | `string\|null` | ❌ No | max 100 chars | Apellidos del usuario |
| `correo` | `string (email)\|null` | ❌ No | formato email válido | Correo electrónico |
| `username` | `string\|null` | ❌ No | min 3, max 50 chars | Nombre de usuario |
| `rol` | `string\|null` | ❌ No | `"admin"` o `"user"` | Rol del usuario |
| `activo` | `boolean\|null` | ❌ No | `true` / `false` | Estado activo/inactivo |
| `password` | `string\|null` | ❌ No | min 8, max 128 chars | Nueva contraseña |

**Ejemplo (actualizar rol y estado):**
```json
{
    "rol": "admin",
    "activo": false
}
```

**Ejemplo (cambiar contraseña):**
```json
{
    "password": "NewSecurePass456!"
}
```

**Esquema JSON:**
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "UserUpdate",
    "type": "object",
    "properties": {
        "nombre": {
            "type": "string",
            "maxLength": 100
        },
        "apellido": {
            "type": "string",
            "maxLength": 100
        },
        "correo": {
            "type": "string",
            "format": "email"
        },
        "username": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50
        },
        "rol": {
            "type": "string",
            "enum": ["admin", "user"],
            "maxLength": 20
        },
        "activo": {
            "type": "boolean"
        },
        "password": {
            "type": "string",
            "minLength": 8,
            "maxLength": 128
        }
    },
    "additionalProperties": false
}
```

---

### 2.3 UserResponse

> Respuesta de `GET /api/v1/auth/me`, `GET /api/v1/users/`, `GET /api/v1/users/{id}`, `POST /api/v1/users/`, `PUT /api/v1/users/{id}`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | `integer` | ID único del usuario |
| `nombre` | `string` | Nombres del usuario |
| `apellido` | `string` | Apellidos del usuario |
| `correo` | `string` | Correo electrónico |
| `username` | `string` | Nombre de usuario |
| `rol` | `string` | Rol (`admin` o `user`) |
| `activo` | `boolean` | Estado activo/inactivo |
| `created_at` | `string (date-time)` | Fecha de creación (ISO 8601) |
| `updated_at` | `string (date-time)` | Fecha de última actualización (ISO 8601) |

> 🔒 **Nota de seguridad**: La contraseña **nunca** se incluye en la respuesta.

**Ejemplo:**
```json
{
    "id": 1,
    "nombre": "Administrador",
    "apellido": "Sistema",
    "correo": "admin@goecosystem.com",
    "username": "admin",
    "rol": "admin",
    "activo": true,
    "created_at": "2026-07-13T10:00:00",
    "updated_at": "2026-07-13T10:00:00"
}
```

**Esquema JSON:**
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "UserResponse",
    "type": "object",
    "required": ["id", "nombre", "apellido", "correo", "username", "rol", "activo", "created_at", "updated_at"],
    "properties": {
        "id": {
            "type": "integer",
            "description": "ID único del usuario"
        },
        "nombre": {
            "type": "string"
        },
        "apellido": {
            "type": "string"
        },
        "correo": {
            "type": "string",
            "format": "email"
        },
        "username": {
            "type": "string"
        },
        "rol": {
            "type": "string",
            "enum": ["admin", "user"]
        },
        "activo": {
            "type": "boolean"
        },
        "created_at": {
            "type": "string",
            "format": "date-time"
        },
        "updated_at": {
            "type": "string",
            "format": "date-time"
        }
    }
}
```

---

## 3. Esquemas de Paciente

### 3.1 PatientCreate

> Body para `POST /api/v1/pacientes/` — **Requiere autenticación (cualquier rol)**

| Campo | Tipo | Requerido | Restricciones | Descripción |
|-------|------|-----------|---------------|-------------|
| `tipo_documento` | `string` | ✅ Sí | max 20 chars | Tipo de documento (CC, TI, CE, etc.) |
| `numero_documento` | `string` | ✅ Sí | max 50 chars, único | Número de documento |
| `nombres` | `string` | ✅ Sí | max 100 chars | Nombres del paciente |
| `apellidos` | `string` | ✅ Sí | max 100 chars | Apellidos del paciente |
| `fecha_nacimiento` | `string` | ✅ Sí | formato `YYYY-MM-DD` | Fecha de nacimiento |
| `sexo` | `string` | ✅ Sí | `"M"`, `"F"` u `"Otro"` | Sexo del paciente |
| `telefono` | `string\|null` | ❌ No | max 20 chars | Teléfono de contacto |
| `correo` | `string (email)\|null` | ❌ No | formato email válido | Correo electrónico |
| `direccion` | `string\|null` | ❌ No | max 255 chars | Dirección de residencia |
| `estado` | `string` | ❌ No | `"Activo"` o `"Inactivo"`, default `"Activo"` | Estado del paciente |

**Ejemplo:**
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

**Esquema JSON:**
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "PatientCreate",
    "type": "object",
    "required": ["tipo_documento", "numero_documento", "nombres", "apellidos", "fecha_nacimiento", "sexo"],
    "properties": {
        "tipo_documento": {
            "type": "string",
            "maxLength": 20,
            "description": "Tipo de documento (CC, TI, CE, etc.)"
        },
        "numero_documento": {
            "type": "string",
            "maxLength": 50,
            "description": "Número de documento único"
        },
        "nombres": {
            "type": "string",
            "maxLength": 100
        },
        "apellidos": {
            "type": "string",
            "maxLength": 100
        },
        "fecha_nacimiento": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
            "description": "Fecha de nacimiento (YYYY-MM-DD)"
        },
        "sexo": {
            "type": "string",
            "enum": ["M", "F", "Otro"],
            "description": "Sexo del paciente"
        },
        "telefono": {
            "type": ["string", "null"],
            "maxLength": 20
        },
        "correo": {
            "type": ["string", "null"],
            "format": "email"
        },
        "direccion": {
            "type": ["string", "null"],
            "maxLength": 255
        },
        "estado": {
            "type": "string",
            "enum": ["Activo", "Inactivo"],
            "default": "Activo"
        }
    },
    "additionalProperties": false
}
```

---

### 3.2 PatientUpdate

> Body para `PUT /api/v1/pacientes/{patient_id}` — **Requiere autenticación (cualquier rol)**

> 💡 Todos los campos son **opcionales**. Solo se actualizan los campos enviados.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `tipo_documento` | `string\|null` | max 20 chars | Tipo de documento |
| `numero_documento` | `string\|null` | max 50 chars | Número de documento |
| `nombres` | `string\|null` | max 100 chars | Nombres del paciente |
| `apellidos` | `string\|null` | max 100 chars | Apellidos del paciente |
| `fecha_nacimiento` | `string\|null` | `YYYY-MM-DD` | Fecha de nacimiento |
| `sexo` | `string\|null` | `"M"`, `"F"`, `"Otro"` | Sexo del paciente |
| `telefono` | `string\|null` | max 20 chars | Teléfono de contacto |
| `correo` | `string (email)\|null` | email válido | Correo electrónico |
| `direccion` | `string\|null` | max 255 chars | Dirección de residencia |
| `estado` | `string\|null` | `"Activo"`, `"Inactivo"` | Estado del paciente |

**Ejemplo (actualizar teléfono y dirección):**
```json
{
    "telefono": "3109876543",
    "direccion": "Av. Caracas #10-20"
}
```

**Esquema JSON:**
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "PatientUpdate",
    "type": "object",
    "properties": {
        "tipo_documento": {
            "type": "string",
            "maxLength": 20
        },
        "numero_documento": {
            "type": "string",
            "maxLength": 50
        },
        "nombres": {
            "type": "string",
            "maxLength": 100
        },
        "apellidos": {
            "type": "string",
            "maxLength": 100
        },
        "fecha_nacimiento": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        "sexo": {
            "type": "string",
            "enum": ["M", "F", "Otro"]
        },
        "telefono": {
            "type": ["string", "null"],
            "maxLength": 20
        },
        "correo": {
            "type": ["string", "null"],
            "format": "email"
        },
        "direccion": {
            "type": ["string", "null"],
            "maxLength": 255
        },
        "estado": {
            "type": "string",
            "enum": ["Activo", "Inactivo"]
        }
    },
    "additionalProperties": false
}
```

---

### 3.3 PatientResponse

> Respuesta de todos los endpoints `GET`, `POST` y `PUT` de `/api/v1/pacientes`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | `integer` | ID único del paciente |
| `tipo_documento` | `string` | Tipo de documento |
| `numero_documento` | `string` | Número de documento |
| `nombres` | `string` | Nombres del paciente |
| `apellidos` | `string` | Apellidos del paciente |
| `fecha_nacimiento` | `string` | Fecha de nacimiento (`YYYY-MM-DD`) |
| `sexo` | `string` | Sexo (`M`, `F`, `Otro`) |
| `telefono` | `string\|null` | Teléfono de contacto |
| `correo` | `string\|null` | Correo electrónico |
| `direccion` | `string\|null` | Dirección de residencia |
| `estado` | `string` | Estado (`Activo` o `Inactivo`) |
| `created_at` | `string (date-time)` | Fecha de creación (ISO 8601) |
| `updated_at` | `string (date-time)` | Fecha de última actualización (ISO 8601) |

**Ejemplo:**
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
    "created_at": "2026-07-11T10:30:00",
    "updated_at": "2026-07-11T10:30:00"
}
```

**Esquema JSON:**
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "PatientResponse",
    "type": "object",
    "required": ["id", "tipo_documento", "numero_documento", "nombres", "apellidos", "fecha_nacimiento", "sexo", "estado", "created_at", "updated_at"],
    "properties": {
        "id": {
            "type": "integer"
        },
        "tipo_documento": {
            "type": "string"
        },
        "numero_documento": {
            "type": "string"
        },
        "nombres": {
            "type": "string"
        },
        "apellidos": {
            "type": "string"
        },
        "fecha_nacimiento": {
            "type": "string"
        },
        "sexo": {
            "type": "string",
            "enum": ["M", "F", "Otro"]
        },
        "telefono": {
            "type": ["string", "null"]
        },
        "correo": {
            "type": ["string", "null"]
        },
        "direccion": {
            "type": ["string", "null"]
        },
        "estado": {
            "type": "string",
            "enum": ["Activo", "Inactivo"]
        },
        "created_at": {
            "type": "string",
            "format": "date-time"
        },
        "updated_at": {
            "type": "string",
            "format": "date-time"
        }
    }
}
```

---

### 3.4 CountResponse

> Respuesta de `GET /api/v1/pacientes/count`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `total` | `integer` | Número total de pacientes |

**Ejemplo:**
```json
{
    "total": 42
}
```

---

## 4. Esquema de Importación

### 4.1 ImportResult

> Respuesta de `POST /api/v1/pacientes/importar` — **Requiere rol admin**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `archivo` | `string` | Nombre del archivo procesado |
| `total_registros` | `integer` | Total de filas en el Excel |
| `insertados` | `integer` | Pacientes insertados exitosamente |
| `duplicados` | `integer` | Documentos ya existentes (omitidos) |
| `errores` | `integer` | Filas con errores de validación |
| `detalles_errores` | `array[ImportError]` | Lista detallada de errores |
| `ids_insertados` | `array[integer]` | IDs de los pacientes insertados |
| `mensaje` | `string` | Mensaje resumen de la operación |

### 4.2 ImportError

> Cada elemento dentro de `detalles_errores`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `row` | `integer` | Número de fila en el Excel |
| `column` | `string\|null` | Columna donde ocurrió el error |
| `value` | `string\|null` | Valor que causó el error |
| `error` | `string` | Descripción del error |

**Ejemplo de respuesta exitosa:**
```json
{
    "archivo": "pacientes.xlsx",
    "total_registros": 10,
    "insertados": 8,
    "duplicados": 1,
    "errores": 1,
    "detalles_errores": [
        {
            "row": 5,
            "column": "FechaNacimiento",
            "value": "15/05/1990",
            "error": "Formato de fecha inválido. Use YYYY-MM-DD"
        }
    ],
    "ids_insertados": [11, 12, 13, 14, 15, 16, 17, 18],
    "mensaje": "Importación completada: 8 insertados, 1 duplicado, 1 error"
}
```

**Esquema JSON:**
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "ImportResult",
    "type": "object",
    "required": ["archivo", "total_registros", "insertados", "duplicados", "errores"],
    "properties": {
        "archivo": {
            "type": "string",
            "description": "Nombre del archivo procesado"
        },
        "total_registros": {
            "type": "integer",
            "description": "Total de filas en el Excel"
        },
        "insertados": {
            "type": "integer",
            "description": "Pacientes insertados exitosamente"
        },
        "duplicados": {
            "type": "integer",
            "description": "Documentos ya existentes (omitidos)"
        },
        "errores": {
            "type": "integer",
            "description": "Filas con errores de validación"
        },
        "detalles_errores": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "row": { "type": "integer" },
                    "column": { "type": ["string", "null"] },
                    "value": { "type": ["string", "null"] },
                    "error": { "type": "string" }
                }
            }
        },
        "ids_insertados": {
            "type": "array",
            "items": { "type": "integer" }
        },
        "mensaje": {
            "type": "string",
            "default": ""
        }
    }
}
```

---

## 5. Esquemas de Error

> Todos los errores siguen un formato estandarizado definido en `core/exceptions.py`.

### 5.1 Formato Estándar de Error

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `success` | `boolean` | Siempre `false` en errores |
| `message` | `string` | Mensaje descriptivo del error |
| `status_code` | `integer` | Código HTTP del error |
| `timestamp` | `string (date-time)` | Marca temporal ISO 8601 (UTC) |
| `details` | `object\|null` | Detalles adicionales (opcional) |

**Esquema JSON:**
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "ErrorResponse",
    "type": "object",
    "required": ["success", "message", "status_code", "timestamp"],
    "properties": {
        "success": {
            "type": "boolean",
            "enum": [false]
        },
        "message": {
            "type": "string",
            "description": "Mensaje descriptivo del error"
        },
        "status_code": {
            "type": "integer",
            "description": "Código HTTP del error"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "Marca temporal ISO 8601 (UTC)"
        },
        "details": {
            "type": ["object", "null"],
            "description": "Detalles adicionales del error"
        }
    }
}
```

---

### 5.2 Error 401 — No Autorizado

> Causas: token JWT faltante, inválido, expirado o usuario no existe en BD.

**Ejemplo:**
```json
{
    "success": false,
    "message": "No se pudieron validar las credenciales",
    "status_code": 401,
    "timestamp": "2026-07-13T10:30:00Z"
}
```

> 📌 El header de respuesta incluye: `WWW-Authenticate: Bearer`

---

### 5.3 Error 403 — Acceso Prohibido

> Causas: usuario autenticado sin permisos suficientes (rol `user` intentando acceder a endpoints de admin) o usuario inactivo.

**Ejemplo (rol insuficiente):**
```json
{
    "success": false,
    "message": "No tienes permisos para realizar esta acción",
    "status_code": 403,
    "timestamp": "2026-07-13T10:30:00Z"
}
```

**Ejemplo (usuario inactivo):**
```json
{
    "success": false,
    "message": "Usuario inactivo. Contacta al administrador.",
    "status_code": 403,
    "timestamp": "2026-07-13T10:30:00Z"
}
```

---

### 5.4 Error 404 — Recurso No Encontrado

> Causas: ID de paciente o usuario no existe en la base de datos.

**Ejemplo:**
```json
{
    "success": false,
    "message": "Paciente no encontrado",
    "status_code": 404,
    "timestamp": "2026-07-13T10:30:00Z"
}
```

---

### 5.5 Error 409 — Conflicto

> Causas: username o correo ya existe (usuarios), número de documento ya existe (pacientes).

**Ejemplo:**
```json
{
    "success": false,
    "message": "Ya existe un usuario con ese username o correo",
    "status_code": 409,
    "timestamp": "2026-07-13T10:30:00Z"
}
```

---

### 5.6 Error 422 — Error de Validación

> Causas: campos faltantes, tipos incorrectos, validaciones de Pydantic fallidas.

**Ejemplo:**
```json
{
    "success": false,
    "message": "Error de validación de datos",
    "status_code": 422,
    "timestamp": "2026-07-13T10:30:00Z",
    "details": {
        "errors": [
            {
                "type": "value_error",
                "loc": ["body", "rol"],
                "msg": "El rol debe ser 'admin' o 'user'",
                "input": "superadmin",
                "url": "https://errors.pydantic.dev/2.0/v/value_error"
            }
        ]
    }
}
```

---

### 5.7 Error 500 — Error Interno del Servidor

> Causas: excepción no controlada en el servidor.

**Ejemplo (entorno desarrollo):**
```json
{
    "success": false,
    "message": "Error interno del servidor",
    "status_code": 500,
    "timestamp": "2026-07-13T10:30:00Z",
    "details": {
        "error": "Connection refused"
    }
}
```

> 🔒 En **producción** el campo `details` se omite por seguridad.

---

## 6. Resumen de Endpoints

### Endpoints Públicos

| Método | Endpoint | Body Request | Body Response | Errores |
|--------|----------|---------------|---------------|---------|
| GET | `/health` | — | `{"status": "ok"}` | — |
| POST | `/api/v1/auth/login` | form-data: `username`, `password` | `Token` | 401 |
| POST | `/api/v1/auth/login/json` | `LoginRequest` | `Token` | 401, 422 |

### Endpoints Autenticados (cualquier rol)

| Método | Endpoint | Body Request | Body Response | Errores |
|--------|----------|---------------|---------------|---------|
| GET | `/api/v1/auth/me` | — | `UserResponse` | 401 |
| GET | `/api/v1/pacientes` | — | `PatientResponse[]` | 401 |
| GET | `/api/v1/pacientes/search` | — | `PatientResponse[]` | 401, 422 |
| GET | `/api/v1/pacientes/count` | — | `{"total": int}` | 401 |
| GET | `/api/v1/pacientes/{id}` | — | `PatientResponse` | 401, 404 |
| POST | `/api/v1/pacientes` | `PatientCreate` | `PatientResponse` (201) | 401, 409, 422 |
| PUT | `/api/v1/pacientes/{id}` | `PatientUpdate` | `PatientResponse` | 401, 404, 409, 422 |

### Endpoints Solo Admin

| Método | Endpoint | Body Request | Body Response | Errores |
|--------|----------|---------------|---------------|---------|
| DELETE | `/api/v1/pacientes/{id}` | — | — (204) | 401, 403, 404 |
| POST | `/api/v1/pacientes/importar` | multipart: `file` | `ImportResult` | 401, 403, 422 |
| GET | `/api/v1/users` | — | `UserResponse[]` | 401, 403 |
| GET | `/api/v1/users/{id}` | — | `UserResponse` | 401, 403, 404 |
| POST | `/api/v1/users` | `UserCreate` | `UserResponse` (201) | 401, 403, 409, 422 |
| PUT | `/api/v1/users/{id}` | `UserUpdate` | `UserResponse` | 401, 403, 404, 409, 422 |
| DELETE | `/api/v1/users/{id}` | — | — (204) | 401, 403, 404 |

---

## 📌 Headers Requeridos

### Endpoints Autenticados

| Header | Valor | Descripción |
|--------|-------|-------------|
| `Authorization` | `Bearer <token_jwt>` | Token JWT obtenido del login |

### Login con form-data (OAuth2)

| Header | Valor |
|--------|-------|
| `Content-Type` | `application/x-www-form-urlencoded` |

### Login con JSON

| Header | Valor |
|--------|-------|
| `Content-Type` | `application/json` |

### Importar Excel

| Header | Valor |
|--------|-------|
| `Content-Type` | `multipart/form-data` |

---

## 📌 Parámetros de Query

| Endpoint | Parámetro | Tipo | Default | Restricciones |
|----------|-----------|------|---------|---------------|
| `GET /pacientes` | `skip` | `integer` | `0` | `>= 0` |
| `GET /pacientes` | `limit` | `integer` | `100` | `1–500` |
| `GET /pacientes/search` | `q` | `string` | — | `min 1 char` (requerido) |
| `GET /pacientes/search` | `skip` | `integer` | `0` | `>= 0` |
| `GET /pacientes/search` | `limit` | `integer` | `100` | `1–500` |
| `GET /users` | `skip` | `integer` | `0` | `>= 0` |
| `GET /users` | `limit` | `integer` | `100` | `1–500` |

---

## 📌 Códigos de Estado HTTP

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `200` | OK | Operación exitosa |
| `201` | Created | Recurso creado exitosamente |
| `204` | No Content | Recurso eliminado (sin body de respuesta) |
| `401` | Unauthorized | Credenciales inválidas o token faltante/expirado |
| `403` | Forbidden | Sin permisos suficientes (rol insuficiente o usuario inactivo) |
| `404` | Not Found | Recurso no encontrado |
| `409` | Conflict | Conflicto de unicidad (username, correo o documento duplicado) |
| `422` | Unprocessable Entity | Error de validación de datos |
| `500` | Internal Server Error | Error no controlado del servidor |

---

> ✅ **Fin del documento** — Todos los esquemas JSON de la Fase 3.6 (JWT + RBAC) documentados.
