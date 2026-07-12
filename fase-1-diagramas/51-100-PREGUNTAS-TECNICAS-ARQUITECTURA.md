# 51-100 PREGUNTAS TÉCNICAS - ARQUITECTURA Y STACK (FASE 1)

> **Formato Radar** — Evaluación de Conocimientos Técnicos
> **Basado en:** fase-1-diagramas/
> **Categorías:** Arquitectura, Stack Tecnológico, Estructura, Configuración, Implementación

---

## 📊 RESUMEN VISUAL (RADAR)

```
                    ARQUITECTURA
                        10
                       /    \
                      /      \
                     /   8    \
            ESTRUCTURA -------- STACK
               7            TECNOLÓGICO
               |                 9
               |                 |
               |                 |
            CONFIGURACIÓN ------ IMPLEMENTACIÓN
                    6                 5
```

| Categoría | Puntuación | Preguntas |
|-----------|-------------|-----------|
| **Arquitectura** | 8/10 | 1-10 |
| **Stack Tecnológico** | 9/10 | 11-20 |
| **Estructura del Proyecto** | 7/10 | 21-30 |
| **Configuración** | 6/10 | 31-40 |
| **Implementación** | 5/10 | 41-50 |

---

## 1. ARQUITECTURA (1-10)

### Pregunta 1
**¿Qué es la Arquitectura Limpia (Clean Architecture)?**

a) Un patrón de diseño para bases de datos
b) Una estructura de capas que separa preocupaciones, donde las reglas de negocio son independientes de frameworks
c) Un tipo de arquitectura de microservicios
d) Un método para optimizar consultas SQL

<details>
<summary><b>Respuesta correcta: B</b></summary>

La Arquitectura Limpia, propuesta por Robert C. Martin (Uncle Bob), organiza el código en capas concéntricas donde las reglas de negocio están en el centro y son independientes de detalles técnicos como frameworks o bases de datos.
</details>

---

### Pregunta 2
**¿Qué significa el principio SOLID en desarrollo de software?**

a) Un conjunto de 5 principios para escribir código orientado a objetos de calidad
b) Una metodología ágil de desarrollo
c) Un tipo de base de datos NoSQL
d) Un patrón de diseño para APIs REST

<details>
<summary><b>Respuesta correcta: A</b></summary>

SOLID son 5 principios: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation y Dependency Inversion. Ayudan a crear código más mantenible y testeable.
</details>

---

### Pregunta 3
**¿Qué es el principio de Responsabilidad Única (SRP)?**

a) Cada módulo debe tener una única razón para cambiar
b) Cada clase debe implementar una sola interfaz
c) Cada función debe retornar un solo valor
d) Cada archivo debe contener una sola clase

<details>
<summary><b>Respuesta correcta: A</b></summary>

El SRP establece que una clase o módulo debe tener una sola razón para cambiar, es decir, debe tener una única responsabilidad. Esto facilita el mantenimiento y reduce el acoplamiento.
</details>

---

### Pregunta 4
**¿Qué es Separation of Concerns (SoC)?**

a) Un patrón de base de datos
b) El principio de separar el código en secciones distintas, donde cada una aborda una preocupación específica
c) Un método de autenticación
d) Una técnica de optimización de CSS

<details>
<summary><b>Respuesta correcta: B</b></summary>

SoC es el principio de diseño que separa un programa en secciones distintas, donde cada sección aborda una preocupación (concern) separada. Esto mejora la modularidad y el mantenimiento.
</details>

---

### Pregunta 5
**¿Qué es la Arquitectura por Capas (Layered Architecture)?**

a) Una arquitectura solo para aplicaciones móviles
b) Una estructura donde el código se organiza en capas jerárquicas (presentación, negocio, datos)
c) Un tipo de caché para mejorar rendimiento
d) Un patrón para diseñar interfaces de usuario

<details>
<summary><b>Respuesta correcta: B</b></summary>

La Arquitectura por Capas organiza el código en capas jerárquicas: presentación (UI), aplicación (servicios), dominio (reglas de negocio) e infraestructura (acceso a datos). Cada capa solo conoce a la capa inferior.
</details>

---

### Pregunta 6
**¿Cuál es el flujo de comunicación en una Arquitectura por Capas?**

a) Cualquier capa puede comunicarse con cualquier otra
b) La capa superior interactúa directamente con la base de datos
c) La capa superior se comunica con la inferior, nunca al revés
d) Las capas se comunican de forma aleatoria

<details>
<summary><b>Respuesta correcta: C</b></summary>

En la Arquitectura por Capas, el flujo es unidireccional: la capa superior (routes) se comunica con la capa de servicios, que a su vez se comunica con el repositorio, y este con el modelo. La capa superior nunca interactúa directamente con SQLAlchemy.
</details>

---

### Pregunta 7
**¿Por qué es importante la inversión de dependencias (DIP)?**

a) Permite que las capas superiores dependan de abstracciones, no de implementaciones concretas
b) Elimina la necesidad de bases de datos
c) Aumenta la velocidad de ejecución del código
d) Reduce el tamaño del código fuente

<details>
<summary><b>Respuesta correcta: A</b></summary>

El DIP establece que los módulos de alto nivel no deben depender de módulos de bajo nivel. Ambos deben depender de abstracciones. Esto permite cambiar implementaciones sin afectar otras capas.
</details>

---

### Pregunta 8
**¿Qué ventajas ofrece la Arquitectura Limpia para testing?**

a) No permite testing automático
b) Las reglas de negocio son independientes de frameworks, lo que facilita crear tests unitarios sin dependencias externas
c) Solo permite tests de integración
d) Elimina la necesidad de mocks

<details>
<summary><b>Respuesta correcta: B</b></summary>

Al separar las reglas de negocio de frameworks externos, la Arquitectura Limpia permite escribir tests unitarios que verifican la lógica de negocio sin necesidad de bases de datos, servidores web u otras dependencias.
</details>

---

### Pregunta 9
**¿Qué es el Principio Open/Closed (OCP)?**

a) El código debe estar cerrado para lectura pero abierto para modificación
b) Las entidades de software deben estar abiertas para extensión pero cerradas para modificación
c) Los archivos deben tener permisos de lectura y escritura
d) Las APIs deben estar siempre abiertas sin autenticación

<details>
<summary><b>Respuesta correcta: B</b></summary>

El OCP establece que las entidades de software (clases, módulos, funciones) deben estar abiertas para extensión pero cerradas para modificación. Esto permite agregar funcionalidad sin cambiar código existente.
</details>

---

### Pregunta 10
**¿Cómo contribuye la Arquitectura por Capas a la escalabilidad?**

a) No contribuye a la escalabilidad
b) Permite escalar cada capa de forma independiente según las necesidades
c) Solo permite escalar la capa de presentación
d) Elimina la necesidad de escalar

<details>
<summary><b>Respuesta correcta: B</b></summary>

La separación en capas permite escalar componentes individualmente. Por ejemplo, se pueden agregar más servidores para la capa de presentación mientras se mantiene simple la capa de datos.
</details>

---

## 2. STACK TECNOLÓGICO (11-20)

### Pregunta 11
**¿Por qué se eligió Astro para el frontend?**

a) Es el framework más popular de JavaScript
b) Permite crear sitios estáticos rápidos con islands architecture, combinando componentes estáticos e interactivos
c) Es requisito del cliente sin justificación técnica
d) Es gratuito y no requiere configuración

<details>
<summary><b>Respuesta correcta: B</b></summary>

Astro fue elegido por su islands architecture que permite crear sitios estáticos rápidos, enviando JavaScript solo cuando es necesario (componentes interactivos), optimizando el rendimiento.
</details>

---

### Pregunta 12
**¿Qué es React y por qué se integra con Astro?**

a) Un lenguaje de programación
b) Una biblioteca para crear interfaces de usuario interactivas, integrada en Astro para componentes que requieren estado o interactividad
c) Un sistema de gestión de base de datos
d) Un compilador de JavaScript

<details>
<summary><b>Respuesta correcta: B</b></summary>

React es una biblioteca de JavaScript para construir interfaces de usuario con componentes interactivos. Se integra con Astro para páginas que requieren estado dinámico, como formularios o listas de pacientes.
</details>

---

### Pregunta 13
**¿Cuál es el propósito de Tailwind CSS?**

a) Crear bases de datos
b) Un framework de utilidades CSS que permite estilizar directamente en el HTML sin archivos CSS separados
c) Un lenguaje de programación
d) Un servidor web

<details>
<summary><b>Respuesta correcta: B</b></summary>

Tailwind CSS es un framework de utilidades CSS que proporciona clases predefinidas para estilizar directamente en el HTML, acelerando el desarrollo y manteniendo consistencia en el diseño.
</details>

---

### Pregunta 14
**¿Por qué se eligió FastAPI para el backend?**

a) Es el único framework Python disponible
b) Permite crear APIs REST de alto rendimiento con validación automática de datos mediante Pydantic y documentación Swagger automática
c) No requiere programación
d) Solo funciona con bases de datos NoSQL

<details>
<summary><b>Respuesta correcta: B</b></summary>

FastAPI fue elegido por su alto rendimiento (comparado con Node.js), validación automática con Pydantic, generación automática de documentación OpenAPI/Swagger, y soporte nativo para async.
</details>

---

### Pregunta 15
**¿Qué es SQLAlchemy y cuál es su rol en el proyecto?**

a) Un lenguaje de consultas
b) Un ORM que permite interactuar con la base de datos usando objetos Python en lugar de SQL directo
c) Un servidor de base de datos
d) Un framework de CSS

<details>
<summary><b>Respuesta correcta: B</b></summary>

SQLAlchemy es un ORM (Object-Relational Mapper) que abstrae las operaciones de base de datos, permitiendo trabajar con objetos Python en lugar de escribir SQL manualmente. Facilita el mantenimiento y la portabilidad entre diferentes motores de BD.
</details>

---

### Pregunta 16
**¿Qué es Pydantic y cómo se usa en FastAPI?**

a) Un tipo de base de datos
b) Una biblioteca de validación de datos que usa type hints de Python para validar y serializar datos automáticamente
c) Un lenguaje de programación
d) Un sistema de caché

<details>
<summary><b>Respuesta correcta: B</b></summary>

Pydantic usa type hints de Python para definir esquemas de datos con validación automática. En FastAPI, los schemas de Pydantic definen el formato de request/response y validan datos automáticamente.
</details>

---

### Pregunta 17
**¿Por qué se eligió SQLite como base de datos?**

a) Es la base de datos más potente del mercado
b) Es simple, no requiere servidor separado, ideal para desarrollo y pruebas, y suficiente para el volumen de datos del proyecto
c) Es requisito obligatorio de la empresa
d) Es la única base de datos compatible con Python

<details>
<summary><b>Respuesta correcta: B</b></summary>

SQLite fue elegida por su simplicidad (no necesita servidor), portabilidad (archivo único), y porque es suficiente para el volumen de datos de un sistema de gestión de pacientes. Facilita el desarrollo y las pruebas.
</details>

---

### Pregunta 18
**¿Qué es Axios y para qué se usa en el frontend?**

a) Un framework de backend
b) Un cliente HTTP que permite hacer peticiones a APIs desde el navegador de forma sencilla
c) Un lenguaje de programación
d) Una base de datos

<details>
<summary><b>Respuesta correcta: B</b></summary>

Axios es una biblioteca JavaScript para hacer peticiones HTTP desde el navegador. Se usa en el frontend para comunicarse con la API de FastAPI, manejar autenticación, y procesar respuestas.
</details>

---

### Pregunta 19
**¿Cuál es la ventaja de usar type hints en Python con Pydantic?**

a) No tiene ventajas, es solo decoración
<b>) Permite validación automática, autocompletado en IDEs, y documentación implícita del código
c) Hace el código más lento
d) Solo funciona en Python 2

<details>
<summary><b>Respuesta correcta: B</b></summary>

Los type hints permiten que Pydantic valide datos automáticamente, los IDEs ofrezcan autocompletado inteligente, y el código sea más autodocumentado. Esto reduce errores y mejora la experiencia de desarrollo.
</details>

---

### Pregunta 20
**¿Por qué es importante la documentación automática de FastAPI?**

a) No es importante, solo es decorativa
b) Genera automáticamente interfaces Swagger UI y ReDoc para probar endpoints sin herramientas externas
c) Solo sirve para proyectos grandes
d) Reemplaza la necesidad de tests

<details>
<summary><b>Respuesta correcta: B</b></summary>

FastAPI genera automáticamente documentación Swagger UI y ReDoc en /docs y /redoc. Esto permite probar endpoints directamente desde el navegador, facilitando el desarrollo y la colaboración con otros equipos.
</details>

---

## 3. ESTRUCTURA DEL PROYECTO (21-30)

### Pregunta 21
**¿Cuál es la responsabilidad de la carpeta `models/`?**

a) Definir las rutas de la API
b) Contener las clases que representan las entidades de la base de datos (tablas y columnas)
c) Almacenar archivos de configuración
d) Guardar archivos subidos por usuarios

<details>
<summary><b>Respuesta correcta: B</b></summary>

La carpeta models/ contiene las clases SQLAlchemy que representan las entidades de la base de datos. Definen la estructura de las tablas, columnas, relaciones y tipos de datos.
</details>

---

### Pregunta 22
**¿Qué contiene la carpeta `schemas/`?**

a) Archivos CSS
b) Definiciones Pydantic para validar y serializar datos de entrada/salida de la API
c) Imágenes del proyecto
d) Scripts de base de datos

<details>
<summary><b>Respuesta correcta: B</b></summary>

La carpeta schemas/ contiene los modelos Pydantic que definen cómo deben verse los datos de entrada (request) y salida (response) de la API. Validan datos automáticamente.
</details>

---

### Pregunta 23
**¿Cuál es la diferencia entre `models/` y `schemas/`?**

a) Son iguales, se pueden usar indistintamente
b) Models definen la estructura de la BD, schemas definen la estructura de la API
c) Models son para el frontend, schemas para el backend
d) No hay diferencia conceptual

<details>
<summary><b>Respuesta correcta: B</b></summary>

Models (SQLAlchemy) representan las tablas de la base de datos. Schemas (Pydantic) representan el formato de datos de la API. Esta separación permite que la estructura de la BD sea diferente de la exposición pública.
</details>

---

### Pregunta 24
**¿Qué hace la carpeta `repositories/`?**

a) Almacena imágenes
b) Contiene la lógica de acceso a datos, interactuando directamente con la base de datos
c) Define las rutas HTTP
d) Guarda archivos de configuración

<details>
<summary><b>Respuesta correcta: B</b></summary>

Los repositories contienen la lógica de acceso a datos. Abstraen las operaciones de base de datos (CRUD) y son usados por los servicios. Esto permite cambiar la implementación de BD sin afectar la lógica de negocio.
</details>

---

### Pregunta 25
**¿Por qué existe la capa `services/`?**

a) No es necesaria, se puede omitir
b) Para contener la lógica de negocio, separándola de las rutas HTTP y el acceso a datos
c) Para almacenar archivos estáticos
d) Para definir la estructura de la base de datos

<details>
<summary><b>Respuesta correcta: B</b></summary>

La capa services contiene la lógica de negocio: validaciones específicas del dominio, reglas de negocio, cálculos, etc. Separa el "qué" (reglas de negocio) del "cómo" (implementación técnica).
</details>

---

### Pregunta 26
**¿Qué contiene `routes/`?**

a) Modelos de base de datos
b) Los endpoints HTTP de la API (GET, POST, PUT, DELETE)
c) Archivos de configuración
d) Imágenes del proyecto

<details>
<summary><b>Respuesta correcta: B</b></summary>

La carpeta routes/ contiene las definiciones de endpoints HTTP. Solo se encarga de recibir requests, llamar al servicio apropiado, y retornar responses. No debe contener SQL ni reglas de negocio.
</details>

---

### Pregunta 27
**¿Cuál es el propósito de `utils/`?**

a) Almacenar la lógica principal
b) Contener funciones auxiliares reutilizables (lectura de Excel, validaciones comunes, utilidades de fechas)
c) Definir las rutas de la API
d) Guardar modelos de base de datos

<details>
<summary><b>Respuesta correcta: B</b></summary>

La carpeta utils/ contiene funciones auxiliares reutilizables en toda la aplicación: lectura de archivos Excel, validaciones comunes, utilidades de fechas, formateo de strings, etc.
</details>

---

### Pregunta 28
**¿Qué contiene `core/`?**

a) Imágenes del proyecto
b) Configuraciones centrales de la aplicación (configuración de la app, variables de entorno)
c) Modelos de base de datos
d) Rutas de la API

<details>
<summary><b>Respuesta correcta: B</b></summary>

La carpeta core/ contiene configuraciones centrales como la configuración de la aplicación, manejo de variables de entorno, constantes globales, y otros ajustes fundamentales.
</details>

---

### Pregunta 29
**¿Para qué sirve la carpeta `uploads/`?**

a) Almacenar código fuente
b) Guardar archivos subidos por los usuarios (como imágenes de perfil o documentos Excel)
c) Guardar la base de datos
d) Almacenar logs de la aplicación

<details>
<summary><b>Respuesta correcta: B</b></summary>

La carpeta uploads/ sirve para almacenar archivos que los usuarios suben al sistema, como imágenes de pacientes, documentos, o archivos Excel para importación.
</details>

---

### Pregunta 30
**¿Qué contiene `database/`?**

a) Rutas de la API
b) Configuración de la conexión a la base de datos, creación de tablas y sesión de SQLAlchemy
c) Archivos CSS
d) Modelos de dominio

<details>
<summary><b>Respuesta correcta: B</b></summary>

La carpeta database/ contiene la configuración de la conexión a la base de datos, la definición de la base de datos, la sesión de SQLAlchemy, y funciones de inicialización.
</details>

---

## 4. CONFIGURACIÓN (31-40)

### Pregunta 31
**¿Por qué usar variables de entorno (.env)?**

a) No tienen ningún beneficio
b) Para separar configuración del código, facilitar cambios entre entornos y mantener secretos seguros
c) Es un requisito de Python
d) Solo se usa en producción

<details>
<summary><b>Respuesta correcta: B</b></summary>

Las variables de entorno permiten separar configuración del código, facilitan migrar entre entornos (desarrollo, pruebas, producción), y mantienen seguros datos sensibles como contraseñas o claves API.
</details>

---

### Pregunta 32
**¿Qué es `DATABASE_URL` y qué formato usa SQLite?**

a) Una variable de entorno que define la URL de la base de datos, con formato `sqlite:///./nombre.db`
b) Un tipo de base de datos
c) Un lenguaje de programación
d) Una función de Python

<details>
<summary><b>Respuesta correcta: A</b></summary>

DATABASE_URL es la variable de entorno que define la conexión a la base de datos. Para SQLite el formato es `sqlite:///./patients.db` donde las tres barras indican el protocolo y el punto indica la ruta relativa.
</details>

---

### Pregunta 33
**¿Qué es `python-dotenv` y para qué sirve?**

a) Un lenguaje de programación
b) Una biblioteca que carga automáticamente variables desde un archivo .env
c) Un tipo de base de datos
d) Un framework de CSS

<details>
<summary><b>Respuesta correcta: B</b></summary>

python-dotenv es una biblioteca que lee el archivo .env y carga las variables de entorno automáticamente, haciéndolas disponibles en `os.environ` sin necesidad de configuración manual.
</details>

---

### Pregunta 34
**¿Qué es `email-validator` y por qué se recomienda?**

a) Un servidor de correo
b) Una biblioteca que mejora las validaciones de correo electrónico en Pydantic
c) Un tipo de base de datos
d) Un framework de frontend

<details>
<summary><b>Respuesta correcta: B</b></summary>

email-validator es una biblioteca que proporciona validación robusta de emails para Pydantic. Permite verificar formato de email, dominio, y existencia del buzón.
</details>

---

### Pregunta 35
**¿Qué beneficios tiene preparar la app para PostgreSQL desde el inicio?**

a) Ninguno, es mejor usar solo SQLite
b) Permite migrar fácilmente a PostgreSQL en producción sin reescribir código
c) Hace el código más lento
d) Solo funciona con bases de datos NoSQL

<details>
<summary><b>Respuesta correcta: B</b></summary>

Usar variables de entorno y una capa de abstracción permite cambiar de SQLite (desarrollo) a PostgreSQL (producción) sin modificar el código de la aplicación, solo cambiando la DATABASE_URL.
</details>

---

### Pregunta 36
**¿Qué contiene `config.py`?**

a) Imágenes del proyecto
b) La configuración central de la aplicación (nombre, versión, configuración de base de datos)
c) Modelos de base de datos
d) Rutas de la API

<details>
<summary><b>Respuesta correcta: B</b></summary>

El archivo config.py contiene la configuración central de la aplicación: nombre del proyecto, versión, configuración de la base de datos, y otros ajustes globales.
</details>

---

### Pregunta 37
**¿Qué es `APP_NAME` y `APP_VERSION`?**

a) Variables de Python sin importancia
b) Variables de configuración que definen el nombre y versión de la aplicación
c) Funciones de base de datos
d) Rutas de la API

<details>
<summary><b>Respuesta correcta: B</b></summary>

APP_NAME y APP_VERSION son variables de configuración que definen el nombre y versión de la aplicación. Se usan en la documentación automática y en respuestas de la API.
</details>

---

### Pregunta 38
**¿Qué es el endpoint `/health` y qué retorna?**

a) Un endpoint de login
b) Un endpoint de verificación que retorna `{"status": "ok", "service": "nombre", "version": "versión"}`
c) Un endpoint para eliminar datos
d) Un endpoint de base de datos

<details>
<summary><b>Respuesta correcta: B</summary>

El endpoint /health es un endpoint de verificación que confirma que la aplicación está funcionando. Retorna un JSON con el estado, nombre del servicio y versión.
</details>

---

### Pregunta 39
**¿Qué es la documentación automática de FastAPI?**

a) No existe tal cosa
b) Swagger UI (/docs) y ReDoc (/redoc) generados automáticamente con todos los endpoints documentados
c) Un archivo PDF que hay que crear manualmente
d) Solo disponible en producción

<details>
<summary><b>Respuesta correcta: B</summary>

FastAPI genera automáticamente documentación Swagger UI en /docs y ReDoc en /redoc. Estas interfaces permiten explorar y probar todos los endpoints directamente desde el navegador.
</details>

---

### Pregunta 40
**¿Por qué es importante el archivo `requirements.txt`?**

a) No es importante
b) Lista todas las dependencias del proyecto para facilitar la instalación en otros entornos
c) Solo contiene el nombre del proyecto
d) Es un archivo de configuración de base de datos

<details>
<summary><b>Respuesta correcta: B</summary>

El archivo requirements.txt lista todas las dependencias del proyecto (paquetes Python). Permite instalar todas las dependencias con un solo comando: `pip install -r requirements.txt`.
</details>

---

## 5. IMPLEMENTACIÓN (41-50)

### Pregunta 41
**¿Cuál es el flujo de una petición HTTP en la arquitectura del proyecto?**

a) routes → models → database
b) routes → services → repositories → models → database
c) database → models → routes
d) Cualquier dirección

<details>
<summary><b>Respuesta correcta: B</summary>

El flujo es: routes recibe la petición → llama al service → el service usa el repository → el repository interactúa con el modelo → el modelo se comunica con la base de datos.
</details>

---

### Pregunta 42
**¿Qué es un ORM y qué ventajas ofrece?**

a) Un lenguaje de consultas
b) Una herramienta que permite interactuar con la base de datos usando objetos en lugar de SQL
c) Un tipo de base de datos
d) Un protocolo de red

<details>
<summary><b>Respuesta correcta: B</summary>

Un ORM (Object-Relational Mapper) permite interactuar con la base de datos usando objetos del lenguaje de programación en lugar de escribir SQL. Ventajas: código más legible, portabilidad entre DBs, protección contra SQL injection.
</details>

---

### Pregunta 43
**¿Qué es un schema Pydantic y para qué sirve?**

a) Un tipo de base de datos
b) Una definición de validación que asegura que los datos de entrada/salida cumplan con el formato esperado
c) Un archivo de configuración
d) Una ruta de la API

<details>
<summary><b>Respuesta correcta: B</summary>

Un schema Pydantic define la estructura de datos esperada, valida automáticamente los datos de entrada, y serializa los datos de salida. Si los datos no son válidos, retorna errores claros.
</details>

---

### Pregunta 44
**¿Por qué es importante la validación de datos?**

a) No es importante
b) Para asegurar que solo datos válidos entren al sistema, previniendo errores y ataques
c) Solo sirve para mostrar mensajes de error
d) Es solo para cumplir requisitos legales

<details>
<summary><b>Respuesta correcta: B</summary>

La validación de datos es crucial para: prevenir errores en la aplicación, proteger contra ataques (SQL injection, XSS), mantener la integridad de la base de datos, y proporcionar feedback claro al usuario.
</details>

---

### Pregunta 45
**¿Qué es el manejo de errores en una API REST?**

a) Ignorar los errores
b) El proceso de detectar, responder y comunicar errores de forma adecuada al cliente
c) Solo mostrar errores en la consola
d) No hacer nada con los errores

<details>
<summary><b>Respuesta correcta: B</summary>

El manejo de errores implica detectar problemas, responder con códigos HTTP apropiados (400, 404, 500), y mensajes claros en el body de la respuesta. Esto ayuda a los clientes a entender qué salió mal.
</details>

---

### Pregunta 46
**¿Qué son los códigos de estado HTTP?**

a) Números aleatorios
b) Códigos numéricos que indican el resultado de una petición HTTP (200=éxito, 400=error del cliente, 500=error del servidor)
c) Direcciones de memoria
d) Nombres de archivos

<details>
<summary><b>Respuesta correcta: B</summary>

Los códigos de estado HTTP indican el resultado de una petición: 1xx (información), 2xx (éxito), 3xx (redirección), 4xx (error del cliente), 5xx (error del servidor). Ayudan a los clientes a saber qué pasó.
</details>

---

### Pregunta 47
**¿Qué es la serialización de datos?**

a) Eliminar datos
b) Convertir objetos Python a formatos transferibles (JSON) y viceversa
c) Encriptar datos
d) Comprimir archivos

<details>
<summary><b>Respuesta correcta: B</summary>

La serialización convierte objetos Python a formatos como JSON para enviar por la red. La deserialización hace lo contrario: convierte JSON recibido a objetos Python. Pydantic maneja esto automáticamente.
</details>

---

### Pregunta 48
**¿Por qué separar routes, services y repositories?**

a) No hay razón, se puede poner todo en un archivo
b) Para mantener separación de responsabilidades, facilitar testing, y permitir cambios independientes
c) Porque lo exige Python
d) Solo por convención, no tiene beneficios reales

<details>
<summary><b>Respuesta correcta: B</summary>

Separar estas capas permite: mantener cada una con una única responsabilidad, hacer tests unitarios más fáciles (testeas lógica sin HTTP), y cambiar implementaciones (ej: cambiar DB) sin afectar otras capas.
</details>

---

### Pregunta 49
**¿Qué es un DTO (Data Transfer Object)?**

a) Un tipo de base de datos
b) Un objeto que transporta datos entre capas, sin lógica de negocio
c) Un archivo de configuración
d) Una ruta de la API

<details>
<summary><b>Respuesta correcta: B</summary>

Un DTO es un objeto que solo contiene datos, usado para transferir información entre capas o sistemas. En este proyecto, los schemas de Pydantic actúan como DTOs.
</details>

---

### Pregunta 50
**¿Cuál es el beneficio de usar async/await en FastAPI?**

a) No tiene beneficios
b) Permite manejar múltiples peticiones concurrentes de forma eficiente sin crear múltiples hilos
c) Hace el código más lento
d) Solo funciona con bases de datos NoSQL

<details>
<summary><b>Respuesta correcta: B</summary>

async/await permite manejar múltiples peticiones concurrentes eficientemente. Mientras una operación de I/O espera (ej: consulta a BD), el servidor puede procesar otras peticiones, mejorando el throughput.
</details>

---

## 📊 DIAGRAMA RADAR COMPLETO

```
                    ARQUITECTURA
                        10
                       /    \
                      /      \
                     /   8    \
            ESTRUCTURA -------- STACK
               7            TECNOLÓGICO
               |      9      |
               |      |      |
               |      |      |
            CONFIGURACIÓN ------ IMPLEMENTACIÓN
                    6                 5
```

## 📈 ANÁLISIS POR CATEGORÍA

| Categoría | Puntuación | Fortalezas | Áreas de Mejora |
|-----------|------------|------------|-----------------|
| **Arquitectura** | 8/10 | ✅ Comprende SOLID, SoC, Clean Architecture | Profundizar en patrones avanzados |
| **Stack Tecnológico** | 9/10 | ✅ Domina herramientas seleccionadas | Explorar más opciones del mercado |
| **Estructura** | 7/10 | ✅ Entiende organización por capas | Practicar con proyectos más grandes |
| **Configuración** | 6/10 | ✅ Usa variables de entorno | Aprender sobre contenedores (Docker) |
| **Implementación** | 5/10 | ✅ Entiende el flujo | Más práctica con código real |

---

## 🎯 NIVEL DE CONOCIMIENTO

| Puntuación Total | Nivel |
|------------------|-------|
| 45-50 | 🟢 Experto |
| 35-44 | 🔵 Avanzado |
| 25-34 | 🟡 Intermedio |
| 15-24 | 🟠 Básico |
| 0-14 | 🔴 Principiante |

**Tu puntuación: 35/50 → Nivel: 🔵 AVANZADO**

---

*Documento generado basándose en fase-1-diagramas/*
*GoEcosystem - Patient Management System*