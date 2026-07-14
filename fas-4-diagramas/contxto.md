Exactamente. De hecho, para que la prueba técnica se vea profesional, **la Fase 4 no debe simular el login**, sino consumir el backend desarrollado en la **Fase 3.6**. El frontend debe conectarse desde el primer momento con la API de FastAPI.

Además, yo haría un pequeño ajuste a la arquitectura: **después del login no llamaría inmediatamente a `/auth/me` si el JWT ya contiene el rol**. Sin embargo, si tu endpoint `/auth/me` devuelve toda la información del usuario (nombre, correo, rol, etc.), es una práctica muy común utilizarlo para mantener el frontend desacoplado del contenido del token.

La Fase 4 la documentaría así:

---

# Fase 4 — Integración Frontend con Backend: Autenticación JWT

## Objetivo

Integrar el frontend desarrollado con **Astro + React + Tailwind CSS** con el backend construido en **FastAPI**, implementando un flujo de autenticación real mediante JWT.

A diferencia de las fases anteriores, en esta etapa **todo el frontend consumirá la API del backend**. No se utilizarán datos simulados (mock) ni autenticación local.

El objetivo es establecer la comunicación entre ambas aplicaciones y preparar la base para los módulos administrativos que se desarrollarán posteriormente.

---

# Objetivos de la Fase 4

Al finalizar esta fase se debe tener:

* ✅ Frontend conectado al backend.
* ✅ Axios configurado.
* ✅ Variables de entorno.
* ✅ Login funcional.
* ✅ Consumo de la API JWT.
* ✅ Almacenamiento del token.
* ✅ Protección de rutas.
* ✅ Redirección según el rol.
* ✅ Cierre de sesión.

---

# Arquitectura General

```text
                    Frontend

        Astro + React + Tailwind

                   │

                Axios

                   │

      http://localhost:8000/api/v1

                   │

                FastAPI

                   │

         JWT Authentication

                   │

              SQLite Database
```

Toda la información será obtenida desde la API.

El frontend nunca accederá directamente a SQLite.

---

# Configuración de Variables de Entorno

El frontend utilizará un archivo:

```text
frontend/

.env
```

Ejemplo:

```env
PUBLIC_API_URL=http://localhost:8000/api/v1
```

De esta forma, la URL del backend podrá cambiar sin modificar el código fuente.

---

# Configuración de Axios

Se creará una instancia única de Axios.

```text
src/

services/

api.ts
```

Responsabilidades:

* URL base.
* Timeout.
* Headers.
* Interceptores.
* JWT automático.

Toda la aplicación utilizará esta instancia.

---

# Flujo de Autenticación

```text
Usuario

↓

Login

↓

Axios

↓

POST /api/v1/auth/login

↓

FastAPI

↓

Validación

↓

JWT

↓

Frontend

↓

Guardar Token

↓

GET /api/v1/auth/me

↓

Obtener Usuario

↓

Redirección
```

---

# Endpoint de Login

```http
POST /api/v1/auth/login
```

Solicitud:

```json
{
    "username":"admin",
    "password":"Admin123*"
}
```

Respuesta:

```json
{
    "access_token":"eyJhbGc...",
    "token_type":"bearer",
    "expires_in":3600
}
```

---

# Obtener Usuario

Después del login exitoso se realizará automáticamente:

```http
GET /api/v1/auth/me
```

Header:

```http
Authorization:

Bearer TOKEN
```

Respuesta esperada:

```json
{
    "id":1,
    "username":"admin",
    "nombre":"Administrador",
    "rol":"ADMIN"
}
```

Esta información será utilizada para controlar la navegación y los permisos del usuario.

---

# Almacenamiento de la Sesión

Una vez autenticado:

* Guardar el JWT.
* Guardar la información básica del usuario.
* Mantener la sesión activa mientras el token sea válido.

El token será enviado automáticamente en todas las peticiones mediante un interceptor de Axios.

---

# Redirección por Rol

## Administrador

Después del login:

```text
/admin/dashboard
```

Página temporal:

```text
Bienvenido Administrador
```

---

## Trabajador

Después del login:

```text
/worker/dashboard
```

Página temporal:

```text
Bienvenido Trabajador
```

---

# Protección de Rutas

Las páginas privadas verificarán:

* existencia del JWT;
* validez del token;
* rol autorizado.

Si el usuario intenta acceder manualmente a una ruta protegida sin autenticarse, será redireccionado al Login.

---

# Comunicación Frontend ↔ Backend

Durante esta fase el frontend ya consumirá el backend para:

* Login.
* Obtener usuario autenticado.
* Validar sesión.
* Cerrar sesión.

No existirán datos simulados.

Toda la información provendrá de FastAPI.

---

# Manejo de Errores

El frontend interpretará las respuestas del backend.

## 401

Credenciales incorrectas.

Mostrar:

```text
Usuario o contraseña incorrectos.
```

---

## 403

Usuario sin permisos.

Mostrar:

```text
No tiene permisos para acceder a este módulo.
```

---

## 500

Error interno.

Mostrar:

```text
Ocurrió un error inesperado.
```

---

# Casos de Prueba

* Login Administrador.
* Login Trabajador.
* Usuario inexistente.
* Contraseña incorrecta.
* Token expirado.
* Acceso directo sin autenticación.
* Cierre de sesión.
* Redirección correcta según el rol.

---

# Estructura Esperada

```text
frontend/

src/

pages/

login.astro

admin/

dashboard.astro

worker/

dashboard.astro

components/

LoginForm.tsx

services/

api.ts

authService.ts

hooks/

useAuth.ts

types/

User.ts

AuthResponse.ts

utils/

auth.ts
```

---

# Commit recomendado

```bash
git add .

git commit -m "feat: integrate frontend authentication with FastAPI backend"
```

---

# Resultado Esperado

Al finalizar la Fase 4, el frontend estará completamente integrado con el backend desarrollado en FastAPI. La autenticación se realizará mediante JWT, todas las solicitudes se enviarán utilizando Axios y el usuario será redirigido automáticamente a la vista correspondiente según su rol. Con esta integración quedará preparada la base para desarrollar en la siguiente fase el Dashboard, el módulo de pacientes y el resto de funcionalidades de la aplicación.

### Recomendación para que el proyecto se vea aún más profesional

Después de esta Fase 4, el siguiente paso no sería empezar el CRUD visual inmediatamente. Haría una **Fase 4.5** de infraestructura del frontend:

* Layout principal (Sidebar + Header + Footer).
* Protección de rutas (Route Guard).
* Context API para autenticación.
* Manejo global del estado del usuario.
* Sistema de notificaciones (Toast).
* Tema claro/oscuro (opcional).

Así, cuando empieces el Dashboard y los módulos de pacientes, ya tendrás una base sólida y reutilizable, muy similar a la arquitectura utilizada en aplicaciones empresariales.
