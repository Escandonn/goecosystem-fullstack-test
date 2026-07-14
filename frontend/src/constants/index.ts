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
