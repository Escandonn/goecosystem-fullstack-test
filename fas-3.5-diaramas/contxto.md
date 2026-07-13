# Fase 3.5 — Hardening del Backend y Buenas Prácticas

## Objetivo

Antes de integrar el frontend, fortalecer el backend implementando buenas prácticas de desarrollo orientadas a aplicaciones empresariales.

En esta fase no se agregan nuevas funcionalidades de negocio; el objetivo es mejorar la calidad del proyecto, su mantenibilidad y la experiencia del desarrollador y de los consumidores de la API.

---

# ¿Por qué esta fase?

Hasta este punto el sistema ya permite administrar pacientes e importar información desde Excel.

Sin embargo, una API profesional también debe ser:

* Robusta frente a errores.
* Fácil de configurar.
* Fácil de mantener.
* Bien documentada.
* Fácil de monitorear.

Estas características son fundamentales en aplicaciones utilizadas por clínicas e instituciones de salud, donde la disponibilidad y la trazabilidad son críticas.

---

# Objetivos

Al finalizar esta fase se debe tener:

* ✅ Manejo global de excepciones.
* ✅ Sistema de logging.
* ✅ Configuración centralizada.
* ✅ Variables de entorno.
* ✅ Documentación Swagger personalizada.
* ✅ Versionado de la API.
* ✅ Respuestas de error consistentes.

---

# Arquitectura

```text
FastAPI

│

├── Middleware

├── Exception Handlers

├── Logger

├── Config

└── Routes
```

Todos estos componentes son transversales y benefician a toda la aplicación.

---

# 1. Configuración Centralizada

## Objetivo

Evitar valores "quemados" dentro del código.

Toda la configuración de la aplicación debe encontrarse en un único lugar.

---

## Archivo

```text
backend/

core/

config.py
```

---

## Responsabilidades

Gestionar:

* Nombre de la aplicación.
* Versión.
* Ambiente.
* URL de la base de datos.
* Carpeta de uploads.
* Tamaño máximo de archivos.
* Configuración de CORS.
* Nivel de logging.

---

## Variables de entorno

Crear:

```text
.env
```

Ejemplo:

```env
APP_NAME=GoEcosystem API

APP_VERSION=1.0.0

ENVIRONMENT=development

DATABASE_URL=sqlite:///./patients.db

UPLOAD_FOLDER=uploads

MAX_UPLOAD_SIZE=10485760

LOG_LEVEL=INFO

API_PREFIX=/api/v1
```

---

## Beneficios

* Separación entre código y configuración.
* Facilidad para cambiar de SQLite a PostgreSQL.
* Configuración diferente para desarrollo y producción.
* Mayor seguridad.

---

# 2. Manejo Global de Excepciones

## Objetivo

Evitar errores internos sin controlar y devolver respuestas uniformes al cliente.

---

## Problema

Sin un manejador global, FastAPI puede devolver mensajes diferentes dependiendo del tipo de excepción.

Esto genera inconsistencias.

---

## Solución

Crear un manejador global de excepciones.

Archivo:

```text
core/

exceptions.py
```

---

## Excepciones a manejar

### 400

Solicitud incorrecta.

---

### 404

Recurso no encontrado.

---

### 409

Conflicto.

Ejemplo:

Documento duplicado.

---

### 422

Errores de validación.

---

### 500

Errores inesperados.

---

## Formato estándar

Todas las respuestas de error deberían seguir la misma estructura.

Ejemplo:

```json
{
    "success": false,
    "message": "Paciente no encontrado",
    "status_code": 404,
    "timestamp": "2026-07-12T09:30:00"
}
```

Esto facilita el consumo desde el frontend.

---

# 3. Sistema de Logging

## Objetivo

Registrar los eventos importantes de la aplicación.

---

## ¿Por qué es importante?

En producción no se utiliza `print()`.

Se utilizan logs para:

* detectar errores;
* auditar procesos;
* monitorear el sistema;
* depurar incidentes.

---

## Archivo

```text
core/

logging.py
```

---

## Eventos recomendados

### INFO

Inicio del servidor.

Conexión a la base de datos.

Importación de Excel.

Paciente creado.

Paciente eliminado.

---

### WARNING

Intento de crear paciente duplicado.

Archivo vacío.

Búsquedas sin resultados.

---

### ERROR

Error de base de datos.

Error leyendo Excel.

Excepciones inesperadas.

---

## Ejemplo de registro

```text
2026-07-12 09:30:15

INFO

Paciente creado

Documento: 123456789
```

---

## Archivo de salida

```text
logs/

app.log
```

Los logs no deben perderse al cerrar el servidor.

---

# 4. Documentación Enriquecida de Swagger

## Objetivo

Mejorar la experiencia del desarrollador que consume la API.

---

## Personalizar

* Título.
* Descripción.
* Versión.
* Contacto.
* Licencia.

---

## Información recomendada

```text
GoEcosystem Digital Health API

Sistema de administración de pacientes.

Versión 1.0

Autor:

Alejandro Escandón
```

---

## Agrupar endpoints

Swagger debe mostrar categorías.

Ejemplo:

```text
Health

Pacientes

Importación
```

---

## Describir cada endpoint

Cada endpoint debe incluir:

* descripción;
* parámetros;
* respuestas;
* códigos HTTP.

---

## Ejemplo

```text
POST

/api/v1/pacientes
```

Descripción

"Crea un nuevo paciente en el sistema."

---

## Ejemplos de respuesta

Swagger debe mostrar ejemplos reales.

Ejemplo:

```json
{
    "id": 1,
    "tipo_documento": "CC",
    "numero_documento": "123456789",
    "nombres": "Juan",
    "apellidos": "Pérez"
}
```

---

# 5. Versionado de la API

## Objetivo

Preparar el sistema para futuras versiones sin romper clientes existentes.

---

## Ruta

```text
/api/v1
```

En el futuro será posible tener:

```text
/api/v2
```

manteniendo compatibilidad.

---

# 6. Middleware

Agregar middleware para registrar:

* tiempo de respuesta;
* método HTTP;
* ruta;
* código de respuesta.

Ejemplo de log:

```text
GET

/api/v1/pacientes

200

18 ms
```

---

# 7. Estructura Esperada

```text
backend/

core/

config.py

exceptions.py

logging.py

database/

models/

repositories/

routes/

schemas/

services/

logs/

app.log

.env
```

---

# Flujo de una petición

```text
Cliente

↓

Middleware

↓

Route

↓

Service

↓

Repository

↓

SQLite

↓

Repository

↓

Service

↓

Route

↓

Exception Handler

↓

Cliente
```

Si ocurre un error en cualquier punto, el manejador global devolverá una respuesta uniforme y el sistema registrará el incidente en los logs.

---

# Beneficios

Al implementar esta fase se obtiene un backend:

* Más mantenible.
* Más fácil de monitorear.
* Más sencillo de configurar.
* Mejor documentado.
* Preparado para producción.
* Más agradable de consumir desde el frontend.

---

# Commit recomendado

```bash
git add .

git commit -m "refactor: improve backend architecture with config logging and exception handling"
```

---

# Resultado Esperado

Al finalizar la Fase 3.5, la API contará con una infraestructura sólida y profesional. Todas las configuraciones estarán centralizadas, los errores serán manejados de forma consistente, los eventos relevantes quedarán registrados mediante logging y la documentación de Swagger ofrecerá una experiencia clara y completa para cualquier desarrollador que consuma la API.

Esta fase deja el backend preparado para iniciar la integración con el frontend en la siguiente etapa del proyecto.
