
---

# Fase 1 — Diseño de la Arquitectura

## Objetivo

Definir una arquitectura limpia, modular y escalable que permita desarrollar la aplicación de forma organizada, facilitando el mantenimiento, las pruebas y futuras ampliaciones del sistema.

---

# ¿Por qué esta arquitectura?

Para esta prueba se eligió una **arquitectura por capas (Layered Architecture)** con separación de responsabilidades.

No implementaremos una Clean Architecture completa porque, para un CRUD de tamaño pequeño o mediano con un tiempo limitado (4–5 horas), introduciría más complejidad que beneficio.

La arquitectura por capas ofrece un equilibrio entre simplicidad, organización y escalabilidad.

---

# Principios aplicados

Seguiremos principalmente los principios **SOLID** y el principio de **Separation of Concerns (SoC)**.

Cada módulo tendrá una única responsabilidad, reduciendo el acoplamiento y facilitando la reutilización del código.

---

# Arquitectura General

```text
                Cliente (React + Astro)
                        │
                  HTTP / JSON
                        │
                 FastAPI (Routes)
                        │
                    Services
                        │
                Repositories
                        │
                  SQLAlchemy ORM
                        │
                    SQLite DB
```

Cada capa conoce únicamente la capa inmediatamente inferior.

---

# Frontend

Se utilizará **Astro** como framework principal y **React** para los componentes interactivos.

### ¿Por qué Astro?

Porque:

* genera sitios muy rápidos;
* envía menos JavaScript al navegador;
* facilita una buena estructura del proyecto;
* permite integrar React sin problemas;
* mejora el rendimiento inicial.

Para una aplicación administrativa donde la mayor parte del contenido es estático y sólo algunas vistas requieren interacción, Astro es una muy buena elección.

---

# ¿Por qué React?

Porque los formularios, tablas y modales requieren estado.

React facilita:

* reutilización de componentes;
* manejo del estado;
* renderizado dinámico;
* ecosistema maduro.

---

# ¿Por qué Tailwind CSS?

Tailwind permite desarrollar interfaces rápidamente sin escribir grandes archivos CSS.

Ventajas:

* clases reutilizables;
* diseño responsive sencillo;
* consistencia visual;
* menor tiempo de desarrollo.

En una prueba técnica el tiempo es un recurso crítico.

---

# Backend

El backend será desarrollado con **FastAPI**.

### Justificación

FastAPI proporciona:

* alto rendimiento;
* validaciones automáticas mediante Pydantic;
* documentación Swagger integrada;
* tipado fuerte;
* código limpio.

Además es uno de los frameworks modernos más utilizados para APIs REST.

---

# Base de Datos

Se utilizará SQLite.

### Justificación

SQLite no requiere instalación de servidor.

Beneficios:

* configuración inmediata;
* archivo único;
* suficiente para pruebas técnicas;
* integración directa con SQLAlchemy.

En producción podría reemplazarse por PostgreSQL sin modificar la lógica de negocio.

---

# SQLAlchemy

Se utilizará SQLAlchemy como ORM.

¿Por qué?

Porque desacopla la aplicación de la base de datos.

Permite:

* escribir menos SQL;
* relaciones entre tablas;
* migrar fácilmente de SQLite a PostgreSQL.

---

# Pydantic

Toda la validación de datos será realizada mediante Pydantic.

Ventajas:

* validación automática;
* serialización JSON;
* documentación automática.

---

# Axios

Axios será utilizado para consumir la API.

¿Por qué?

Porque facilita:

* interceptores;
* manejo de errores;
* configuración global;
* reutilización.

---

# Organización del Backend

```text
backend/

app/
```

Contendrá el punto de entrada de la aplicación.

---

## models/

Define las entidades SQLAlchemy.

Ejemplo:

Paciente

Usuario

Catálogo

Su responsabilidad es únicamente representar las tablas de la base de datos.

---

## schemas/

Define los modelos Pydantic.

Ejemplo:

PacienteCreate

PacienteUpdate

PacienteResponse

Su objetivo es validar las entradas y salidas de la API.

---

## routes/

Contiene únicamente los endpoints.

Ejemplo:

```python
GET /pacientes

POST /pacientes
```

No debe existir lógica de negocio en esta carpeta.

---

## services/

Aquí vive la lógica de negocio.

Ejemplo:

* crear paciente;
* validar duplicados;
* importar Excel.

Es la capa donde se toman las decisiones del sistema.

---

## repositories/

Gestiona el acceso a la base de datos.

Su responsabilidad es ejecutar consultas mediante SQLAlchemy.

Así evitamos que Services conozca detalles de la persistencia.

---

## database/

Configura:

* conexión;
* sesión;
* motor SQLAlchemy.

---

## utils/

Funciones auxiliares.

Ejemplo:

* lectura de Excel;
* generación de fechas;
* validadores.

---

## uploads/

Almacena temporalmente los archivos Excel.

---

# Organización del Frontend

```text
src/
```

---

## pages/

Define las rutas de Astro.

Ejemplo:

```
/

pacientes

dashboard
```

---

## layouts/

Plantillas compartidas.

Navbar

Sidebar

Footer

---

## components/

Componentes reutilizables.

Ejemplo:

PatientTable

PatientForm

SearchBar

Button

Modal

Loader

Toast

---

## services/

Contendrá las llamadas HTTP.

Ejemplo:

```typescript
PacienteService.ts
```

Toda la comunicación con FastAPI estará centralizada aquí.

---

## hooks/

Hooks personalizados.

Ejemplo:

```
usePatients()

usePagination()
```

---

## types/

Interfaces TypeScript.

Ejemplo:

```typescript
interface Patient
```

---

## utils/

Funciones auxiliares.

---

## styles/

Archivos CSS globales.

---

# Flujo de una petición

```text
Usuario

↓

React

↓

Axios

↓

FastAPI Route

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

React
```

Este flujo mantiene cada capa enfocada en una única responsabilidad y facilita el mantenimiento del código.

---

# Escalabilidad

Aunque la prueba técnica es pequeña, esta arquitectura permite crecer sin reorganizar el proyecto. En el futuro podrían añadirse módulos como:

* Citas médicas.
* Médicos.
* Especialidades.
* Medicamentos.
* Usuarios y roles.
* Autenticación JWT.
* Auditoría.
* Historial clínico.

Cada nuevo módulo seguiría la misma estructura (`models`, `schemas`, `services`, `repositories` y `routes`), manteniendo el proyecto consistente.

---

# ¿Por qué no elegimos otras arquitecturas?

* **MVC tradicional:** mezcla con frecuencia lógica de negocio y acceso a datos, lo que dificulta el mantenimiento en proyectos que crecen.
* **Microservicios:** añaden complejidad innecesaria para una prueba técnica y requieren infraestructura adicional.
* **Clean Architecture completa:** es una excelente opción para proyectos grandes, pero implica crear más capas, interfaces y adaptadores. Para una prueba de pocas horas, ese tiempo se aprovecha mejor implementando funcionalidades y demostrando buenas prácticas con una arquitectura por capas bien organizada.

## Conclusión

La arquitectura seleccionada ofrece un balance entre rapidez de desarrollo, claridad y escalabilidad. Permite demostrar principios de diseño sólidos, separar responsabilidades y construir una base preparada para evolucionar hacia un sistema de gestión clínica más completo sin introducir complejidad innecesaria durante la prueba técnica.
