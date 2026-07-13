"""Punto de entrada de la aplicación FastAPI - GoEcosystem Digital Health API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.exceptions import register_exception_handlers
from core.logging import setup_logging, get_logger
from core.middleware import RequestTimingMiddleware
from database.init_db import init_db
from routes import health, patient

# ── Inicializar logging ─────────────────────────────────────────
setup_logging()
logger = get_logger("main")

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
            "name": "Pacientes",
            "description": "Operaciones CRUD para gestión de pacientes.",
        },
        {
            "name": "Importación",
            "description": "Importación masiva de pacientes desde archivos Excel.",
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
