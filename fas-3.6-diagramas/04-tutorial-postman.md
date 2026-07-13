# 🧪 Guía Completa de Pruebas con Postman - Fase 3.6 (JWT + RBAC)

## 🚀 Iniciar el servidor

```powershell
cd "c:\Users\ADMINSTRADOR\Documents\prueba-tecnica\goecosystem-fullstack-test\backend"
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: **http://localhost:8000**

> ⚠️ Al iniciar el servidor por primera vez, se crea automáticamente el usuario administrador por defecto:
> - **Username**: `admin`
> - **Password**: `Admin123*`
> - **Rol**: `admin`

---

## 🌐 Documentación automática

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

> 💡 En Swagger UI puedes usar el botón **Authorize** 🔓 y pegar el token JWT obtenido en el login para probar todos los endpoints protegidos.

---

## 📋 Endpoints disponibles

### Endpoints Públicos (sin autenticación)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/auth/login` | Login con form-data (OAuth2) |
| POST | `/api/v1/auth/login/json` | Login con body JSON |

### Endpoints Autenticados (cualquier rol)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/auth/me` | Obtener perfil del usuario actual |
| GET | `/api/v1/pacientes` | Listar pacientes (paginado) |
| GET | `/api/v1/pacientes/search?q=` | Buscar pacientes |
| GET | `/api/v1/pacientes/count` | Contar pacientes |
| GET | `/api/v1/pacientes/{id}` | Obtener paciente por ID |
| POST | `/api/v1/pacientes` | Crear paciente |
| PUT | `/api/v1/pacientes/{id}` | Actualizar paciente |

### Endpoints Solo Admin (rol: admin)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| DELETE | `/api/v1/pacientes/{id}` | Eliminar paciente |
| POST | `/api/v1/pacientes/importar` | Importar pacientes desde Excel |
| GET | `/api/v1/users` | Listar usuarios |
| GET | `/api/v1/users/{id}` | Obtener usuario por ID |
| POST | `/api/v1/users` | Crear usuario |
| PUT | `/api/v1/users/{id}` | Actualizar usuario |
| DELETE | `/api/v1/users/{id}` | Eliminar usuario |

---

## 📝 Pasos para probar cada endpoint en Postman

---

## 1️⃣ Health Check (público)

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

## 2️⃣ Login con form-data (OAuth2 — compatible con Swagger)

**En Postman:**
- Método: `POST`
- URL: `http://localhost:8000/api/v1/auth/login`
- Headers:
  - `Content-Type`: `application/x-www-form-urlencoded`
- Body: Seleccionar **x-www-form-urlencoded**

**Campos a enviar:**
| Key | Value |
|-----|-------|
| `username` | `admin` |
| `password` | `Admin123*` |

**Respuesta esperada:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbCI6ImFkbWluIiwiZXhwIjoxNzU3OTk5NjAwfQ.signature",
    "token_type": "bearer",
    "username": "admin",
    "rol": "admin"
}
```

**Código de respuesta:** `200 OK`

> 🔑 **Importante**: Copia el valor de `access_token` (sin las comillas). Lo usarás en todos los endpoints protegidos.

---

## 3️⃣ Login con JSON (alternativa)

**En Postman:**
- Método: `POST`
- URL: `http://localhost:8000/api/v1/auth/login/json`
- Headers:
  - `Content-Type`: `application/json`
- Body: Seleccionar **raw** → **JSON**

**JSON a enviar:**
```json
{
    "username": "admin",
    "password": "Admin123*"
}
```

**Respuesta esperada:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "username": "admin",
    "rol": "admin"
}
```

**Código de respuesta:** `200 OK`

---

## 4️⃣ Obtener perfil del usuario actual (/auth/me)

> ⚠️ Requiere token JWT válido

**En Postman:**
- Método: `GET`
- URL: `http://localhost:8000/api/v1/auth/me`
- Headers:
  - `Authorization`: `Bearer <pegar_aqui_el_token>`

**Respuesta esperada:**
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

**Código de respuesta:** `200 OK`

---

## 5️⃣ Listar Pacientes (con autenticación)

**En Postman:**
- Método: `GET`
- URL: `http://localhost:8000/api/v1/pacientes?skip=0&limit=10`
- Headers:
  - `Authorization`: `Bearer <pegar_aqui_el_token>`

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

## 6️⃣ Buscar Pacientes

**En Postman:**
- Método: `GET`
- URL: `http://localhost:8000/api/v1/pacientes/search?q=juan`
- Headers:
  - `Authorization`: `Bearer <pegar_aqui_el_token>`

**Parámetros:**
- `q`: texto de búsqueda (busca en nombres, apellidos y número de documento)

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

## 7️⃣ Contar Pacientes

**En Postman:**
- Método: `GET`
- URL: `http://localhost:8000/api/v1/pacientes/count`
- Headers:
  - `Authorization`: `Bearer <pegar_aqui_el_token>`

**Respuesta esperada:**
```json
{
    "total": 1
}
```

**Código de respuesta:** `200 OK`

---

## 8️⃣ Obtener Paciente por ID

**En Postman:**
- Método: `GET`
- URL: `http://localhost:8000/api/v1/pacientes/1`
- Headers:
  - `Authorization`: `Bearer <pegar_aqui_el_token>`

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

---

## 9️⃣ Crear Paciente

**En Postman:**
- Método: `POST`
- URL: `http://localhost:8000/api/v1/pacientes`
- Headers:
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer <pegar_aqui_el_token>`
- Body: Seleccionar **raw** → **JSON**

**JSON a enviar:**
```json
{
    "tipo_documento": "CC",
    "numero_documento": "98765432",
    "nombres": "María Fernanda",
    "apellidos": "Gómez López",
    "fecha_nacimiento": "1995-08-20",
    "sexo": "F",
    "telefono": "3109876543",
    "correo": "maria.gomez@email.com",
    "direccion": "Carrera 50 #12-34",
    "estado": "Activo"
}
```

**Respuesta esperada (201 Created):**
```json
{
    "id": 2,
    "tipo_documento": "CC",
    "numero_documento": "98765432",
    "nombres": "María Fernanda",
    "apellidos": "Gómez López",
    "fecha_nacimiento": "1995-08-20",
    "sexo": "F",
    "telefono": "3109876543",
    "correo": "maria.gomez@email.com",
    "direccion": "Carrera 50 #12-34",
    "estado": "Activo",
    "fecha_creacion": "2026-07-13T11:00:00",
    "fecha_actualizacion": "2026-07-13T11:00:00"
}
```

**Código de respuesta:** `201 Created`

---

## 🔟 Actualizar Paciente

**En Postman:**
- Método: `PUT`
- URL: `http://localhost:8000/api/v1/pacientes/1`
- Headers:
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer <pegar_aqui_el_token>`
- Body: Seleccionar **raw** → **JSON**

**JSON a enviar (solo los campos a actualizar):**
```json
{
    "telefono": "3201234567",
    "direccion": "Av. Principal #99-01"
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
    "telefono": "3201234567",
    "correo": "juan.perez@email.com",
    "direccion": "Av. Principal #99-01",
    "estado": "Activo",
    "fecha_creacion": "2026-07-11T10:30:00",
    "fecha_actualizacion": "2026-07-13T11:15:00"
}
```

**Código de respuesta:** `200 OK`

---

## 1️⃣1️⃣ Eliminar Paciente (solo Admin)

> ⚠️ Requiere rol `admin`. Un usuario con rol `user` recibirá `403 Forbidden`.

**En Postman:**
- Método: `DELETE`
- URL: `http://localhost:8000/api/v1/pacientes/1`
- Headers:
  - `Authorization`: `Bearer <pegar_aqui_el_token_admin>`

**Respuesta esperada:** _(cuerpo vacío)_

**Código de respuesta:** `204 No Content`

---

## 1️⃣2️⃣ Importar Pacientes desde Excel (solo Admin)

> ⚠️ Requiere rol `admin`.

**En Postman:**
- Método: `POST`
- URL: `http://localhost:8000/api/v1/pacientes/importar`
- Headers:
  - `Authorization`: `Bearer <pegar_aqui_el_token_admin>`
  - _(NO establecer Content-Type manualmente; Postman lo hace automáticamente con form-data)_
- Body: Seleccionar **form-data**

**Campo a enviar:**
| Key | Type | Value |
|-----|------|-------|
| `file` | **File** | _(seleccionar archivo .xlsx del disco)_ |

> 📂 El archivo Excel debe tener las columnas: `TipoDocumento`, `NumeroDocumento`, `Nombres`, `Apellidos`, `FechaNacimiento`, `Sexo`. Opcionales: `Telefono`, `Correo`, `Direccion`, `Estado`.

**Respuesta esperada:**
```json
{
    "total_registros": 10,
    "insertados": 8,
    "duplicados": 1,
    "errores": 1,
    "detalles_errores": [
        {
            "fila": 5,
            "error": "Fecha de nacimiento inválida"
        }
    ]
}
```

**Código de respuesta:** `200 OK`

---

## 1️⃣3️⃣ Listar Usuarios (solo Admin)

**En Postman:**
- Método: `GET`
- URL: `http://localhost:8000/api/v1/users`
- Headers:
  - `Authorization`: `Bearer <pegar_aqui_el_token_admin>`

**Respuesta esperada:**
```json
[
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
]
```

**Código de respuesta:** `200 OK`

---

## 1️⃣4️⃣ Crear Usuario (solo Admin)

**En Postman:**
- Método: `POST`
- URL: `http://localhost:8000/api/v1/users`
- Headers:
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer <pegar_aqui_el_token_admin>`
- Body: Seleccionar **raw** → **JSON**

**JSON a enviar:**
```json
{
    "nombre": "Carlos",
    "apellido": "Rodríguez",
    "correo": "carlos.rodriguez@goecosystem.com",
    "username": "crodriguez",
    "password": "Trabajador123*",
    "rol": "user"
}
```

**Respuesta esperada (201 Created):**
```json
{
    "id": 2,
    "nombre": "Carlos",
    "apellido": "Rodríguez",
    "correo": "carlos.rodriguez@goecosystem.com",
    "username": "crodriguez",
    "rol": "user",
    "activo": true,
    "created_at": "2026-07-13T11:30:00",
    "updated_at": "2026-07-13T11:30:00"
}
```

**Código de respuesta:** `201 Created`

---

## 1️⃣5️⃣ Actualizar Usuario (solo Admin)

**En Postman:**
- Método: `PUT`
- URL: `http://localhost:8000/api/v1/users/2`
- Headers:
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer <pegar_aqui_el_token_admin>`
- Body: Seleccionar **raw** → **JSON**

**JSON a enviar:**
```json
{
    "activo": false,
    "rol": "admin"
}
```

**Respuesta esperada:**
```json
{
    "id": 2,
    "nombre": "Carlos",
    "apellido": "Rodríguez",
    "correo": "carlos.rodriguez@goecosystem.com",
    "username": "crodriguez",
    "rol": "admin",
    "activo": false,
    "created_at": "2026-07-13T11:30:00",
    "updated_at": "2026-07-13T11:45:00"
}
```

**Código de respuesta:** `200 OK`

---

## 1️⃣6️⃣ Eliminar Usuario (solo Admin)

**En Postman:**
- Método: `DELETE`
- URL: `http://localhost:8000/api/v1/users/2`
- Headers:
  - `Authorization`: `Bearer <pegar_aqui_el_token_admin>`

**Respuesta esperada:** _(cuerpo vacío)_

**Código de respuesta:** `204 No Content`

---

## 🧪 Pruebas de Errores y Seguridad

---

## ❌ Caso A: Acceder sin token (401 Unauthorized)

**En Postman:**
- Método: `GET`
- URL: `http://localhost:8000/api/v1/pacientes`
- Headers: _(NO incluir Authorization)_

**Respuesta esperada:**
```json
{
    "detail": "Not authenticated"
}
```

**Código de respuesta:** `401 Unauthorized`

---

## ❌ Caso B: Token inválido o expirado (401 Unauthorized)

**En Postman:**
- Método: `GET`
- URL: `http://localhost:8000/api/v1/pacientes`
- Headers:
  - `Authorization`: `Bearer token_invalido_12345`

**Respuesta esperada:**
```json
{
    "detail": "Token inválido o expirado"
}
```

**Código de respuesta:** `401 Unauthorized`

---

## ❌ Caso C: Credenciales incorrectas en login (401 Unauthorized)

**En Postman:**
- Método: `POST`
- URL: `http://localhost:8000/api/v1/auth/login/json`
- Headers:
  - `Content-Type`: `application/json`
- Body: Seleccionar **raw** → **JSON**

**JSON a enviar:**
```json
{
    "username": "admin",
    "password": "contraseña_incorrecta"
}
```

**Respuesta esperada:**
```json
{
    "detail": "Usuario o contraseña incorrectos"
}
```

**Código de respuesta:** `401 Unauthorized`

---

## ❌ Caso D: Trabajador intenta eliminar paciente (403 Forbidden)

> Primero, inicia sesión con un usuario de rol `user` y usa su token.

**En Postman:**
- Método: `DELETE`
- URL: `http://localhost:8000/api/v1/pacientes/1`
- Headers:
  - `Authorization`: `Bearer <pegar_aqui_el_token_trabajador>`

**Respuesta esperada:**
```json
{
    "detail": "No tiene permisos suficientes"
}
```

**Código de respuesta:** `403 Forbidden`

---

## ❌ Caso E: Trabajador intenta listar usuarios (403 Forbidden)

**En Postman:**
- Método: `GET`
- URL: `http://localhost:8000/api/v1/users`
- Headers:
  - `Authorization`: `Bearer <pegar_aqui_el_token_trabajador>`

**Respuesta esperada:**
```json
{
    "detail": "No tiene permisos suficientes"
}
```

**Código de respuesta:** `403 Forbidden`

---

## ❌ Caso F: Trabajador intenta importar Excel (403 Forbidden)

**En Postman:**
- Método: `POST`
- URL: `http://localhost:8000/api/v1/pacientes/importar`
- Headers:
  - `Authorization`: `Bearer <pegar_aqui_el_token_trabajador>`
- Body: **form-data** con campo `file` (archivo .xlsx)

**Respuesta esperada:**
```json
{
    "detail": "No tiene permisos suficientes"
}
```

**Código de respuesta:** `403 Forbidden`

---

## ❌ Caso G: Crear usuario con username duplicado (409 Conflict)

**En Postman:**
- Método: `POST`
- URL: `http://localhost:8000/api/v1/users`
- Headers:
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer <pegar_aqui_el_token_admin>`
- Body: Seleccionar **raw** → **JSON**

**JSON a enviar:**
```json
{
    "nombre": "Otro",
    "apellido": "Admin",
    "correo": "nuevo@goecosystem.com",
    "username": "admin",
    "password": "OtraClave123*",
    "rol": "user"
}
```

**Respuesta esperada:**
```json
{
    "detail": "El username ya está registrado"
}
```

**Código de respuesta:** `409 Conflict`

---

## ❌ Caso H: Paciente no encontrado (404 Not Found)

**En Postman:**
- Método: `GET`
- URL: `http://localhost:8000/api/v1/pacientes/9999`
- Headers:
  - `Authorization`: `Bearer <pegar_aqui_el_token>`

**Respuesta esperada:**
```json
{
    "detail": "Paciente no encontrado"
}
```

**Código de respuesta:** `404 Not Found`

---

## 📋 Resumen de Códigos de Respuesta

| Código | Significado | Cuándo ocurre |
|--------|-------------|---------------|
| `200 OK` | Petición exitosa | GET, PUT exitoso |
| `201 Created` | Recurso creado | POST de paciente o usuario exitoso |
| `204 No Content` | Recurso eliminado | DELETE exitoso |
| `401 Unauthorized` | No autenticado | Sin token, token inválido o credenciales incorrectas |
| `403 Forbidden` | Sin permisos | Rol insuficiente (ej: user intenta DELETE) |
| `404 Not Found` | Recurso no existe | ID de paciente o usuario no encontrado |
| `409 Conflict` | Conflicto | Username, correo o documento duplicado |
| `422 Unprocessable Entity` | Validación fallida | Body JSON con campos inválidos o faltantes |

---

## 💡 Tips para Postman

1. **Usa Variables de Entorno**: Guarda el token en una variable `{{token}}` para reutilizarlo:
   - Ve a **Environment** → **Add Variable**
   - Nombre: `token`, valor: _(pega el token del login)_
   - En los headers usa: `Bearer {{token}}`

2. **Tests automatizados**: En la pestaña **Tests** del request de login, agrega:
   ```javascript
   pm.test("Login exitoso", function () {
       pm.response.to.have.status(200);
   });
   pm.test("Token recibido", function () {
       const jsonData = pm.response.json();
       pm.expect(jsonData.access_token).to.not.be.null;
       pm.environment.set("token", jsonData.access_token);
   });
   ```
   Esto guarda automáticamente el token en la variable de entorno.

3. **Collection Runner**: Ejecuta toda la colección de pruebas en secuencia con **Runner**.

4. **Importar colección desde Swagger**: Ve a `http://localhost:8000/docs` → clic derecho → **Save as OpenAPI JSON** → Importar en Postman.
