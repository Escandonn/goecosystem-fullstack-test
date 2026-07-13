# 03 - Diagrama de Usuario (Casos de Uso) — Fase 3.6

## Diagrama de Casos de Uso — Sistema de Autenticación JWT y RBAC

```
═══════════════════════════════════════════════════════════════════════════════════════
                   DIAGRAMA DE CASOS DE USO - FASE 3.6 (JWT + RBAC)
═══════════════════════════════════════════════════════════════════════════════════════

         ┌──────────────────────────────────────────────────────────────────┐
         │                        SISTEMA GOECOSYSTEM                       │
         │                                                                  │
         │   ┌──────────┐                                                  │
         │   │  Iniciar  │◄──────┬─────────────────────────────────────┐    │
         │   │  Sesión   │       │                                     │    │
         │   │  (Login)  │       │                                     │    │
         │   └──────────┘       │                                     │    │
         │                       │                                     │    │
         │   ┌──────────┐        │                                     │    │
         │   │  Obtener │◄───────┤                                     │    │
         │   │ Info User│        │                                     │    │
         │   │ (/me)    │        │                                     │    │
         │   └──────────┘        │                                     │    │
         │                       │                                     │    │
         │   ┌──────────┐        │                                     │    │
         │   │  Listar   │◄───────┤                                     │    │
         │   │ Pacientes │        │                                     │    │
         │   └──────────┘        │                                     │    │
         │                       │                                     │    │
         │   ┌──────────┐        │                                     │    │
         │   │  Buscar   │◄───────┤                                     │    │
         │   │ Pacientes │        │                                     │    │
         │   └──────────┘        │                                     │    │
         │                       │                                     │    │
         │   ┌──────────┐        │                                     │    │
         │   │  Contar   │◄───────┤                                     │    │
         │   │ Pacientes │        │                                     │    │
         │   └──────────┘        │                                     │    │
         │                       │                                     │    │
         │   ┌──────────┐        │                                     │    │
         │   │  Obtener │◄───────┤                                     │    │
         │   │ Paciente  │        │                                     │    │
         │   │  por ID  │        │                                     │    │
         │   └──────────┘        │                                     │    │
         │                       │                                     │    │
         │   ┌──────────┐        │                                     │    │
         │   │  Crear    │◄───────┤                                     │    │
         │   │ Paciente  │        │                                     │    │
         │   └──────────┘        │                                     │    │
         │                       │                                     │    │
         │   ┌──────────┐        │                                     │    │
         │   │ Actualizar│◄───────┤                                     │    │
         │   │ Paciente  │        │                                     │    │
         │   └──────────┘        │                                     │    │
         │                       │                                     │    │
         │   ┌──────────┐        │               ┌──────────┐         │    │
         │   │ Eliminar  │◄───────┤◄──────────────│  Crear    │◄──────┼────┤
         │   │ Paciente  │        │               │  Usuario  │        │    │
         │   └──────────┘        │               └──────────┘         │    │
         │                       │                                     │    │
         │   ┌──────────┐        │               ┌──────────┐         │    │
         │   │ Importar  │◄───────┤◄──────────────│  Listar   │◄──────┼────┤
         │   │  Excel    │        │               │  Usuarios │        │    │
         │   └──────────┘        │               └──────────┘         │    │
         │                       │                                     │    │
         │                       │               ┌──────────┐         │    │
         │                       │◄──────────────│  Obtener  │◄──────┼────┤
         │                       │               │  Usuario  │        │    │
         │                       │               └──────────┘         │    │
         │                       │                                     │    │
         │                       │               ┌──────────┐         │    │
         │                       │◄──────────────│ Actualizar│◄──────┼────┤
         │                       │               │  Usuario  │        │    │
         │                       │               └──────────┘         │    │
         │                       │                                     │    │
         │                       │               ┌──────────┐         │    │
         │                       │◄──────────────│ Eliminar  │◄──────┼────┤
         │                                       │  Usuario  │        │    │
         │                                       └──────────┘         │    │
         └─────────────────────────────────────────────────────────────┘    │
                                                                        │
                          ┌───────────────────┐                          │
                          │   👤 ADMIN         │                          │
                          │  (Rol: admin)      │                          │
                          └───────────────────┘                          │
                                                                        │
                                                                        │
                          ┌───────────────────┐                          │
                          │   👤 TRABAJADOR    │                          │
                          │  (Rol: user)       │                          │
                          └───────────────────┘                          │
                                                                        │
                                                                        │
                          ┌───────────────────┐                          │
                          │   👤 NO AUTENTICADO│                          │
                          │  (Sin sesión)      │                          │
                          └───────────────────┘                          │
                                                                        │
```

---

## Diagrama Simplificado de Roles y Permisos

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          MODELO RBAC — ROLES Y PERMISOS                             │
└─────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────┐
    │                        SISTEMA                                       │
    │                                                                      │
    │   ENDPOINTS PÚBLICOS              ENDPOINTS AUTENTICADOS            │
    │   ┌─────────────────┐            ┌─────────────────────────┐       │
    │   │ GET  /health     │            │ GET  /auth/me            │       │
    │   │ GET  /docs       │            │ GET  /pacientes          │       │
    │   │ GET  /redoc      │            │ GET  /pacientes/search   │       │
    │   │ POST /auth/login │            │ GET  /pacientes/count    │       │
    │   │ POST /auth/login │            │ GET  /pacientes/{id}     │       │
    │   │      /json       │            │ POST /pacientes          │       │
    │   └─────────────────┘            │ PUT  /pacientes/{id}     │       │
    │            ▲                      └────────────┬────────────┘       │
    │            │                                   │                     │
    │            │                      ┌────────────┴────────────┐       │
    │            │                      │                         │       │
    │            │              ENDPOINTS DE ADMIN         ENDPOINTS       │
    │            │              ┌─────────────────┐       DE USUARIO        │
    │            │              │ DELETE /pacientes│      (cualquier       │
    │            │              │   /{id}          │      rol autenticado)│
    │            │              │ POST   /pacientes│                      │
    │            │              │   /importar      │                      │
    │            │              │ GET    /users    │                      │
    │            │              │ GET    /users/{id}│                     │
    │            │              │ POST   /users    │                      │
    │            │              │ PUT    /users/{id}│                     │
    │            │              │ DELETE /users/{id}│                     │
    │            │              └─────────────────┘                      │
    │            │                                   │                     │
    └────────────┼───────────────────────────────────┼─────────────────────┘
                 │                                   │
    ┌────────────┴───────┐                ┌──────────┴──────────┐
    │  👤 NO AUTENTICADO │                │  👤 AUTENTICADO     │
    │                    │                │                      │
    │  Puede:            │                │  ┌────────────────┐ │
    │  ✅ Login           │                │  │  👤 TRABAJADOR  │ │
    │  ✅ Health check    │                │  │  (rol: user)    │ │
    │  ✅ Ver docs        │                │  │                 │ │
    │                    │                │  │  Puede:         │ │
    │  No puede:         │                │  │  ✅ /auth/me    │ │
    │  ❌ Acceder a      │                │  │  ✅ Ver pacientes│ │
    │     pacientes      │                │  │  ✅ Buscar      │ │
    │  ❌ Acceder a      │                │  │  ✅ Contar      │ │
    │     usuarios       │                │  │  ✅ Crear paciente│ │
    │  ❌ Importar Excel │                │  │  ✅ Editar paciente│ │
    │                    │                │  │                 │ │
    └────────────────────┘                │  │  No puede:     │ │
                                          │  │  ❌ Eliminar    │ │
                                          │  │  ❌ Importar    │ │
                                          │  │  ❌ Gestionar   │ │
                                          │  │     usuarios   │ │
                                          │  └────────────────┘ │
                                          │                      │
                                          │  ┌────────────────┐ │
                                          │  │  👤 ADMIN        │ │
                                          │  │  (rol: admin)    │ │
                                          │  │                 │ │
                                          │  │  Puede:         │ │
                                          │  │  ✅ TODO lo de   │ │
                                          │  │     trabajador  │ │
                                          │  │  ✅ Eliminar     │ │
                                          │  │     pacientes   │ │
                                          │  │  ✅ Importar    │ │
                                          │  │     Excel       │ │
                                          │  │  ✅ CRUD usuarios│ │
                                          │  │  ✅ Asignar roles│ │
                                          │  └────────────────┘ │
                                          └──────────────────────┘
```

---

## Tabla de Permisos por Rol

| Acción | No Autenticado | Trabajador (user) | Administrador (admin) |
|--------|:---:|:---:|:---:|
| Login (obtener token) | ✅ | ✅ | ✅ |
| Health check | ✅ | ✅ | ✅ |
| Ver documentación Swagger | ✅ | ✅ | ✅ |
| GET /auth/me | ❌ | ✅ | ✅ |
| Listar pacientes | ❌ | ✅ | ✅ |
| Buscar pacientes | ❌ | ✅ | ✅ |
| Contar pacientes | ❌ | ✅ | ✅ |
| Obtener paciente por ID | ❌ | ✅ | ✅ |
| Crear paciente | ❌ | ✅ | ✅ |
| Actualizar paciente | ❌ | ✅ | ✅ |
| Eliminar paciente | ❌ | ❌ | ✅ |
| Importar Excel | ❌ | ❌ | ✅ |
| Listar usuarios | ❌ | ❌ | ✅ |
| Obtener usuario por ID | ❌ | ❌ | ✅ |
| Crear usuario | ❌ | ❌ | ✅ |
| Actualizar usuario | ❌ | ❌ | ✅ |
| Eliminar usuario | ❌ | ❌ | ✅ |

---

## Casos de Uso Detallados

### CU-01: Iniciar Sesión (Login)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CASO DE USO: Iniciar Sesión                                            │
├─────────────────────────────────────────────────────────────────────────┤
│  Actor: Cualquier usuario (no autenticado)                              │
│  Precondición: El usuario debe estar registrado en el sistema           │
│  Postcondición: Se devuelve un JWT al cliente                          │
│                                                                         │
│  Flujo principal:                                                       │
│  1. El cliente envía POST /api/v1/auth/login                           │
│     con username y password                                             │
│  2. El sistema busca el usuario por username                           │
│  3. El sistema verifica la contraseña con bcrypt                       │
│  4. El sistema genera un JWT con sub, rol y expiración                 │
│  5. El sistema devuelve el token + datos del usuario                   │
│                                                                         │
│  Flujos alternativos:                                                   │
│  - 2a. Usuario no existe → 401 "Credenciales inválidas"               │
│  - 3a. Password incorrecta → 401 "Credenciales inválidas"              │
│  - 3b. Usuario inactivo → 401 "Credenciales inválidas"                 │
└─────────────────────────────────────────────────────────────────────────┘
```

### CU-02: Consultar Información del Usuario Actual

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CASO DE USO: Obtener Info del Usuario Actual (/auth/me)               │
├─────────────────────────────────────────────────────────────────────────┤
│  Actor: Usuario autenticado (cualquier rol)                            │
│  Precondición: El cliente debe enviar un JWT válido                   │
│  Postcondición: Se devuelve la información del usuario                 │
│                                                                         │
│  Flujo principal:                                                       │
│  1. El cliente envía GET /api/v1/auth/me                               │
│     con header Authorization: Bearer <token>                           │
│  2. El sistema decodifica el JWT                                       │
│  3. El sistema busca el usuario por username (sub del token)           │
│  4. El sistema devuelve id, nombre, apellido, correo, username, rol    │
│                                                                         │
│  Flujos alternativos:                                                   │
│  - 2a. Token ausente → 401 "Not authenticated"                        │
│  - 2b. Token inválido/expirado → 401 "Token inválido o expirado"      │
│  - 3a. Usuario no encontrado → 401                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

### CU-03: Gestionar Usuarios (CRUD)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CASO DE USO: Gestionar Usuarios                                       │
├─────────────────────────────────────────────────────────────────────────┤
│  Actor: Administrador (rol: admin)                                     │
│  Precondición: El admin debe estar autenticado con JWT válido          │
│  Postcondición: Se crea/actualiza/elimina un usuario                   │
│                                                                         │
│  Flujo principal — Crear usuario:                                      │
│  1. El admin envía POST /api/v1/users                                 │
│     con nombre, apellido, correo, username, password, rol              │
│  2. El sistema verifica que el username no exista                      │
│  3. El sistema hashea la contraseña con bcrypt                         │
│  4. El sistema crea el usuario en la BD                                │
│  5. El sistema devuelve el usuario creado (201)                       │
│                                                                         │
│  Flujos alternativos:                                                   │
│  - 2a. Username ya existe → 409 Conflict                             │
│  - 2b. Correo ya existe → 409 Conflict                                │
│  - Token no es admin → 403 "No tiene permisos suficientes"            │
│  - Sin token → 401 "Not authenticated"                                │
└─────────────────────────────────────────────────────────────────────────┘
```

### CU-04: Eliminar Paciente (solo Admin)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CASO DE USO: Eliminar Paciente                                        │
├─────────────────────────────────────────────────────────────────────────┤
│  Actor: Administrador (rol: admin)                                     │
│  Precondición: El admin debe estar autenticado con JWT válido          │
│  Postcondición: El paciente se elimina de la BD                       │
│                                                                         │
│  Flujo principal:                                                       │
│  1. El admin envía DELETE /api/v1/pacientes/{id}                      │
│     con header Authorization: Bearer <token>                           │
│  2. El sistema decodifica el JWT y verifica el rol admin               │
│  3. El sistema busca el paciente por ID                                │
│  4. El sistema elimina el paciente                                     │
│  5. El sistema devuelve 204 No Content                                 │
│                                                                         │
│  Flujos alternativos:                                                   │
│  - 2a. Rol no es admin → 403 Forbidden                               │
│  - 3a. Paciente no existe → 404 Not Found                             │
│  - Sin token → 401 Unauthorized                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

### CU-05: Importar Pacientes desde Excel (solo Admin)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CASO DE USO: Importar Excel                                           │
├─────────────────────────────────────────────────────────────────────────┤
│  Actor: Administrador (rol: admin)                                     │
│  Precondición: El admin debe estar autenticado con JWT válido          │
│  Postcondición: Se importan los pacientes del archivo Excel            │
│                                                                         │
│  Flujo principal:                                                       │
│  1. El admin envía POST /api/v1/pacientes/importar                    │
│     con header Authorization: Bearer <token>                           │
│     y un archivo .xlsx en form-data (campo: file)                      │
│  2. El sistema decodifica el JWT y verifica el rol admin               │
│  3. El sistema lee el Excel con ExcelReader (Pandas)                   │
│  4. El sistema valida y normaliza los registros                        │
│  5. El sistema inserta en batch en la BD                               │
│  6. El sistema devuelve ImportResult con métricas                     │
│                                                                         │
│  Flujos alternativos:                                                   │
│  - 2a. Rol no es admin → 403 Forbidden                               │
│  - 3a. Archivo no es .xlsx → 400 Bad Request                          │
│  - 3b. Columnas requeridas faltantes → 400 Bad Request                │
│  - Sin token → 401 Unauthorized                                        │
└─────────────────────────────────────────────────────────────────────────┘
```
