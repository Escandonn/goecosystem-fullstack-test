Es una muy buena idea. De hecho, **Go Ecosystem** menciona como punto extra la autenticación JWT. Agregar esta fase antes del frontend tiene sentido, porque cuando empieces la interfaz ya tendrás protegidos los endpoints y podrás trabajar con sesiones reales.

A nivel de arquitectura, haría un pequeño cambio: no usaría "Administrador" y "Trabajador" como tipos de usuario directamente, sino un modelo **RBAC (Role-Based Access Control)**. Así el sistema es más escalable y profesional.

---

# Fase 3.6 — Autenticación JWT y Control de Acceso por Roles (RBAC)

## Objetivo

Implementar un sistema de autenticación basado en **JWT (JSON Web Token)** que permita proteger los recursos de la API y controlar el acceso según el rol del usuario.

El sistema diferenciará entre usuarios **Administrador** y **Trabajador**, aplicando permisos específicos para cada uno.

Esta implementación sigue una arquitectura preparada para crecer hacia nuevos roles sin modificar la lógica principal de la aplicación.

---

# ¿Por qué implementar autenticación antes del Frontend?

En aplicaciones empresariales del sector salud, ningún usuario puede acceder directamente a los módulos del sistema.

Todo acceso debe cumplir el siguiente flujo:

```text
Usuario

↓

Login

↓

Validación

↓

JWT

↓

Acceso a recursos
```

Esto garantiza que únicamente usuarios autorizados puedan consultar o modificar información clínica.

---

# Objetivos de la Fase 3.6

Al finalizar esta fase se debe tener:

* ✅ Sistema de autenticación JWT.
* ✅ Hash seguro de contraseñas.
* ✅ Inicio de sesión.
* ✅ Protección de endpoints.
* ✅ Roles de usuario.
* ✅ Middleware de autenticación.
* ✅ Dependencias de seguridad.
* ✅ Documentación Swagger con autenticación.
* ✅ Usuario administrador inicial.

---

# Arquitectura

```text
Cliente

↓

Login

↓

JWT

↓

FastAPI Security

↓

Routes

↓

Services

↓

Repositories

↓

SQLite
```

---

# Modelo de Datos

Se incorpora una nueva entidad al sistema.

```text
Usuario
──────────────────────────────

id

nombre

apellido

correo

username

password_hash

rol

activo

created_at

updated_at
```

El campo **password_hash** almacenará la contraseña cifrada, nunca en texto plano.

---

# Modelo de Roles (RBAC)

Se implementará un modelo basado en roles.

```text
Roles

│

├── Administrador

└── Trabajador
```

Este enfoque facilita agregar nuevos perfiles en el futuro, como Médico, Enfermero o Auditor, sin modificar la arquitectura.

---

# Permisos por Rol

## Administrador

Tiene acceso completo al sistema.

Puede:

* Crear usuarios.
* Crear pacientes.
* Editar pacientes.
* Eliminar pacientes.
* Importar archivos Excel.
* Consultar todos los pacientes.
* Administrar usuarios.
* Acceder al Dashboard.

---

## Trabajador

Acceso limitado a la operación diaria.

Puede:

* Iniciar sesión.
* Consultar pacientes.
* Buscar pacientes.
* Crear pacientes.
* Editar pacientes.

No puede:

* Eliminar pacientes.
* Crear usuarios.
* Importar Excel.
* Cambiar roles.
* Acceder a configuraciones administrativas.

---

# Endpoints de Autenticación

## Login

```http
POST /api/v1/auth/login
```

Recibe:

```json
{
    "username": "admin",
    "password": "123456"
}
```

Respuesta:

```json
{
    "access_token": "...",
    "token_type": "bearer",
    "expires_in": 3600
}
```

---

## Usuario Actual

```http
GET /api/v1/auth/me
```

Devuelve la información del usuario autenticado.

---

## Crear Usuario

```http
POST /api/v1/users
```

Disponible únicamente para el rol Administrador.

---

## Listar Usuarios

```http
GET /api/v1/users
```

Solo Administrador.

---

# Flujo de Autenticación

```text
Usuario

↓

Login

↓

Validación de contraseña

↓

Generación JWT

↓

Cliente almacena token

↓

Authorization: Bearer TOKEN

↓

FastAPI valida token

↓

Permite acceso
```

---

# Protección de Endpoints

Los endpoints públicos serán:

```text
/health

/docs

/redoc

/api/v1/auth/login
```

Todos los demás requerirán autenticación.

---

# Seguridad de Contraseñas

Las contraseñas nunca se almacenarán en texto plano.

Se utilizará hashing seguro mediante algoritmos especializados.

El sistema almacenará únicamente el hash generado, protegiendo la información incluso si la base de datos fuera comprometida.

---

# Dependencias Recomendadas

Instalar:

```bash
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install python-multipart
```

Estas librerías permitirán:

* Generar JWT.
* Verificar JWT.
* Hashear contraseñas.
* Procesar formularios de autenticación.

---

# Organización del Proyecto

Se incorporan nuevos módulos.

```text
backend/

core/

security.py

auth/

jwt.py

dependencies.py

models/

user.py

schemas/

user.py

auth.py

repositories/

user_repository.py

services/

user_service.py

routes/

auth.py

user.py
```

Cada componente mantiene una única responsabilidad.

---

# Swagger con JWT

La documentación incluirá autenticación mediante el botón **Authorize**.

El flujo será:

1. Iniciar sesión mediante `/auth/login`.
2. Copiar el token.
3. Presionar **Authorize**.
4. Pegar el token.
5. Consumir los endpoints protegidos desde Swagger.

---

# Usuario Inicial

Durante la inicialización de la base de datos se creará automáticamente un usuario administrador.

Credenciales de ejemplo:

```text
Usuario:

admin

Contraseña:

Admin123*
```

En un entorno de producción estas credenciales deberán modificarse inmediatamente.

---

# Flujo Completo

```text
Cliente

↓

Login

↓

JWT

↓

Middleware de Seguridad

↓

Verificación de Rol

↓

Route

↓

Service

↓

Repository

↓

SQLite
```

Antes de ejecutar cualquier operación protegida, el sistema verificará la autenticidad del token y los permisos asociados al rol del usuario.

---

# Casos de Prueba

* Inicio de sesión exitoso.
* Credenciales inválidas.
* Token expirado.
* Token inválido.
* Acceso sin token.
* Trabajador intentando eliminar un paciente.
* Administrador creando un usuario.
* Administrador importando un archivo Excel.
* Trabajador consultando pacientes.

---

# Beneficios

Con esta fase el sistema incorpora un esquema de seguridad profesional, permitiendo que cada usuario acceda únicamente a las funcionalidades autorizadas según su rol.

La arquitectura queda preparada para evolucionar hacia un sistema clínico completo con múltiples perfiles y políticas de acceso, alineándose con las necesidades de una plataforma de salud empresarial.

---

# Commit recomendado

```bash
git add .

git commit -m "feat: implement JWT authentication and role-based access control"
```

---

# Resultado Esperado

Al finalizar la Fase 3.6, el backend contará con autenticación mediante JWT, gestión de usuarios y autorización basada en roles. La API estará protegida y preparada para que el frontend implemente un flujo de inicio de sesión seguro y controle la visualización de funcionalidades según el perfil del usuario, siguiendo un enfoque similar al utilizado en aplicaciones empresariales modernas.

