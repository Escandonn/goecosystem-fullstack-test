
---

# Fase 2 — Diseño del Modelo de Datos y Configuración del Backend

## Objetivo

Construir la base del backend definiendo el modelo de datos, la conexión con la base de datos y la estructura inicial de la API antes de implementar la lógica de negocio.

Esta fase busca asegurar que el sistema tenga una base consistente, mantenible y preparada para crecer con nuevos módulos.

---

# Objetivos de la Fase 2

Al finalizar esta fase se debe tener:

* ✅ Base de datos SQLite configurada.
* ✅ SQLAlchemy configurado.
* ✅ Sesiones de base de datos.
* ✅ Modelos del dominio.
* ✅ Schemas de Pydantic.
* ✅ Configuración mediante variables de entorno.
* ✅ Endpoint `/health`.
* ✅ Documentación Swagger funcionando.
* ✅ Primera versión de la base de datos creada.

---

# ¿Por qué comenzar por el modelo de datos?

En una aplicación de gestión clínica, la información es el núcleo del sistema. Antes de construir interfaces o lógica de negocio, es fundamental definir cómo se almacenarán los datos y cómo se relacionarán entre sí.

Diseñar primero el modelo de datos permite:

* Evitar cambios estructurales posteriores.
* Reducir inconsistencias.
* Facilitar el desarrollo del CRUD.
* Preparar el sistema para futuras funcionalidades como citas, médicos, medicamentos o historias clínicas.

---

# Arquitectura del Backend

```text
Cliente

↓

Routes (FastAPI)

↓

Services

↓

Repositories

↓

Models (SQLAlchemy)

↓

SQLite
```

Cada capa tiene una responsabilidad específica y evita el acoplamiento entre la lógica de negocio y el acceso a datos.

---

# Modelo Entidad-Relación Inicial

Para esta primera versión del sistema se trabajará con una única entidad principal: **Paciente**.

```text
Paciente
────────────────────────────
id (PK)
tipo_documento
numero_documento
nombres
apellidos
fecha_nacimiento
sexo
telefono
correo
direccion
estado
created_at
updated_at
```

---

# Justificación del Modelo

Durante la prueba técnica solo se administrarán pacientes, por lo que no es necesario crear relaciones complejas con otras entidades.

Sin embargo, el modelo está preparado para crecer. En futuras iteraciones podrían añadirse:

```text
Paciente

│

├── Citas

├── Médicos

├── Especialidades

├── Medicamentos

├── Usuarios

└── Historia Clínica
```

Esto demuestra que el diseño considera la evolución natural del sistema.

---

# Organización del Backend

```text
backend/

app/
```

Punto de entrada de la aplicación.

---

## database/

Responsable de la conexión con SQLite.

Contendrá:

* Engine.
* Session.
* Base declarativa.

Responsabilidad:

Centralizar toda la configuración de la base de datos para evitar duplicación de código.

---

## models/

Define la estructura de las tablas mediante SQLAlchemy.

Ejemplo:

```text
Paciente
```

Aquí únicamente se representan las entidades persistentes.

No debe existir lógica de negocio.

---

## schemas/

Define los modelos Pydantic.

Se crearán, por ejemplo:

```text
PacienteCreate

PacienteUpdate

PacienteResponse
```

Estos modelos permiten:

* validar datos de entrada;
* serializar respuestas;
* documentar automáticamente la API.

---

## repositories/

Gestionan el acceso a los datos.

Ejemplo:

```text
PacienteRepository
```

Responsabilidades:

* consultar;
* insertar;
* actualizar;
* eliminar.

La capa superior nunca interactúa directamente con SQLAlchemy.

---

## services/

Contiene la lógica de negocio.

Ejemplo:

* validar duplicados;
* calcular edad si fuera necesario;
* importar pacientes desde Excel;
* aplicar reglas del negocio.

---

## routes/

Contiene únicamente los endpoints HTTP.

Ejemplo:

```text
GET /pacientes

POST /pacientes
```

No debe contener consultas SQL ni reglas de negocio.

---

## utils/

Funciones auxiliares.

Ejemplos:

* lectura de Excel;
* validaciones comunes;
* utilidades de fechas.

---

# Configuración mediante Variables de Entorno

Aunque SQLite requiere poca configuración, es recomendable utilizar un archivo `.env` para mantener la aplicación preparada para otros entornos.

Ejemplo:

```env
DATABASE_URL=sqlite:///./patients.db

APP_NAME=GoEcosystem API

APP_VERSION=1.0.0
```

Beneficios:

* Separación entre código y configuración.
* Facilita migrar a PostgreSQL.
* Mejores prácticas para producción.

---

# Dependencias Adicionales

Además de las instaladas en la Fase 1, se recomienda incorporar:

```bash
pip install python-dotenv
pip install email-validator
```

**Justificación:**

* `python-dotenv` permite cargar variables desde un archivo `.env`.
* `email-validator` mejora las validaciones de correo que utiliza Pydantic.

---

# Documentación Automática

FastAPI generará automáticamente:

```text
/docs
```

(Swagger UI)

y

```text
/redoc
```

Esta documentación permitirá probar la API sin herramientas externas.

---

# Endpoint Inicial

Antes de implementar el CRUD se creará un endpoint de verificación:

```http
GET /health
```

Respuesta esperada:

```json
{
  "status": "ok",
  "service": "GoEcosystem API",
  "version": "1.0.0"
}
```

Este endpoint confirma que la aplicación está funcionando correctamente.

---

# Estructura Esperada al Finalizar la Fase

```text
backend/
│
├── app/
│
├── core/
│   └── config.py
│
├── database/
│   ├── base.py
│   ├── session.py
│   └── init_db.py
│
├── models/
│   └── patient.py
│
├── schemas/
│   └── patient.py
│
├── repositories/
│   └── patient_repository.py
│
├── services/
│   └── patient_service.py
│
├── routes/
│   ├── health.py
│   └── patient.py
│
├── utils/
│
├── uploads/
│
├── main.py
│
├── requirements.txt
│
└── .env
```

---

# Commit recomendado

Una vez completada esta fase:

```bash
git add .

git commit -m "feat: configure database and define patient domain model"
```

---

## ¿Por qué esta secuencia?

En lugar de empezar creando endpoints sin estructura, primero se define la base sobre la que trabajará todo el sistema. Esto reduce retrabajo y facilita que las siguientes fases (CRUD, importación de Excel, autenticación e integración con el frontend) se construyan de forma ordenada y consistente.

### Próxima fase

La **Fase 3** consistirá en implementar el **CRUD completo de pacientes**, conectando las capas `routes`, `services` y `repositories`, incorporando validaciones con Pydantic, manejo de errores y pruebas iniciales desde Swagger antes de integrar el frontend.
