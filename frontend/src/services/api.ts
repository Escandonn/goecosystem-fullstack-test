import axios from "axios";
import { API_BASE_URL, STORAGE_KEYS, ROUTES } from "../constants";

/**
 * Instancia de Axios configurada para el backend FastAPI.
 * - baseURL: http://localhost:8000/api/v1
 * - Interceptor de petición: inyecta el token JWT en el header Authorization.
 * - Interceptor de respuesta: si llega 401, limpia storage y redirige a /login.
 */
export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 15000,
});

// Interceptor de petición: adjunta el Bearer token si existe.
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

// Interceptor de respuesta: maneja 401 redirigiendo al login.
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
