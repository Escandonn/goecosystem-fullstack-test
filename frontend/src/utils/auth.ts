import { STORAGE_KEYS, ROUTES } from "../constants";
import type { User } from "../types/User";

/**
 * Utilidades de autenticación para Astro (sin React).
 * Usadas en las páginas .astro para proteger rutas y redirigir.
 */

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

/**
 * Protege una página .astro: si no hay token, redirige a /login.
 * Llamar dentro de un <script> en la página.
 */
export function requireAuth(): void {
  if (typeof window === "undefined") return;
  if (!isAuthenticated()) {
    window.location.href = ROUTES.LOGIN;
  }
}

/**
 * Redirige según el rol del usuario.
 * admin → /admin/dashboard, cualquier otro → /worker/dashboard
 */
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
