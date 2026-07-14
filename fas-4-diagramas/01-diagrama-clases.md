# Fase 4 — Diagrama de Clases

## Objetivo

Documentar las clases, interfaces, tipos y módulos principales del frontend (Astro + React + TypeScript) y su relación con el backend FastAPI durante el flujo de autenticación JWT.

---

## Diagrama de Clases

```mermaid
classDiagram
    direction TB

    %% ──────────────── FRONTEND ────────────────

    class ApiAxios {
        +baseURL: string
        +timeout: number
        +interceptors: Interceptors
    }
    note for ApiAxios "Instancia única de Axios\nbaseURL = http://localhost:8000/api/v1"

    class AuthService {
        +login(credentials: LoginFormData): Promise~AuthResponse~
        +getProfile(): Promise~User~
        +logout(): void
    }
    note for AuthService "consume /auth/login/json\ny /auth/me"

    class UseAuthHook {
        +loading: boolean
        +error: string|null
        +login(credentials: LoginFormData): Promise~boolean~
        +logout(): void
    }
    note for UseAuthHook "Hook de React\ngestiona estado de auth"

    class LoginForm {
        -formData: LoginFormData
        -errors: LoginErrors
        -loading: boolean
        +validate(): boolean
        +handleSubmit(e: FormEvent): void
        +handleChange(e: ChangeEvent): void
    }
    note for LoginForm "Componente React\nclient:load"

    class AuthUtils {
        +getToken(): string|null
        +getUser(): User|null
        +isAuthenticated(): boolean
        +isAdmin(): boolean
        +requireAuth(): void
        +redirectByRole(): void
        +logout(): void
    }
    note for AuthUtils "Usado en páginas .astro\npara proteger rutas"

    class Constants {
        +API_BASE_URL: string
        +STORAGE_KEYS: Record
        +ROUTES: Record
        +ROLES: Record
    }

    %% ──────────────── TIPOS ────────────────

    class LoginFormData {
        +username: string
        +password: string
    }

    class LoginErrors {
        +username?: string
        +password?: string
    }

    class AuthResponse {
        +access_token: string
        +token_type: string
        +username?: string
        +rol?: string
        +expires_in?: number
    }

    class User {
        +id: number
        +username: string
        +nombre: string
        +rol: string
    }

    %% ──────────────── COMPONENTES UI ────────────────

    class Button {
        +variant: "primary"|"secondary"|"danger"
        +loading: boolean
        +disabled: boolean
    }

    class Input {
        +label?: string
        +error?: string
        +name: string
        +type: string
        +value: string
        +onChange: ChangeEvent
    }

    class Alert {
        +type: "error"|"warning"|"info"|"success"
        +message: string
    }

    %% ──────────────── BACKEND ────────────────

    class AuthRouter {
        +POST /auth/login(form_data): Token
        +POST /auth/login_json(credentials): Token
        +GET /auth/me(user): UserResponse
    }

    class UserService {
        +authenticate(username, password): User
        +create_token(user): Token
        +get_by_username(username): User
    }

    class Token {
        +access_token: str
        +token_type: str
        +username: str
        +rol: str
    }

    class LoginRequest {
        +username: str
        +password: str
    }

    class UserResponse {
        +id: int
        +username: str
        +nombre: str
        +rol: str
    }

    %% ──────────────── RELACIONES ────────────────

    LoginForm --> UseAuthHook : usa
    UseAuthHook --> AuthService : llama
    AuthService --> ApiAxios : usa instancia
    ApiAxios --> AuthRouter : HTTP POST/GET
    AuthRouter --> UserService : delega
    UserService --> Token : crea
    AuthRouter --> UserResponse : retorna

    LoginForm --> LoginFormData : estado
    LoginForm --> LoginErrors : validación
    LoginForm --> Button : renderiza
    LoginForm --> Input : renderiza
    LoginForm --> Alert : renderiza

    UseAuthHook --> AuthResponse : recibe
    UseAuthHook --> User : almacena
    AuthUtils --> User : lee de localStorage
    AuthUtils --> Constants : usa

    AuthService --> LoginRequest : envía
    AuthRouter --> LoginRequest : recibe
    AuthRouter --> Token : retorna
```

---

## Descripción de Clases Principales

### Frontend — Capa de Servicios

| Clase / Módulo | Archivo | Responsabilidad |
|---|---|---|
| `ApiAxios` | `services/api.ts` | Instancia única de Axios con `baseURL`, interceptores de petición (Bearer token) y respuesta (401 → redirect) |
| `AuthService` | `services/authService.ts` | Métodos `login()`, `getProfile()`, `logout()` que consumen los endpoints reales del backend |

### Frontend — Capa de Estado (Hooks)

| Clase / Módulo | Archivo | Responsabilidad |
|---|---|---|
| `UseAuthHook` | `hooks/useAuth.ts` | Hook de React que gestiona `loading`, `error`, llama a `authService`, guarda token en `localStorage`, obtiene perfil y redirige por rol |

### Frontend — Componentes UI

| Clase / Módulo | Archivo | Responsabilidad |
|---|---|---|
| `LoginForm` | `components/LoginForm.tsx` | Formulario controlado con validación, dispara `useAuth.login()` |
| `Input` | `components/Input.tsx` | Campo de texto reutilizable con label y error |
| `Button` | `components/Button.tsx` | Botón con variantes y estado `loading` |
| `Alert` | `components/Alert.tsx` | Mensaje de error/advertencia/info/éxito |

### Frontend — Utilidades

| Clase / Módulo | Archivo | Responsabilidad |
|---|---|---|
| `AuthUtils` | `utils/auth.ts` | Funciones para proteger rutas `.astro`: `requireAuth()`, `redirectByRole()`, `logout()`, `isAuthenticated()`, `isAdmin()` |
| `Constants` | `constants/index.ts` | `API_BASE_URL`, `STORAGE_KEYS`, `ROUTES`, `ROLES` |

### Frontend — Tipos TypeScript

| Tipo | Archivo | Campos |
|---|---|---|
| `LoginFormData` | `types/Login.ts` | `username: string`, `password: string` |
| `LoginErrors` | `types/Login.ts` | `username?: string`, `password?: string` |
| `AuthResponse` | `types/AuthResponse.ts` | `access_token`, `token_type`, `username?`, `rol?`, `expires_in?` |
| `User` | `types/User.ts` | `id: number`, `username: string`, `nombre: string`, `rol: string` |

### Backend — FastAPI

| Clase / Módulo | Archivo | Responsabilidad |
|---|---|---|
| `AuthRouter` | `routes/auth.py` | Endpoints `POST /auth/login`, `POST /auth/login/json`, `GET /auth/me` |
| `UserService` | `services/user_service.py` | `authenticate()`, `create_token()`, `get_by_username()` |
| `Token` | `schemas/auth.py` | `access_token: str`, `token_type: str`, `username: str`, `rol: str` |
| `LoginRequest` | `schemas/auth.py` | `username: str`, `password: str` |
| `UserResponse` | `schemas/user.py` | `id`, `username`, `nombre`, `rol` |

---

## Flujo de Dependencias

```text
LoginForm.tsx
  └── useAuth.ts
        └── authService.ts
              └── api.ts (Axios)
                    └── FastAPI /auth/login/json
                    └── FastAPI /auth/me
```

```text
admin/dashboard.astro
  └── utils/auth.ts
        └── constants/index.ts
        └── localStorage (token + user)
```

---

## Almacenamiento de Sesión

| Clave | Valor | Origen |
|---|---|---|
| `goecosystem_token` | JWT (`access_token`) | `POST /auth/login/json` |
| `goecosystem_user` | JSON del usuario | `GET /auth/me` |

Ambos se eliminan al hacer `logout()` o cuando el interceptor recibe un `401`.
