"""Punto de entrada de la aplicación FastAPI - GoEcosystem Digital Health API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from core.config import settings
from core.exceptions import register_exception_handlers
from core.logging import setup_logging, get_logger
from core.middleware import RequestTimingMiddleware
from database.init_db import init_db
from routes import auth, health, patient, user

# ── Inicializar logging ─────────────────────────────────────────
setup_logging()
logger = get_logger("main")

# ── Esquema de seguridad OAuth2 JWT para Swagger ────────────────
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
    scheme_name="JWT",
    description="Introduce tu username y password para obtener un token JWT.",
)

# ── Crear la aplicación FastAPI ──────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    contact={
        "name": settings.APP_CONTACT_NAME,
        "url": settings.APP_CONTACT_URL,
    },
    license_info={
        "name": settings.APP_LICENSE_NAME,
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Health",
            "description": "Endpoints de verificación de salud de la API.",
        },
        {
            "name": "Auth",
            "description": "Autenticación y gestión de tokens JWT.",
        },
        {
            "name": "Pacientes",
            "description": "Operaciones CRUD para gestión de pacientes (requiere autenticación).",
        },
        {
            "name": "Usuarios",
            "description": "Gestión de usuarios del sistema (requiere rol admin).",
        },
        {
            "name": "Importación",
            "description": "Importación masiva de pacientes desde archivos Excel (requiere rol admin).",
        },
    ],
)

# ── Middleware ──────────────────────────────────────────────────
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Timing de requests + request ID
app.add_middleware(RequestTimingMiddleware)

# ── Handlers de excepciones globales ────────────────────────────
register_exception_handlers(app)

# ── Inicializar base de datos al arrancar ───────────────────────
init_db()
logger.info("Base de datos inicializada | url=%s", settings.DATABASE_URL)

# ── Registrar rutas ─────────────────────────────────────────────
app.include_router(health.router)
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(user.router, prefix=settings.API_V1_PREFIX)
app.include_router(patient.router, prefix=settings.API_V1_PREFIX)
logger.info("Rutas registradas | prefix=%s", settings.API_V1_PREFIX)


# ── Endpoint raíz ───────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    """Endpoint raíz con información básica de la API."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "api_prefix": settings.API_V1_PREFIX,
    }
