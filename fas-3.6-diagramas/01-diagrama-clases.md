# 01 - Diagrama de Clases UML — Fase 3.6

## Diagrama de Clases del Sistema de Autenticación JWT y RBAC

```
═══════════════════════════════════════════════════════════════════════════════════════
                      DIAGRAMA DE CLASES - FASE 3.6 (JWT + RBAC)
═══════════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              PAQUETE: models                                        │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                              <<class>>                                       │    │
│  │                                User                                           │    │
│  │                          (models/user.py)                                     │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  - __tablename__: str = "users"                                               │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  + id: int (PK, autoincrement)                                                │    │
│  │  + nombre: str                                                                │    │
│  │  + apellido: str                                                              │    │
│  │  + correo: str (unique)                                                       │    │
│  │  + username: str (unique)                                                     │    │
│  │  + password_hash: str                                                         │    │
│  │  + rol: str (default="user")                                                 │    │
│  │  + activo: bool (default=True)                                                │    │
│  │  + created_at: datetime (default=now)                                         │    │
│  │  + updated_at: datetime (onupdate=now)                                       │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                      ▲
                                      │ hereda
                                      │
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              PAQUETE: database                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                              <<class>>                                       │    │
│  │                               Base                                           │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  - declarative_base()                                                       │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              PAQUETE: schemas                                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                              <<class>>                                       │    │
│  │                            UserBase                                           │    │
│  │                        (schemas/user.py)                                      │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  + nombre: str                                                               │    │
│  │  + apellido: str                                                             │    │
│  │  + correo: EmailStr                                                          │    │
│  │  + username: str                                                             │    │
│  │  + rol: str (default="user")                                                 │    │
│  │  + activo: bool (default=True)                                                │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│              ▲                                                                      │
│              │ hereda                                                               │
│              ├──────────────────────────────┬───────────────────────────────────┘   │
│              ▼                              ▼                                       │
│  ┌──────────────────────────────┐  ┌──────────────────────────────────────────┐    │
│  │      <<class>>               │  │      <<class>>                            │    │
│  │    UserCreate                 │  │    UserUpdate                             │    │
│  ├──────────────────────────────┤  ├──────────────────────────────────────────┤    │
│  │  + password: str              │  │  + nombre?: str                           │    │
│  │                               │  │  + apellido?: str                         │    │
│  │  (hereda todo de UserBase)    │  │  + correo?: EmailStr                      │    │
│  │                               │  │  + username?: str                         │    │
│  │                               │  │  + rol?: str                              │    │
│  │                               │  │  + activo?: bool                          │    │
│  │                               │  │  + password?: str                         │    │
│  └──────────────────────────────┘  └──────────────────────────────────────────┘    │
│              │                                                                      │
│              │ hereda                                                               │
│              ▼                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                              <<class>>                                       │    │
│  │                           UserResponse                                       │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  + id: int                                                                   │    │
│  │  + created_at: datetime                                                      │    │
│  │  + updated_at: datetime                                                      │    │
│  │  (hereda todo de UserBase)                                                   │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                              <<class>>                                       │    │
│  │                          LoginRequest                                        │    │
│  │                       (schemas/auth.py)                                       │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  + username: str                                                              │    │
│  │  + password: str                                                              │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                              <<class>>                                       │    │
│  │                              Token                                            │    │
│  │                       (schemas/auth.py)                                       │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  + access_token: str                                                         │    │
│  │  + token_type: str (default="bearer")                                        │    │
│  │  + username: str                                                             │    │
│  │  + rol: str                                                                  │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                              <<class>>                                       │    │
│  │                           TokenData                                           │    │
│  │                       (schemas/auth.py)                                       │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  + sub: Optional[str]                                                         │    │
│  │  + rol: Optional[str]                                                         │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              PAQUETE: repositories                                  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         <<class>>                                            │    │
│  │                    UserRepository                                             │    │
│  │              (repositories/user_repository.py)                               │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  - db: Session                                                               │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  + get_all(skip, limit) → List[User]                                         │    │
│  │  + get_by_id(id) → User | None                                               │    │
│  │  + get_by_username(username) → User | None                                   │    │
│  │  + get_by_correo(correo) → User | None                                       │    │
│  │  + count() → int                                                             │    │
│  │  + create(data) → User                                                        │    │
│  │  + update(user, data) → User                                                 │    │
│  │  + delete(user) → None                                                       │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                      ▲
                                      │ usa
                                      │
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              PAQUETE: services                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         <<class>>                                            │    │
│  │                      UserService                                              │    │
│  │                (services/user_service.py)                                    │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  - repository: UserRepository                                                 │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  + authenticate(username, password) → User | HTTPException(401)              │    │
│  │  + create_token(user) → Token                                                │    │
│  │  + get_all(skip, limit) → List[UserResponse]                                 │    │
│  │  + get_by_id(id) → UserResponse | HTTPException(404)                         │    │
│  │  + create(data) → UserResponse | HTTPException(409)                          │    │
│  │  + update(id, data) → UserResponse | HTTPException(404, 409)                │    │
│  │  + delete(id) → None | HTTPException(404)                                    │    │
│  │  + ensure_admin_exists() → None  (ejecuta al iniciar)                        │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                      ▲
                                      │ usa
                                      │
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              PAQUETE: routes                                        │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         <<class>>                                            │    │
│  │                       auth_router                                             │    │
│  │                    (routes/auth.py)                                           │    │
│  │                    (APIRouter de FastAPI)                                    │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  + POST /auth/login        → login_oauth2()        (form-data)               │    │
│  │  + POST /auth/login/json   → login_json()         (JSON body)               │    │
│  │  + GET  /auth/me           → get_current_user_info()                        │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         <<class>>                                            │    │
│  │                      user_router                                              │    │
│  │                    (routes/user.py)                                           │    │
│  │                    (APIRouter de FastAPI)                                    │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  + GET    /users            → listar_usuarios()     [require_admin]          │    │
│  │  + GET    /users/{id}       → obtener_usuario()    [require_admin]          │    │
│  │  + POST   /users            → crear_usuario()      [require_admin]          │    │
│  │  + PUT    /users/{id}       → actualizar_usuario()  [require_admin]          │    │
│  │  + DELETE /users/{id}       → eliminar_usuario()    [require_admin]          │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         <<class>>                                            │    │
│  │                    patient_router                                             │    │
│  │                    (routes/patient.py)                                        │    │
│  │                    (APIRouter de FastAPI)                                    │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  + GET    /pacientes            → listar_pacientes()    [auth]              │    │
│  │  + GET    /pacientes/search     → buscar_pacientes()    [auth]              │    │
│  │  + GET    /pacientes/count      → contar_pacientes()    [auth]              │    │
│  │  + GET    /pacientes/{id}       → obtener_paciente()    [auth]              │    │
│  │  + POST   /pacientes            → crear_paciente()      [auth]              │    │
│  │  + PUT    /pacientes/{id}       → actualizar_paciente() [auth]              │    │
│  │  + DELETE /pacientes/{id}       → eliminar_paciente()   [require_admin]     │    │
│  │  + POST   /pacientes/importar   → importar_excel()     [require_admin]     │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              PAQUETE: core                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         <<module>>                                           │    │
│  │                       security.py                                             │    │
│  │                    (core/security.py)                                         │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  + hash_password(password: str) → str                                        │    │
│  │      └── Usa passlib + bcrypt                                                │    │
│  │  + verify_password(plain: str, hashed: str) → bool                           │    │
│  │      └── Usa passlib + bcrypt                                                │    │
│  │  + create_access_token(data: dict) → str                                     │    │
│  │      └── Usa python-jose (HS256)                                             │    │
│  │  + decode_access_token(token: str) → dict | JWTError                         │    │
│  │      └── Usa python-jose (HS256)                                             │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              PAQUETE: auth                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         <<module>>                                           │    │
│  │                        jwt.py                                                 │    │
│  │                    (auth/jwt.py)                                              │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  + oauth2_scheme: OAuth2PasswordBearer                                       │    │
│  │      └── tokenUrl = "/api/v1/auth/login"                                     │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         <<module>>                                           │    │
│  │                   dependencies.py                                            │    │
│  │                 (auth/dependencies.py)                                       │    │
│  ├─────────────────────────────────────────────────────────────────────────────┤    │
│  │  + get_current_user(token: str) → User                                       │    │
│  │      ├── decode_access_token(token)                                          │    │
│  │      ├── UserRepository.get_by_username(sub)                                 │    │
│  │      └── HTTPException(401) si inválido                                       │    │
│  │  + require_role(allowed_roles: List[str]) → Callable                          │    │
│  │      └── Verifica rol del usuario actual                                      │    │
│  │  + require_admin → require_role(["admin"])                                   │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## Relaciones entre Clases

```
                    ┌──────────────┐
                    │     Base     │
                    │ (SQLAlchemy) │
                    └──────┬───────┘
                           │ declarative_base()
                           │ crea
                           ▼
                    ┌──────────────┐
                    │     User     │
                    │   (Model)    │
                    └──────┬───────┘
                           │ mapea a
                           ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  UserBase    │◀───│UserResponse │    │   Session    │
│  (Schema)    │    │  (Schema)   │    │ (SQLAlchemy) │
└──────┬───────┘    └─────────────┘    └──────┬───────┘
       ▲            ▲                          │
       │ hereda     │ hereda                   │ usa
       │            │                          ▼
       │            │                  ┌──────────────┐
┌──────┴──────┐     │                  │UserRepository│
│ UserCreate  │     │                  └──────┬───────┘
│  (Schema)   │     │                         │
└─────────────┘     │                         │ usa
                    │                         ▼
┌──────────────┐   │                  ┌──────────────┐
│ UserUpdate   │   │                  │ UserService  │
│  (Schema)    │   │                  └──────┬───────┘
└─────────────┘   │                         │
                    │                         │ usa
                    │                         ▼
┌──────────────┐   │                  ┌──────────────┐
│ LoginRequest │   │                  │ auth_router  │
│  (Schema)    │   │                  │ user_router  │
└─────────────┘   │                  │patient_router│
                    │                  └──────┬───────┘
┌──────────────┐   │                         │
│    Token     │   │                         │ usa
│  (Schema)    │   │                         ▼
└─────────────┘   │                  ┌──────────────┐
                    │                  │ dependencies │
┌──────────────┐   │                  │get_current_user│
│  TokenData   │   │                  │ require_role  │
│  (Schema)    │   │                  │ require_admin  │
└─────────────┘   │                  └──────┬───────┘
                    │                         │
                    │                         │ usa
                    │                         ▼
                    │                  ┌──────────────┐
                    │                  │  security.py │
                    │                  │hash_password │
                    │                  │verify_password│
                    │                  │create_token  │
                    │                  │decode_token   │
                    │                  └──────────────┘
```

## Dependencias de Seguridad — Flujo de Inyección

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FASTAPI DEPENDENCY INJECTION                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Endpoint protegido                                                      │
│  ┌─────────────────────────────────────────────────────┐               │
│  │  @router.get("/pacientes")                          │               │
│  │  def listar(current = Depends(get_current_user)):   │               │
│  └───────────────────┬─────────────────────────────────┘               │
│                      │                                                 │
│                      ▼                                                 │
│  ┌─────────────────────────────────────────────────────┐               │
│  │  get_current_user(token: str = Depends(oauth2_scheme))│              │
│  │  ├── Extrae token del header Authorization: Bearer  │               │
│  │  ├── decode_access_token(token) → payload           │               │
│  │  ├── payload["sub"] → username                       │               │
│  │  ├── UserRepository.get_by_username(username)       │               │
│  │  └── Retorna User o HTTPException(401)               │               │
│  └───────────────────┬─────────────────────────────────┘               │
│                      │                                                 │
│                      ▼                                                 │
│  ┌─────────────────────────────────────────────────────┐               │
│  │  require_role(["admin"])                             │               │
│  │  ├── Llama a get_current_user                        │               │
│  │  ├── Verifica user.rol in allowed_roles              │               │
│  │  └── HTTPException(403) si no tiene permiso          │               │
│  └─────────────────────────────────────────────────────┘               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Tabla de Endpoints y Protección

| Endpoint | Método | Autenticación | Rol Requerido |
|----------|--------|---------------|---------------|
| `/health` | GET | Pública | — |
| `/docs` | GET | Pública | — |
| `/redoc` | GET | Pública | — |
| `/api/v1/auth/login` | POST | Pública | — |
| `/api/v1/auth/login/json` | POST | Pública | — |
| `/api/v1/auth/me` | GET | Requerida | Cualquier rol |
| `/api/v1/users` | GET | Requerida | admin |
| `/api/v1/users/{id}` | GET | Requerida | admin |
| `/api/v1/users` | POST | Requerida | admin |
| `/api/v1/users/{id}` | PUT | Requerida | admin |
| `/api/v1/users/{id}` | DELETE | Requerida | admin |
| `/api/v1/pacientes` | GET | Requerida | Cualquier rol |
| `/api/v1/pacientes/search` | GET | Requerida | Cualquier rol |
| `/api/v1/pacientes/count` | GET | Requerida | Cualquier rol |
| `/api/v1/pacientes/{id}` | GET | Requerida | Cualquier rol |
| `/api/v1/pacientes` | POST | Requerida | Cualquier rol |
| `/api/v1/pacientes/{id}` | PUT | Requerida | Cualquier rol |
| `/api/v1/pacientes/{id}` | DELETE | Requerida | admin |
| `/api/v1/pacientes/importar` | POST | Requerida | admin |
