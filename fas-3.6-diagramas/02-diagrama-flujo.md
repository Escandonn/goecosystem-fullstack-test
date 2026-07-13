# 02 - Diagrama de Flujo — Fase 3.6

## Flujo de Autenticación JWT y Control de Acceso (RBAC)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        FLUJO DE AUTENTICACIÓN JWT + RBAC                            │
└─────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────┐
    │  CLIENTE │
    │(Postman/ │
    │ Frontend)│
    └────┬─────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  1. SOLICITA LOGIN                                                                  │
│                                                                                      │
│     POST /api/v1/auth/login        (form-data)                                       │
│     POST /api/v1/auth/login/json   (JSON body)                                       │
│                                                                                      │
│     Body:                                                                            │
│     ┌──────────────────────────────────────┐                                        │
│     │  username: "admin"                   │                                        │
│     │  password: "Admin123*"               │                                        │
│     └──────────────────────────────────────┘                                        │
└─────────────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  2. ROUTE: auth.py → login_oauth2() / login_json()                                  │
│                                                                                      │
│     Recibe credenciales (username, password)                                        │
│     Llama a UserService.authenticate(username, password)                             │
└───────────────────┬─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  3. SERVICE: UserService.authenticate()                                              │
│                                                                                      │
│     ┌─────────────────────┐                                                         │
│     │ UserRepository      │                                                         │
│     │ .get_by_username()  │─── Busca usuario en BD por username                    │
│     └─────────┬───────────┘                                                         │
│               │                                                                     │
│               ▼                                                                     │
│        ┌──────────────┐     NO        ┌──────────────────────┐                      │
│        │  Usuario     │──────────────▶│  HTTPException(401)  │                      │
│        │  existe?     │               │  "Credenciales       │                      │
│        └──────┬───────┘               │   inválidas"         │                      │
│               │ SI                    └──────────────────────┘                      │
│               ▼                                                                     │
│        ┌──────────────────┐                                                         │
│        │ security.py       │                                                         │
│        │ verify_password() │─── Compara hash bcrypt                                  │
│        └────────┬─────────┘                                                         │
│                 │                                                                   │
│                 ▼                                                                   │
│          ┌──────────────┐     NO        ┌──────────────────────┐                    │
│          │  Password    │──────────────▶│  HTTPException(401)  │                    │
│          │  correcta?   │               │  "Credenciales       │                    │
│          └──────┬───────┘               │   inválidas"         │                    │
│                 │ SI                    └──────────────────────┘                    │
│                 ▼                                                                   │
│          ┌──────────────────┐                                                       │
│          │ Usuario válido    │                                                       │
│          │ (User object)     │                                                       │
│          └────────┬─────────┘                                                       │
└───────────────────┬─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  4. SERVICE: UserService.create_token()                                              │
│                                                                                      │
│     ┌─────────────────────┐                                                         │
│     │ security.py          │                                                         │
│     │ create_access_token()│                                                         │
│     │  ├── Payload:        │                                                         │
│     │  │   sub = username  │                                                         │
│     │  │   rol = user.rol  │                                                         │
│     │  │   exp = +60 min   │                                                         │
│     │  └── Algoritmo: HS256│                                                         │
│     └─────────┬───────────┘                                                         │
│               │                                                                     │
│               ▼                                                                     │
│     ┌─────────────────────┐                                                         │
│     │ JWT Token (string)   │                                                         │
│     │ "eyJhbGciOiJIUzI1..."│                                                         │
│     └─────────┬───────────┘                                                         │
└───────────────────┬─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  5. RESPUESTA: Token JSON                                                            │
│                                                                                      │
│     {                                                                                │
│       "access_token": "eyJhbGciOiJIUzI1NiIs...",                                    │
│       "token_type": "bearer",                                                         │
│       "username": "admin",                                                           │
│       "rol": "admin"                                                                 │
│     }                                                                                │
│                                                                                      │
│     Código: 200 OK                                                                   │
└───────────────────┬─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  6. CLIENTE ALMACENA EL TOKEN                                                        │
│                                                                                      │
│     ┌──────────────────────────────────────┐                                        │
│     │  Guarda access_token en:              │                                        │
│     │  ├── Variable de entorno              │                                        │
│     │  ├── LocalStorage (frontend)         │                                        │
│     │  ├── Postman: Variable de entorno     │                                        │
│     │  └── SessionStorage                   │                                        │
│     └──────────────────────────────────────┘                                        │
└───────────────────┬─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  7. CLIENTE ENVÍA PETICIÓN A ENDPOINT PROTEGIDO                                       │
│                                                                                      │
│     GET /api/v1/pacientes                                                            │
│     Headers:                                                                         │
│       Authorization: Bearer eyJhbGciOiJIUzI1NiIs...                                 │
└───────────────────┬─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  8. FASTAPI: DEPENDENCY INJECTION — get_current_user()                               │
│                                                                                      │
│     ┌─────────────────────────┐                                                     │
│     │ oauth2_scheme            │                                                     │
│     │ Extrae token del header  │                                                     │
│     │ Authorization: Bearer    │                                                     │
│     └───────────┬─────────────┘                                                     │
│                 │                                                                     │
│                 ▼                                                                     │
│     ┌─────────────────────────┐     NO        ┌──────────────────────┐              │
│     │  Token presente?         │─────────────▶│  HTTPException(401)  │              │
│     └───────────┬─────────────┘               │  "Not authenticated" │              │
│                 │ SI                          └──────────────────────┘              │
│                 ▼                                                                     │
│     ┌─────────────────────────┐                                                     │
│     │ security.py              │                                                     │
│     │ decode_access_token()    │                                                     │
│     │  ├── Verifica firma HS256│                                                    │
│     │  ├── Verifica expiración │                                                    │
│     │  └── Extrae payload      │                                                     │
│     └───────────┬─────────────┘                                                     │
│                 │                                                                     │
│                 ▼                                                                     │
│          ┌──────────────┐    ERROR     ┌──────────────────────┐                     │
│          │  Token válido?│─────────────▶│  HTTPException(401)  │                     │
│          └──────┬───────┘              │  "Token inválido o   │                     │
│                 │ OK                   │   expirado"          │                     │
│                 ▼                      └──────────────────────┘                     │
│     ┌─────────────────────────┐                                                     │
│     │ payload["sub"] = username│                                                    │
│     │ payload["rol"] = rol     │                                                    │
│     └───────────┬─────────────┘                                                     │
│                 │                                                                     │
│                 ▼                                                                     │
│     ┌─────────────────────────┐     NO        ┌──────────────────────┐            │
│     │ UserRepository           │─────────────▶│  HTTPException(401)  │            │
│     │ .get_by_username(sub)    │               │  "Usuario no         │            │
│     └───────────┬─────────────┘               │   encontrado"        │            │
│                 │ ENCONTRADO                 └──────────────────────┘            │
│                 ▼                                                                     │
│     ┌─────────────────────────┐                                                     │
│     │ User object              │                                                     │
│     │ (usuario autenticado)    │                                                     │
│     └───────────┬─────────────┘                                                     │
└───────────────────┬─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  9. VERIFICACIÓN DE ROL (si el endpoint requiere RBAC)                               │
│                                                                                      │
│     ┌──────────────────────────────┐                                                │
│     │ require_role(["admin"])       │                                                │
│     │  o require_admin              │                                                │
│     ├──────────────────────────────┤                                                │
│     │  Verifica: user.rol           │                                                │
│     │  in allowed_roles             │                                                │
│     └──────────────┬───────────────┘                                                │
│                    │                                                                 │
│             ┌──────┴──────┐                                                          │
│             │             │                                                          │
│         SI tiene       NO tiene                                                     │
│         permiso        permiso                                                       │
│             │             │                                                          │
│             ▼             ▼                                                          │
│     ┌──────────┐  ┌──────────────────────┐                                          │
│     │ Continúa │  │  HTTPException(403)  │                                          │
│     │ flujo    │  │  "No tiene permisos  │                                          │
│     │ normal   │  │   suficientes"       │                                          │
│     └────┬─────┘  └──────────────────────┘                                          │
│          │                                                                          │
│          ▼                                                                          │
└───────────────────┬─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  10. ROUTE → SERVICE → REPOSITORY → DB                                               │
│                                                                                      │
│     ┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐            │
│     │  Route    │───▶│  Service     │───▶│  Repository │───▶│  SQLite  │            │
│     │ (handler) │    │ (lógica)     │    │ (data access)│    │ (DB)     │            │
│     └──────────┘    └──────────────┘    └──────────────┘    └────┬─────┘            │
│                                                                  │                  │
│                                                                  ▼                  │
│                                                          ┌──────────────┐          │
│                                                          │  Resultados  │          │
│                                                          │  (datos DB)  │          │
│                                                          └──────┬───────┘          │
│                                                                 │                   │
│                                                                 ▼                   │
│     ┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐            │
│     │  Route    │◀───│  Service     │◀───│  Repository │◀───│  Datos   │            │
│     │ (responde)│    │ (procesa)    │    │ (mapea)      │    │          │            │
│     └────┬─────┘    └──────────────┘    └──────────────┘    └──────────┘            │
│          │                                                                          │
└──────────┬───────────────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  11. RESPUESTA AL CLIENTE                                                            │
│                                                                                      │
│     ┌──────────────────────────────────────┐                                        │
│     │  200 OK → Datos solicitados          │                                        │
│     │  201 Created → Recurso creado         │                                        │
│     │  401 Unauthorized → Sin token/inválido│                                       │
│     │  403 Forbidden → Sin permiso de rol  │                                        │
│     │  404 Not Found → Recurso no existe    │                                       │
│     │  409 Conflict → Duplicado             │                                        │
│     │  422 Unprocessable → Datos inválidos │                                        │
│     └──────────────────────────────────────┘                                        │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Flujo de Inicialización — Usuario Admin por Defecto

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    INICIALIZACIÓN DE BASE DE DATOS                                  │
└─────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────┐
    │  STARTUP │
    │  (main)  │
    └────┬─────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  init_db.py                                                                          │
│                                                                                      │
│     ├── Crea tablas (Base.metadata.create_all)                                       │
│     └── Llama a UserService.ensure_admin_exists()                                    │
└───────────────────┬─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  UserService.ensure_admin_exists()                                                   │
│                                                                                      │
│     ┌─────────────────────────┐                                                     │
│     │ UserRepository           │                                                     │
│     │ .get_by_username("admin")│                                                    │
│     └───────────┬─────────────┘                                                     │
│                 │                                                                     │
│         ┌───────┴───────┐                                                             │
│         │               │                                                             │
│     YA EXISTE      NO EXISTE                                                         │
│         │               │                                                             │
│         ▼               ▼                                                             │
│  ┌──────────┐  ┌──────────────────────────────────────────┐                        │
│  │  No hace │  │  Crea usuario admin:                     │                        │
│  │  nada    │  │  ├── nombre: "Admin"                     │                        │
│  │  (skip)  │  │  ├── apellido: "Sistema"                 │                        │
│  └──────────┘  │  ├── correo: "admin@goecosystem.com"     │                        │
│                │  ├── username: "admin"                   │                        │
│                │  ├── password_hash: hash("Admin123*")    │                        │
│                │  ├── rol: "admin"                        │                        │
│                │  └── activo: True                       │                        │
│                └──────────────────────────────────────────┘                        │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Flujo de Errores de Autenticación

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    ERRORES DE AUTENTICACIÓN Y AUTORIZACIÓN                          │
└─────────────────────────────────────────────────────────────────────────────────────┘

  CASO 1: Sin token (401 Unauthorized)
  ─────────────────────────────────────
  Cliente → GET /api/v1/pacientes (sin header Authorization)
       │
       ▼
  oauth2_scheme → No hay token
       │
       ▼
  HTTPException(401)
  {
    "detail": "Not authenticated"
  }

  CASO 2: Token inválido o expirado (401 Unauthorized)
  ──────────────────────────────────────────────────────
  Cliente → GET /api/v1/pacientes
  Authorization: Bearer <token_inválido>
       │
       ▼
  decode_access_token() → JWTError
       │
       ▼
  HTTPException(401)
  {
    "detail": "Token inválido o expirado"
  }

  CASO 3: Token válido pero rol insuficiente (403 Forbidden)
  ──────────────────────────────────────────────────────────
  Cliente (rol=user) → DELETE /api/v1/pacientes/1
  Authorization: Bearer <token_válido>
       │
       ▼
  get_current_user() → User(rol="user")
       │
       ▼
  require_admin → user.rol != "admin"
       │
       ▼
  HTTPException(403)
  {
    "detail": "No tiene permisos suficientes"
  }

  CASO 4: Credenciales incorrectas en login (401 Unauthorized)
  ─────────────────────────────────────────────────────────────
  Cliente → POST /api/v1/auth/login
  username: "admin", password: "incorrecta"
       │
       ▼
  UserService.authenticate() → verify_password() → False
       │
       ▼
  HTTPException(401)
  {
    "detail": "Credenciales inválidas"
  }
```
