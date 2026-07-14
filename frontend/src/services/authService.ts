import { api } from "./api";
import type { AuthResponse } from "../types/AuthResponse";
import type { User } from "../types/User";
import type { LoginFormData } from "../types/Login";

/**
 * Servicio de autenticación que consume los endpoints reales de FastAPI.
 * No usa datos simulados (mock) ni autenticación local.
 */
export const authService = {
  /**
   * POST /auth/login
   * Envía credenciales como JSON y recibe { access_token, token_type }.
   */
  async login(credentials: LoginFormData): Promise<AuthResponse> {
    // El backend tiene un endpoint específico que acepta JSON:
    // POST /auth/login/json (a diferencia de /auth/login que usa form-data)
    const response = await api.post<AuthResponse>("/auth/login/json", credentials, {
      headers: { "Content-Type": "application/json" },
    });
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
   * No hay endpoint de logout en el backend; el token JWT es stateless.
   */
  logout(): void {
    if (typeof window !== "undefined") {
      localStorage.removeItem("goecosystem_token");
      localStorage.removeItem("goecosystem_user");
    }
  },
};
