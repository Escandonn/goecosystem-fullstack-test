import { useState, useCallback } from "react";
import { authService } from "../services/authService";
import { STORAGE_KEYS, ROUTES } from "../constants";
import type { LoginFormData } from "../types/Login";
import type { User } from "../types/User";

/**
 * Hook de autenticación para componentes React.
 * Gestiona el estado de login, almacenamiento del token y redirección por rol.
 * Conecta con el backend real de FastAPI (sin mocks).
 */
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
      // Manejar errores del backend
      if (err.response?.status === 401) {
        setError("Usuario o contraseña incorrectos");
      } else if (err.response?.status === 422) {
        setError("Datos de entrada inválidos");
      } else if (err.code === "ERR_NETWORK") {
        setError("No se pudo conectar con el servidor. Verifica que el backend esté activo.");
      } else {
        setError(err.response?.data?.detail ?? "Error al iniciar sesión");
      }
      // Limpiar token si quedó guardado a medias
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
