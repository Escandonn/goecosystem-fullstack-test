# Fase 4 — Diagrama de Flujo de Autenticación

## Objetivo

Documentar el flujo completo de autenticación JWT desde que el usuario abre la página de login hasta que es redirigido a su dashboard según su rol, incluyendo manejo de errores y cierre de sesión.

---

## Flujo de Login (Happy Path)

```mermaid
flowchart TD
    A[Usuario abre /login] --> B[Astro renderiza login.astro]
    B --> C[React hidrata LoginForm\nclient:load]
    C --> D[Usuario escribe\nusername + password]
    D --> E[Click: Iniciar Sesión]
    E --> F[LoginForm.validate\ncampos no vacíos]
    F -->|validación OK| G[useAuth.login credentials]
    F -->|validación falla| FERR[Mostrar error en campo]
    G --> H[authService.login\nPOST /auth/login/json]
    H --> I[FastAPI recibe JSON\nLoginRequest username, password]
    I --> J[UserService.authenticate\nverifica en SQLite]
    J -->|credenciales válidas| K[UserService.create_token\ngenera JWT HS256]
    J -->|credenciales inválidas| JERR[401 Unauthorized]
    K --> L[Retorna Token\naccess_token, token_type,\nusername, rol]
    L --> M[Frontend guarda token\nlocalStorage goecosystem_token]
    M --> N[authService.getProfile\nGET /auth/me\nBearer token]
    N --> O[FastAPI valida JWT\nget_current_user]
    O --> P[Retorna UserResponse\nid, username, nombre, rol]
    P --> Q[Frontend guarda user\nlocalStorage goecosystem_user]
    Q --> R{user.rol == ADMIN?}
    R -->|Sí| S[window.location.href\n/admin/dashboard]
    R -->|No| T[window.location.href\n/worker/dashboard]
    S --> U[admin/dashboard.astro\nrequireAuth + render]
    T --> V[worker/dashboard.astro\nrequireAuth + render]
```

---

## Flujo de Errores de Login

```mermaid
flowchart TD
    A[POST /auth/login/json] --> B{Código de respuesta}
    B -->|200 OK| C[Login exitoso\ncontinuar flujo]
    B -->|401| D[useAuth: setError\n'Usuario o contraseña incorrectos']
    B -->|422| E[useAuth: setError\n'Datos de entrada inválidos']
    B -->|500| F[useAuth: setError\n'Error del servidor']
    B -->|ERR_NETWORK| G[useAuth: setError\n'No se pudo conectar\ncon el servidor']
    D --> H[Mostrar Alert error\nen LoginForm]
    E --> H
    F --> H
    G --> H
    H --> I[Limpiar token\nlocalStorage.removeItem]
    I --> J[Usuario puede reintentar]
```

---

## Flujo de Protección de Rutas

```mermaid
flowchart TD
    A[Usuario accede a\n/admin/dashboard] --> B[Página .astro carga]
    B --> C[Script: getUser]
    C --> D{¿Token en localStorage?}
    D -->|No| E[window.location.href\n/login]
    D -->|Sí| F[Renderizar dashboard]
    F --> G[Mostrar nombre de usuario\nen navbar]
    F --> H[Botón Cerrar Sesión activo]
    H --> I[Click: logout]
    I --> J[localStorage.removeItem\ntoken + user]
    J --> K[window.location.href\n/login]
```

---

## Flujo del Interceptor de Axios

```mermaid
flowchart LR
    subgraph Request Interceptor
        R1[Cada petición Axios] --> R2{¿Token en localStorage?}
        R2 -->|Sí| R3[Authorization: Bearer token]
        R2 -->|No| R4[Sin header]
        R3 --> R5[Enviar petición]
        R4 --> R5
    end

    subgraph Response Interceptor
        S1[Respuesta recibida] --> S2{¿Status 401?}
        S2 -->|No| S3[Retornar response]
        S2 -->|Sí| S4[limpiar localStorage\ntoken + user]
        S4 --> S5{¿URL actual\nes /login?}
        S5 -->|No| S6[redirect a /login]
        S5 -->|Sí| S7[no redirigir]
    end
```

---

## Flujo de Cierre de Sesión

```mermaid
flowchart TD
    A[Usuario click\nCerrar Sesión] --> B[authUtils.logout]
    B --> C[localStorage.removeItem\ngoecosystem_token]
    C --> D[localStorage.removeItem\ngoecosystem_user]
    D --> E[window.location.href = /login]
    E --> F[Página de login cargada\nsin sesión activa]
```

> **Nota:** El backend JWT es *stateless*, por lo que el logout se realiza únicamente en el frontend eliminando el token del `localStorage`. No hay llamada a un endpoint de logout en el servidor.

---

## Secuencia Completa (Diagrama de Secuencia)

```mermaid
sequenceDiagram
    actor U as Usuario
    participant LF as LoginForm
    participant UA as useAuth
    participant AS as authService
    participant API as Axios Instance
    participant FA as FastAPI
    participant DB as SQLite
    participant LS as localStorage

    U->>LF: Escribe username + password
    U->>LF: Click "Iniciar Sesión"
    LF->>LF: validate() — campos no vacíos
    LF->>UA: login(credentials)
    UA->>AS: authService.login(credentials)
    AS->>API: POST /auth/login/json
    API->>FA: { username, password }
    FA->>DB: SELECT user WHERE username
    DB-->>FA: User record
    FA->>FA: verify_password + create_jwt
    FA-->>API: 200 { access_token, token_type, username, rol }
    API-->>AS: AuthResponse
    AS-->>UA: authResponse
    UA->>LS: setItem(goecosystem_token, access_token)
    UA->>AS: authService.getProfile()
    AS->>API: GET /auth/me
    API->>FA: Authorization: Bearer <token>
    FA->>FA: decode_jwt + get_current_user
    FA-->>API: 200 { id, username, nombre, rol }
    API-->>AS: User
    AS-->>UA: userProfile
    UA->>LS: setItem(goecosystem_user, JSON)
    UA->>UA: evaluar rol
    alt rol == ADMIN
        UA->>U: redirect /admin/dashboard
    else rol != ADMIN
        UA->>U: redirect /worker/dashboard
    end
```

---

## Endpoints Consumidos

| Método | Endpoint | Body / Header | Respuesta | Uso |
|---|---|---|---|---|
| `POST` | `/api/v1/auth/login/json` | `{ "username": "...", "password": "..." }` | `Token { access_token, token_type, username, rol }` | Autenticar y obtener JWT |
| `GET` | `/api/v1/auth/me` | `Authorization: Bearer <token>` | `UserResponse { id, username, nombre, rol }` | Obtener perfil del usuario autenticado |

---

## Casos de Prueba Cubiertos

| # | Caso | Resultado Esperado |
|---|---|---|
| 1 | Login admin (`admin` / `Admin123*`) | Redirect a `/admin/dashboard` |
| 2 | Login trabajador válido | Redirect a `/worker/dashboard` |
| 3 | Usuario inexistente | Alert: "Usuario o contraseña incorrectos" (401) |
| 4 | Contraseña incorrecta | Alert: "Usuario o contraseña incorrectos" (401) |
| 5 | Campos vacíos | Error en campo: "El nombre de usuario es obligatorio" |
| 6 | Acceso directo a `/admin/dashboard` sin token | Redirect a `/login` |
| 7 | Token expirado (401 en cualquier petición) | Interceptor limpia sesión y redirige a `/login` |
| 8 | Cerrar sesión | Limpia `localStorage` y redirige a `/login` |
| 9 | Backend caído | Alert: "No se pudo conectar con el servidor" (ERR_NETWORK) |
