## Fase 1 — Inicialización del Proyecto y Arquitectura

Esta primera fase tiene como objetivo dejar listo el entorno de desarrollo con una arquitectura limpia, escalable y profesional. Antes de escribir código de negocio, se configurarán el repositorio Git, el backend con FastAPI y el frontend con Astro + React + Tailwind CSS.

---

# Objetivos de la Fase 1

Al finalizar esta fase se debe tener:

* ✅ Repositorio Git inicializado.
* ✅ Repositorio en GitHub conectado.
* ✅ Proyecto dividido en Frontend y Backend.
* ✅ FastAPI funcionando.
* ✅ Astro + React + Tailwind funcionando.
* ✅ `.gitignore` configurado.
* ✅ `README.md` inicial.
* ✅ Primer commit.

---

# Arquitectura del Proyecto

```text
goecosystem-fullstack-test/
│
├── backend/
│   ├── app/
│   │
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── services/
│   ├── repositories/
│   ├── core/
│   ├── database/
│   ├── utils/
│   ├── uploads/
│   ├── static/
│   │
│   ├── database.py
│   ├── config.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │
│   ├── assets/
│   ├── components/
│   ├── layouts/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   ├── types/
│   ├── utils/
│   ├── styles/
│   └── constants/
│
├── docs/
│
├── excel/
│
├── .gitignore
├── README.md
└── LICENSE
```

---

# Crear la carpeta principal

```bash
mkdir goecosystem-fullstack-test

cd goecosystem-fullstack-test
```

---

# Inicializar Git

```bash
git init
```

Comprobar:

```bash
git status
```

---

# Crear el repositorio en GitHub

Nombre recomendado:

```text
goecosystem-fullstack-test
```

No agregar:

* README
* License
* .gitignore

---

# Conectar GitHub

```bash
git remote add origin https://github.com/TU_USUARIO/goecosystem-fullstack-test.git
```

Verificar:

```bash
git remote -v
```

---

# Crear las carpetas principales

```bash
mkdir backend
mkdir frontend
mkdir docs
mkdir excel
```

---

# Estructura del Backend

Entrar:

```bash
cd backend
```

Crear estructura:

```bash
mkdir app
mkdir models
mkdir schemas
mkdir routes
mkdir services
mkdir repositories
mkdir core
mkdir database
mkdir utils
mkdir uploads
mkdir static
```

---

# Crear archivos

```bash
touch main.py
touch database.py
touch config.py
touch requirements.txt
```

Windows (PowerShell):

```powershell
New-Item main.py
New-Item database.py
New-Item config.py
New-Item requirements.txt
```

---

# Crear entorno virtual

Windows

```bash
python -m venv venv
```

Activar

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

# Instalar FastAPI

```bash
pip install fastapi
```

```bash
pip install uvicorn
```

```bash
pip install sqlalchemy
```

```bash
pip install pydantic
```

```bash
pip install pandas
```

```bash
pip install openpyxl
```

Guardar dependencias:

```bash
pip freeze > requirements.txt
```

---

# Crear Frontend

Volver a la raíz:

```bash
cd ..
```

Crear proyecto Astro:

```bash
npm create astro@latest frontend
```

Seleccionar:

```text
Minimal
```

Después:

```text
TypeScript

Yes
```

Instalar React:

```bash
cd frontend

npx astro add react
```

Agregar Tailwind:

```bash
npx astro add tailwind
```

Instalar Axios:

```bash
npm install axios
```

Instalar dependencias:

```bash
npm install
```

---

# Crear estructura Frontend

Dentro de `src`:

```text
src/

assets/

components/

layouts/

pages/

hooks/

services/

types/

utils/

styles/

constants/
```

---

# Crear README

```text
# Go Ecosystem FullStack Test

Prueba técnica desarrollada con:

- FastAPI
- Astro
- React
- Tailwind CSS
- SQLite

Autor:
Alejandro Escandón
```

---

# Crear .gitignore

```gitignore
# Python
venv/
__pycache__/
*.pyc

# SQLite
*.db

# Environment
.env

# Node
node_modules/

# Astro
dist/

# VSCode
.vscode/

# Logs
*.log

# OS
.DS_Store
Thumbs.db

# Excel temporal
~$*.xlsx
```

---

# Primer Commit

```bash
git add .
```

```bash
git commit -m "chore: initialize full stack project structure"
```

---

# Publicar

```bash
git push -u origin main
```

---

# Resultado esperado

Al finalizar la Fase 1 deberías tener:

```text
goecosystem-fullstack-test
│
├── backend/
│   ├── app/
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── services/
│   ├── repositories/
│   ├── core/
│   ├── database/
│   ├── utils/
│   ├── uploads/
│   ├── static/
│   ├── main.py
│   ├── database.py
│   ├── config.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── styles/
│   │   ├── types/
│   │   ├── utils/
│   │   └── constants/
│
├── docs/
├── excel/
├── .gitignore
└── README.md
```

### Próxima fase

La **Fase 2** consistirá en diseñar el modelo de datos, crear la base de datos SQLite con SQLAlchemy, definir las entidades (`Paciente`, `Usuario`, `Catálogo`), preparar las migraciones y dejar la API lista para implementar el CRUD. Esta base facilitará la importación desde Excel y el desarrollo del frontend.
