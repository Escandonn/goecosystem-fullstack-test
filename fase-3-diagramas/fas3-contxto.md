La Fase 2 ya deja el backend funcional y probado. Para la **Fase 3** no empezaría por el frontend. En una prueba técnica, lo más profesional es terminar completamente el backend antes de integrar la interfaz.

La Fase 3 debe enfocarse en la **importación del Excel**, porque ese es uno de los requisitos principales del caso de negocio de Go Ecosystem Digital Health.

---

# Fase 3 — Importación de Pacientes desde Excel

## Objetivo

Implementar un módulo que permita cargar un archivo Excel con pacientes, validar su contenido y almacenarlo en la base de datos evitando registros duplicados.

---

# ¿Por qué esta fase?

En el contexto de Go Ecosystem, las clínicas entregan información inicial en archivos Excel. Este proceso de carga masiva suele ser el primer paso antes de administrar los pacientes desde la aplicación.

Resolver este requerimiento demuestra habilidades en:

* Manipulación de archivos.
* Validación de datos.
* Persistencia en base de datos.
* Manejo de errores.
* Diseño de APIs.

---

# Objetivos de la Fase 3

Al finalizar esta fase se debe tener:

* ✅ Endpoint para subir archivos Excel.
* ✅ Lectura del archivo con Pandas.
* ✅ Validación de columnas.
* ✅ Validación de datos.
* ✅ Inserción masiva.
* ✅ Detección de duplicados.
* ✅ Resumen del proceso.
* ✅ Pruebas en Swagger y Postman.

---

# Flujo General

```text
Usuario

↓

Selecciona pacientes.xlsx

↓

POST /api/v1/pacientes/importar

↓

FastAPI

↓

UploadFile

↓

Pandas

↓

Validaciones

↓

Services

↓

Repository

↓

SQLite

↓

Resumen

↓

JSON
```

---

# Arquitectura

No se agregan nuevas capas.

Simplemente se amplían las existentes.

```text
routes/

patient.py
```

↓

```text
services/

patient_service.py
```

↓

```text
repositories/

patient_repository.py
```

↓

```text
utils/

excel_reader.py
```

---

# Paso 1

Crear la carpeta uploads.

```text
backend/

uploads/
```

Los archivos se almacenarán temporalmente.

---

# Paso 2

Crear utilitario para leer Excel.

```text
utils/

excel_reader.py
```

Responsabilidades:

* abrir archivo;
* leer hoja;
* convertir a DataFrame;
* devolver lista de pacientes.

No debe guardar información en la base de datos.

---

# Paso 3

Instalar dependencias

Ya tenemos:

```bash
pandas
```

```bash
openpyxl
```

No se requieren nuevas librerías.

---

# Paso 4

Crear Schema de respuesta.

Ejemplo:

```text
ImportResult
```

Debe contener:

```text
total_registros

insertados

duplicados

errores
```

---

# Paso 5

Crear Endpoint

```http
POST

/api/v1/pacientes/importar
```

Debe recibir

```text
multipart/form-data
```

con

```text
file
```

---

# Paso 6

Validar archivo.

Aceptar únicamente

```text
.xlsx
```

Si llega

```text
.pdf
```

Debe responder

```http
400 Bad Request
```

---

# Paso 7

Validar columnas

El Excel debe contener exactamente:

```text
TipoDocumento

NumeroDocumento

Nombres

Apellidos

FechaNacimiento

Sexo

Telefono

Correo

Direccion

Estado
```

Si falta una columna

↓

devolver error.

---

# Paso 8

Leer DataFrame

```text
Excel

↓

Pandas

↓

DataFrame

↓

Lista de diccionarios
```

---

# Paso 9

Validar registros

Por cada paciente validar:

* documento obligatorio;
* documento único;
* correo válido;
* teléfono;
* fecha;
* estado.

---

# Paso 10

Detectar duplicados.

Caso:

```text
12345678
```

ya existe.

↓

No insertar.

↓

Agregar al contador de duplicados.

---

# Paso 11

Guardar pacientes.

Los registros válidos

↓

Repository

↓

SQLite

---

# Paso 12

Construir respuesta.

Ejemplo:

```json
{
  "archivo": "pacientes.xlsx",
  "total_registros": 100,
  "insertados": 96,
  "duplicados": 3,
  "errores": 1
}
```

---

# Paso 13

Swagger

Probar

```http
POST

/api/v1/pacientes/importar
```

Subiendo

```text
pacientes.xlsx
```

---

# Paso 14

Postman

Body

↓

form-data

↓

file

↓

Seleccionar Excel

↓

Enviar.

---

# Paso 15

Casos de prueba

## Archivo correcto

Debe importar todos.

---

## Archivo vacío

Debe responder

```json
{
    "detail":"El archivo está vacío"
}
```

---

## Archivo incorrecto

Enviar

```text
foto.jpg
```

↓

Respuesta

400.

---

## Columnas faltantes

Eliminar

```text
Correo
```

↓

Error.

---

## Documento duplicado

Debe insertarse únicamente una vez.

---

# Flujo esperado

```text
Excel

↓

Validación

↓

Lectura

↓

DataFrame

↓

Validación

↓

Duplicados

↓

Guardar

↓

Respuesta
```

---

# Estructura final

```text
backend/

routes/

patient.py

services/

patient_service.py

repositories/

patient_repository.py

schemas/

import_result.py

utils/

excel_reader.py

uploads/
```

---

# Commit recomendado

```bash
git add .

git commit -m "feat: implement patient excel import"
```

---

# Resultado esperado

Al finalizar la Fase 3, el backend no solo ofrecerá un CRUD de pacientes, sino también la capacidad de importar información masiva desde Excel, una funcionalidad alineada con el caso de negocio de Go Ecosystem Digital Health.

## Antes de pasar al frontend

Mi recomendación sería agregar una **Fase 3.5** dedicada a **refinar el backend**, incorporando aspectos como:

* Manejo global de excepciones.
* Logging de la aplicación.
* Configuración centralizada.
* Documentación enriquecida de Swagger.
* Pruebas automatizadas de la API.

Con esto, el backend quedaría listo y robusto antes de comenzar la **Fase 4**, donde se desarrollaría la interfaz con **Astro + React + Tailwind CSS** y se integraría con los endpoints ya implementados. Este orden refleja un flujo de trabajo muy similar al que se sigue en proyectos profesionales.
