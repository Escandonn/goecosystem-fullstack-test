Ese es el siguiente paso lógico. Ya no estás en la fase de autenticación; ahora entras en la **integración del módulo de administración de pacientes**.

No haría que el frontend llame directamente a los endpoints desde los componentes. Lo profesional es mantener la misma separación de responsabilidades que tienes en el backend.

La siguiente fase la documentaría así:

---

# Fase 5 — Dashboard Administrador e Integración de Pacientes

## Objetivo

Integrar el Dashboard del Administrador con el backend para consumir y visualizar la información real de los pacientes.

En esta fase **no se implementará todavía el CRUD visual completo**. El objetivo es conectar el frontend con la API desarrollada en FastAPI y renderizar la información siguiendo la arquitectura definida desde el inicio del proyecto.

Todos los datos mostrados en pantalla deberán provenir del backend mediante peticiones HTTP autenticadas con JWT.

---

# Objetivos de la Fase 5

Al finalizar esta fase se debe tener:

* ✅ Dashboard del Administrador.
* ✅ Consumo de la API de pacientes.
* ✅ Axios utilizando JWT.
* ✅ Renderizado dinámico de pacientes.
* ✅ Componentes reutilizables.
* ✅ Estados de carga.
* ✅ Manejo de errores.
* ✅ Estructura preparada para CRUD.

---

# Arquitectura

```text
Administrador

↓

Dashboard

↓

React Components

↓

Custom Hooks

↓

Services

↓

Axios

↓

FastAPI

↓

SQLite
```

Cada capa tendrá una responsabilidad específica.

---

# Flujo de Datos

```text
Administrador

↓

Dashboard

↓

usePatients()

↓

PatientService

↓

GET /api/v1/pacientes

↓

FastAPI

↓

Repository

↓

SQLite

↓

JSON

↓

Frontend

↓

Renderizado
```

Todo el flujo respetará la arquitectura implementada en el backend.

---

# Organización del Frontend

```text
src/

pages/

admin/

dashboard.astro

components/

dashboard/

DashboardCards.tsx

PatientTable.tsx

PatientRow.tsx

SearchBar.tsx

Loading.tsx

EmptyState.tsx

services/

patientService.ts

hooks/

usePatients.ts

types/

patient.ts
```

---

# Responsabilidad de cada carpeta

## pages/

Únicamente define las rutas.

No debe contener lógica de negocio.

---

## hooks/

Gestiona el estado de los pacientes.

Ejemplo:

```text
usePatients()
```

Será responsable de:

* consultar la API;
* almacenar pacientes;
* manejar loading;
* manejar errores.

---

## services/

Toda comunicación con FastAPI.

Ejemplo:

```text
patientService.ts
```

Funciones:

```text
getPatients()

getPatient()

searchPatients()

countPatients()
```

Ningún componente realizará llamadas HTTP directamente.

---

## types/

Interfaces TypeScript.

Ejemplo:

```typescript
interface Patient {

id:number

tipo_documento:string

numero_documento:string

nombres:string

apellidos:string

telefono:string

correo:string

estado:string
}
```

---

## components/

Componentes reutilizables.

Cada componente tendrá una única responsabilidad.

---

# Dashboard

Al ingresar como Administrador se visualizará:

```text
Dashboard

────────────────────────

Total Pacientes

Pacientes Activos

Pacientes Inactivos

────────────────────────

Listado de Pacientes
```

En esta fase las tarjetas podrán mostrar inicialmente el total de pacientes obtenido desde la API y dejar preparadas las métricas restantes para fases posteriores.

---

# Consumo del Backend

Endpoints utilizados.

```http
GET

/api/v1/pacientes
```

```http
GET

/api/v1/pacientes/count
```

Todos consumirán JWT.

---

# Renderizado

Los pacientes se mostrarán en una tabla.

```text
Documento

Nombre

Correo

Teléfono

Estado
```

Los registros serán generados dinámicamente utilizando React.

No existirá información estática.

---

# Estados de la Aplicación

## Loading

Mientras la API responde.

Mostrar spinner.

---

## Error

Si falla la petición.

Mostrar:

```text
No fue posible obtener la información.
```

---

## Sin resultados

Mostrar:

```text
No existen pacientes registrados.
```

---

# Seguridad

Todas las peticiones deberán incluir:

```http
Authorization

Bearer TOKEN
```

Si el backend responde:

```http
401
```

↓

Cerrar sesión.

↓

Redireccionar al Login.

---

# Preparación para el CRUD

Aunque en esta fase únicamente se visualizarán los datos, la estructura quedará preparada para incorporar posteriormente:

* Crear paciente.
* Editar paciente.
* Eliminar paciente.
* Buscar pacientes.
* Paginación.
* Ordenamiento.
* Importación desde Excel.

Sin modificar la arquitectura del proyecto.

---

# Casos de Prueba

* Login como Administrador.
* Obtener listado de pacientes.
* Obtener total de pacientes.
* Mostrar mensaje cuando no existan registros.
* Manejar error de conexión.
* Token expirado.
* Redirección al Login cuando la sesión expire.

---

# Estructura Esperada

```text
frontend/

src/

pages/

admin/

dashboard.astro

components/

dashboard/

DashboardCards.tsx

PatientTable.tsx

PatientRow.tsx

Loading.tsx

EmptyState.tsx

services/

patientService.ts

hooks/

usePatients.ts

types/

patient.ts

layouts/

AdminLayout.astro
```

---

# Commit recomendado

```bash
git add .

git commit -m "feat: integrate admin dashboard with patient API"
```

---

# Resultado Esperado

Al finalizar esta fase, el Administrador podrá iniciar sesión, acceder a su Dashboard y visualizar información real proveniente del backend. La integración respetará la arquitectura definida desde el inicio del proyecto, manteniendo separadas las responsabilidades entre componentes, hooks, servicios y tipos. Esta base permitirá implementar en las siguientes fases el CRUD completo, la búsqueda, la paginación y la importación de pacientes sin necesidad de reorganizar la aplicación.

### Próxima fase (Fase 5.5)

Después de esta integración, el siguiente paso natural sería desarrollar el **CRUD visual completo**, agregando:

* Crear paciente (modal o formulario).
* Editar paciente.
* Eliminar con confirmación.
* Búsqueda en tiempo real.
* Paginación.
* Ordenamiento.
* Importación de Excel desde el frontend.
* Actualización automática del Dashboard tras cada operación.

De esta forma el desarrollo avanza de manera incremental y mantiene una arquitectura limpia y consistente.
