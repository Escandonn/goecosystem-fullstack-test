# Fase 4 — Código Funcional: Clases Principales y Métodos

## Objetivo

Documentar el código funcional real implementado en la Fase 4, mostrando las clases, interfaces, hooks y servicios principales con sus métodos y autenticación JWT.

---

## Índice

1. [Constants — Configuración Global](#1-constants--configuración-global)
2. [Types — Tipos TypeScript](#2-types--tipos-typescript)
3. [api.ts — Instancia de Axios](#3-apits--instancia-de-axios)
4. [authService.ts — Servicio de Autenticación](#4-authservicets--servicio-de-autenticación)
5. [useAuth.ts — Hook de React](#5-useauthts--hook-de-react)
6. [auth.ts — Utilidades para Astro](#6-authts--utilidades-para-astro)
7. [LoginForm.tsx — Componente Principal](#7-loginformtsx--componente-principal)
8. [Componentes UI — Button, Input, Alert](#8-componentes-ui--button-input-alert)
9. [Páginas Astro — Login y Dashboards](#9-páginas-astro--login-y-dashboards)
10. [Backend — Endpoints de Autenticación](#10-backend--endpoints-de-autenticación)

---

## 1. Constants — Configuración Global

**Archivo:** `src/constants/index.ts`

```typescript
export const API_BASE_URL =
  import.meta.env.PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export const STORAGE_KEYS = {
  TOKEN: "goecosystem_token",
  USER: "goecosystem_user",
} as const;

export const ROUTES = {
  LOGIN: "/login",
  ADMIN_DASHBOARD: "/admin/dashboard",
  WORKER_DASHBOARD: "/worker/dashboard",
} as const;

export const ROLES = {
  ADMIN: "ADMIN",
  USER: "USER",
} as const;
```

### Descripción

| Constante | Tipo | Descripción |
|---|---|---|
| `API_BASE_URL` | `string` | URL base del backend FastAPI, leída de `.env` (`PUBLIC_API_URL`) |
| `STORAGE_KEYS` | `const` | Claves de `localStorage` para token y usuario |
| `ROUTES` | `const` | Rutas de la aplicación |
| `ROLES` | `const` | Roles del sistema |

---

## 2. Types — Tipos TypeScript

### `src/types/Login.ts`

```typescript
export interface LoginFormData {
  username: string;
  password: string;
}

export interface LoginErrors {
  username?: string;
  password?: string;
}
```

### `src/types/AuthResponse.ts`

```typescript
export interface AuthResponse {
  access_token: string;
  token_type: string;
  username?: string;
  rol?: string;
  expires_in?: number;
}
```

### `src/types/User.ts`

```typescript
export interface User {
  id: number;
  username: string;
  nombre: string;
  rol: string;
}
```

---

## 3. api.ts — Instancia de Axios

**Archivo:** `src/services/api.ts`

```typescript
import axios from "axios";
import { API_BASE_URL, STORAGE_KEYS, ROUTES } from "../constants";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 15000,
});

// ─── Interceptor de Petición ───
// Inyecta el Bearer token en cada petición si existe en localStorage
api.interceptors.request.use(
  (config) => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ─── Interceptor de Respuesta ───
// Si llega 401, limpia la sesión y redirige al login
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (typeof window !== "undefined" && error.response?.status === 401) {
      localStorage.removeItem(STORAGE_KEYS.TOKEN);
      localStorage.removeItem(STORAGE_KEYS.USER);
      if (window.location.pathname !== ROUTES.LOGIN) {
        window.location.href = ROUTES.LOGIN;
      }
    }
    return Promise.reject(error);
  }
);
```

### Métodos y Interceptores

| Método | Tipo | Descripción |
|---|---|---|
| `api.create(config)` | Factory | Crea la instancia con `baseURL`, `headers`, `timeout` |
| `interceptors.request.use` | Interceptor | Inyecta `Authorization: Bearer <token>` en cada petición |
| `interceptors.response.use` | Interceptor | Captura `401`, limpia `localStorage` y redirige a `/login` |

---

## 4. authService.ts — Servicio de Autenticación

**Archivo:** `src/services/authService.ts`

```typescript
import { api } from "./api";
import type { AuthResponse } from "../types/AuthResponse";
import type { User } from "../types/User";
import type { LoginFormData } from "../types/Login";

export const authService = {
  /**
   * POST /auth/login/json
   * Envía credenciales como JSON y recibe { access_token, token_type, username, rol }.
   */
  async login(credentials: LoginFormData): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>(
      "/auth/login/json",
      credentials,
      { headers: { "Content-Type": "application/json" } }
    );
    return response.data;
  },

  /**
   * GET /auth/me
   * Requiere Bearer token (inyectado por el interceptor de api.ts).
   * Devuelve los datos del usuario autenticado.
   */
  async getProfile(): Promise<User> {
    const response = await api.get<User>("/auth/me");
    return response.data;
  },

  /**
   * Cierra sesión limpiando el almacenamiento local.
   * El JWT es stateless: no hay endpoint de logout en el backend.
   */
  logout(): void {
    if (typeof window !== "undefined") {
      localStorage.removeItem("goecosystem_token");
      localStorage.removeItem("goecosystem_user");
    }
  },
};
```

### Métodos

| Método | Parámetros | Retorna | Endpoint | Descripción |
|---|---|---|---|---|
| `login()` | `LoginFormData { username, password }` | `Promise<AuthResponse>` | `POST /auth/login/json` | Autentica y recibe el JWT |
| `getProfile()` | — | `Promise<User>` | `GET /auth/me` | Obtiene el perfil del usuario autenticado |
| `logout()` | — | `void` | — | Limpia `localStorage` (sin llamada al backend) |

---

## 5. useAuth.ts — Hook de React

**Archivo:** `src/hooks/useAuth.ts`

```typescript
import { useState, useCallback } from "react";
import { authService } from "../services/authService";
import { STORAGE_KEYS, ROUTES } from "../constants";
import type { LoginFormData } from "../types/Login";

export function useAuth() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = useCallback(async (credentials: LoginFormData): Promise<boolean> => {
    setLoading(true);
    setError(null);
    try {
      // 1. Enviar credenciales al backend
      const authResponse = await authService.login(credentials);

      // 2. Guardar token en localStorage
      localStorage.setItem(STORAGE_KEYS.TOKEN, authResponse.access_token);

      // 3. Obtener perfil del usuario con el token recién guardado
      const userProfile = await authService.getProfile();
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userProfile));

      // 4. Redirigir según el rol
      const rol = userProfile.rol?.toUpperCase();
      if (rol === "ADMIN") {
        window.location.href = ROUTES.ADMIN_DASHBOARD;
      } else {
        window.location.href = ROUTES.WORKER_DASHBOARD;
      }

      return true;
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError("Usuario o contraseña incorrectos");
      } else if (err.response?.status === 422) {
        setError("Datos de entrada inválidos");
      } else if (err.code === "ERR_NETWORK") {
        setError("No se pudo conectar con el servidor. Verifica que el backend esté activo.");
      } else {
        setError(err.response?.data?.detail ?? "Error al iniciar sesión");
      }
      localStorage.removeItem(STORAGE_KEYS.TOKEN);
      localStorage.removeItem(STORAGE_KEYS.USER);
      return false;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    authService.logout();
    window.location.href = ROUTES.LOGIN;
  }, []);

  return { login, logout, loading, error, setError };
}
```

### Métodos y Estado

| Miembro | Tipo | Descripción |
|---|---|---|
| `loading` | `boolean` | Indica si la petición de login está en curso |
| `error` | `string \| null` | Mensaje de error para mostrar en la UI |
| `login()` | `(credentials) => Promise<boolean>` | Ejecuta el flujo completo: login → guardar token → getProfile → redirect |
| `logout()` | `() => void` | Limpia sesión y redirige a `/login` |
| `setError()` | `(msg) => void` | Permite limpiar el error desde el componente |

### Manejo de Errores

| HTTP Status | Mensaje mostrado |
|---|---|
| `401` | "Usuario o contraseña incorrectos" |
| `422` | "Datos de entrada inválidos" |
| `ERR_NETWORK` | "No se pudo conectar con el servidor. Verifica que el backend esté activo." |
| Otros | `err.response.data.detail` o "Error al iniciar sesión" |

---

## 6. auth.ts — Utilidades para Astro

**Archivo:** `src/utils/auth.ts`

```typescript
import { STORAGE_KEYS, ROUTES } from "../constants";
import type { User } from "../types/User";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(STORAGE_KEYS.TOKEN);
}

export function getUser(): User | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem(STORAGE_KEYS.USER);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as User;
  } catch {
    return null;
  }
}

export function isAuthenticated(): boolean {
  return getToken() !== null;
}

export function isAdmin(): boolean {
  const user = getUser();
  return user?.rol?.toUpperCase() === "ADMIN";
}

export function logout(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(STORAGE_KEYS.TOKEN);
  localStorage.removeItem(STORAGE_KEYS.USER);
  window.location.href = ROUTES.LOGIN;
}

export function requireAuth(): void {
  if (typeof window === "undefined") return;
  if (!isAuthenticated()) {
    window.location.href = ROUTES.LOGIN;
  }
}

export function redirectByRole(): void {
  if (typeof window === "undefined") return;
  const user = getUser();
  if (!user) return;
  const rol = user.rol?.toUpperCase();
  if (rol === "ADMIN") {
    window.location.href = ROUTES.ADMIN_DASHBOARD;
  } else {
    window.location.href = ROUTES.WORKER_DASHBOARD;
  }
}
```

### Métodos

| Método | Retorna | Descripción |
|---|---|---|
| `getToken()` | `string \| null` | Lee el JWT de `localStorage` |
| `getUser()` | `User \| null` | Lee y parsea el usuario de `localStorage` |
| `isAuthenticated()` | `boolean` | Verifica si hay token |
| `isAdmin()` | `boolean` | Verifica si el rol es `ADMIN` |
| `requireAuth()` | `void` | Redirige a `/login` si no hay token |
| `redirectByRole()` | `void` | Redirige según el rol del usuario |
| `logout()` | `void` | Limpia sesión y redirige a `/login` |

---

## 7. LoginForm.tsx — Componente Principal

**Archivo:** `src/components/LoginForm.tsx`

```typescript
import { useState, type FormEvent } from "react";
import { Button } from "./Button";
import { Input } from "./Input";
import { Alert } from "./Alert";
import { useAuth } from "../hooks/useAuth";
import type { LoginFormData, LoginErrors } from "../types/Login";

export function LoginForm() {
  const { login, loading, error, setError } = useAuth();
  const [formData, setFormData] = useState<LoginFormData>({
    username: "",
    password: "",
  });
  const [errors, setErrors] = useState<LoginErrors>({});

  function validate(): boolean {
    const newErrors: LoginErrors = {};
    if (!formData.username.trim()) {
      newErrors.username = "El nombre de usuario es obligatorio";
    }
    if (!formData.password) {
      newErrors.password = "La contraseña es obligatoria";
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (!validate()) return;
    await login(formData);
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name as keyof LoginErrors]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5" noValidate>
      {error && <Alert type="error" message={error} />}
      <Input label="Usuario" name="username" type="text"
        placeholder="Ingresa tu usuario" value={formData.username}
        onChange={handleChange} error={errors.username} disabled={loading} />
      <Input label="Contraseña" name="password" type="password"
        placeholder="Ingresa tu contraseña" value={formData.password}
        onChange={handleChange} error={errors.password} disabled={loading} />
      <Button type="submit" loading={loading} className="mt-2">
        {loading ? "Iniciando sesión…" : "Iniciar Sesión"}
      </Button>
    </form>
  );
}
```

### Estado y Métodos

| Miembro | Tipo | Descripción |
|---|---|---|
| `formData` | `LoginFormData` | Estado del formulario (`username`, `password`) |
| `errors` | `LoginErrors` | Errores de validación por campo |
| `validate()` | `() => boolean` | Valida que los campos no estén vacíos |
| `handleSubmit()` | `(e: FormEvent) => void` | Previene default, valida y llama `login()` |
| `handleChange()` | `(e: ChangeEvent) => void` | Actualiza `formData` y limpia errores |

---

## 8. Componentes UI — Button, Input, Alert

### Button.tsx

```typescript
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger";
  loading?: boolean;
}
```

| Prop | Tipo | Default | Descripción |
|---|---|---|---|
| `variant` | `"primary" \| "secondary" \| "danger"` | `"primary"` | Color del botón |
| `loading` | `boolean` | `false` | Muestra spinner y deshabilita |
| `disabled` | `boolean` | `false` | Deshabilita el botón |

### Input.tsx

```typescript
interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}
```

| Prop | Tipo | Descripción |
|---|---|---|
| `label` | `string?` | Etiqueta del campo |
| `error` | `string?` | Mensaje de error bajo el campo |
| `name` | `string` | Nombre del campo (para `handleChange`) |
| `type` | `string` | Tipo de input (`text`, `password`, etc.) |

### Alert.tsx

```typescript
interface AlertProps {
  type?: "error" | "warning" | "info" | "success";
  message: string;
}
```

| Prop | Tipo | Default | Descripción |
|---|---|---|---|
| `type` | `"error" \| "warning" \| "info" \| "success"` | `"error"` | Estilo del mensaje |
| `message` | `string` | — | Texto a mostrar |

---

## 9. Páginas Astro — Login y Dashboards

### login.astro

```astro
---
import { LoginForm } from "../components/LoginForm";
import "../styles/global.css";
---
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>Iniciar Sesión — GoEcosystem</title>
  </head>
  <body>
    <div class="min-h-screen flex items-center justify-center ...">
      <div class="w-full max-w-md">
        <!-- Header con logo -->
        <!-- Card -->
        <LoginForm client:load />
      </div>
    </div>
  </body>
</html>
```

> **Directiva `client:load`:** Hidrata el componente React inmediatamente al cargar la página.

### admin/dashboard.astro — Script de Protección

```typescript
import { getUser, logout } from "../../utils/auth";

const user = getUser();
if (!user) {
  window.location.href = "/login";
} else {
  // Mostrar nombre de usuario
  const userEl = document.getElementById("stat-user");
  if (userEl) userEl.textContent = user.nombre || user.username;

  // Botón de logout
  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) logoutBtn.addEventListener("click", logout);
}
```

### worker/dashboard.astro

Misma estructura que `admin/dashboard.astro` pero con badge `TRABAJADOR` y rutas de acciones para trabajadores.

---

## 10. Backend — Endpoints de Autenticación

**Archivo:** `backend/routes/auth.py`

### `POST /auth/login` — OAuth2 (form-urlencoded)

```python
@router.post("/login", response_model=Token, tags=["Auth"])
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = UserService.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise UnauthorizedError("Credenciales incorrectas")
    return UserService.create_token(user)
```

### `POST /auth/login/json` — JSON body (usado por el frontend)

```python
@router.post("/login/json", response_model=Token, tags=["Auth"])
def login_json(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
):
    user = UserService.authenticate(db, credentials.username, credentials.password)
    if not user:
        raise UnauthorizedError("Credenciales incorrectas")
    return UserService.create_token(user)
```

### `GET /auth/me` — Perfil del usuario autenticado

```python
@router.get("/me", response_model=UserResponse, tags=["Auth"])
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### Schemas del Backend

**`backend/schemas/auth.py`**

```python
class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    rol: str

class TokenData(BaseModel):
    username: Optional[str] = None
    rol: Optional[str] = None
```

**`backend/schemas/user.py`**

```python
class UserResponse(BaseModel):
    id: int
    username: str
    nombre: str
    rol: str
```

### UserService — Métodos de Autenticación

**Archivo:** `backend/services/user_service.py`

| Método | Parámetros | Retorna | Descripción |
|---|---|---|---|
| `authenticate(db, username, password)` | `Session, str, str` | `User \| None` | Verifica credenciales contra la base de datos |
| `create_token(user)` | `User` | `Token` | Genera el JWT con `username` y `rol` |
| `get_by_username(db, username)` | `Session, str` | `User \| None` | Busca un usuario por username |

---

## Resumen del Flujo de Autenticación

```text
LoginForm.tsx
  │  validate() → handleSubmit()
  ▼
useAuth.ts
  │  login(credentials)
  ▼
authService.ts
  │  login() → POST /auth/login/json
  │  getProfile() → GET /auth/me
  ▼
api.ts (Axios)
  │  Interceptor request: Bearer token
  │  Interceptor response: 401 → redirect
  ▼
FastAPI (backend)
  │  UserService.authenticate() → SQLite
  │  UserService.create_token() → JWT HS256
  │  get_current_user() → decode JWT
  ▼
localStorage
  │  goecosystem_token = access_token
  │  goecosystem_user = JSON del perfil
  ▼
Redirect
  │  ADMIN → /admin/dashboard
  │  USER  → /worker/dashboard
```

---

## Archivos de la Fase 4

```text
frontend/
├── .env
├── src/
│   ├── components/
│   │   ├── Alert.tsx
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   └── LoginForm.tsx
│   ├── constants/
│   │   └── index.ts
│   ├── hooks/
│   │   └── useAuth.ts
│   ├── pages/
│   │   ├── login.astro
│   │   ├── admin/
│   │   │   └── dashboard.astro
│   │   └── worker/
│   │       └── dashboard.astro
│   ├── services/
│   │   ├── api.ts
│   │   └── authService.ts
│   ├── styles/
│   │   └── global.css
│   ├── types/
│   │   ├── AuthResponse.ts
│   │   ├── Login.ts
│   │   └── User.ts
│   └── utils/
│       └── auth.ts
```
