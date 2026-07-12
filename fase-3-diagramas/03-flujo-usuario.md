# Fase 3 — Diagrama de Flujo de Usuario

## Flujo de Importación de Pacientes desde Excel

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              FLUJO DE USUARIO - IMPORTACIÓN EXCEL                  │
└─────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────┐
    │  USUARIO │
    └────┬─────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  1. ACCEDE AL SISTEMA                                                               │
│     - Abre Swagger UI: http://localhost:8000/docs                                   │
│     - O usa Postman para probar la API                                              │
└─────────────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  2. PREPARA EL ARCHIVO EXCEL                                                        │
│     - Formato: .xlsx (obligatorio)                                                   │
│     - Ubicación: /excel/pacientes_ejemplo.xlsx                                      │
│                                                                                      │
│     Columnas requeridas:                                                            │
│     ┌─────────────────┬─────────────────────┬──────────────┬────────────────┐        │
│     │ TipoDocumento   │ NumeroDocumento     │ Nombres      │ Apellidos     │        │
│     ├─────────────────┼─────────────────────┼──────────────┼────────────────┤        │
│     │ CC              │ 1001234567         │ JUAN CARLOS  │ PEREZ GOMEZ   │        │
│     │ CE              │ 1007654321         │ MARIA ELENA  │ RODRIGUEZ...  │        │
│     └─────────────────┴─────────────────────┴──────────────┴────────────────┘        │
│                                                                                      │
│     Columnas opcionales: Telefono, Correo, Direccion, Estado                         │
└─────────────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  3. ENVÍA EL ARCHIVO POR POST                                                        │
│                                                                                      │
│     Método: POST                                                                     │
│     URL: http://localhost:8000/api/v1/pacientes/importar                             │
│     Content-Type: multipart/form-data                                               │
│     Campo: file (archivo Excel)                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  4. SISTEMA PROCESA EL ARCHIVO                                                       │
│                                                                                      │
│     ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│     │ ExcelReader │───▶│ Validar     │───▶│ Normalizar  │───▶│ Batch       │       │
│     │ (Pandas)    │    │ Columnas    │    │ Datos       │    │ Insert      │       │
│     └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘       │
│                                                                    │                 │
│                                                                    ▼                 │
│                                                      ┌─────────────────────────┐   │
│                                                      │ Repository.create_batch()│   │
│                                                      │ - Verifica duplicados   │   │
│                                                      │ - Inserta registros     │   │
│                                                      │ - Maneja errores        │   │
│                                                      └─────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  5. SISTEMA RETORNA RESPUESTA JSON                                                   │
│                                                                                      │
│     {                                                                                │
│       "archivo": "pacientes.xlsx",                                                   │
│       "total_registros": 10,                                                         │
│       "insertados": 8,                                                               │
│       "duplicados": 1,                                                               │
│       "errores": 1,                                                                  │
│       "detalles_errores": [                                                          │
│         { "row": 5, "column": "Nombres", "error": "Nombres es requerido" }          │
│       ],                                                                             │
│       "ids_insertados": [1, 2, 3, 4, 5, 6, 7, 8],                                   │
│       "mensaje": "Importación exitosa. 8 paciente(s) importado(s)."                │
│     }                                                                                │
└─────────────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  6. USUARIO VISUALIZA EL RESULTADO                                                   │
│                                                                                      │
│     ✅ Éxito: "Importación exitosa. 8 paciente(s) importado(s)."                   │
│     ⚠️  Parcial: "Importación parcial. 8 insertados, 1 duplicado, 1 error."          │
│     ❌  Error: "No se importaron pacientes. 10 documento(s) ya existen."            │
└─────────────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  7. VERIFICA LOS DATOS IMPORTADOS                                                    │
│                                                                                      │
│     GET /api/v1/pacientes/                                                           │
│     GET /api/v1/pacientes/{id}                                                       │
│     GET /api/v1/pacientes/count                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════════════
                           PANTALLAS DEL SISTEMA
═══════════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  SWAGGER UI - POST /importar                                                        │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  POST /api/v1/pacientes/importar                                                     │
│  ───────────────────────────────────────────────────────────────────────────────    │
│                                                                                      │
│  Try it out   [●]                                                                    │
│                                                                                      │
│  Parameters  [+]                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │ file: (file) *                                                                            │
│  │ Description: Archivo Excel (.xlsx) con los pacientes a importar              │    │
│  │ Choose File [pacientes_ejemplo.xlsx                                    ]    │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                      │
│  Execute   [CURL] [Request URL] [Response Headers]                                   │
│                                                                                      │
│  Response 200                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │ {                                                                            │    │
│  │   "archivo": "pacientes_ejemplo.xlsx",                                        │    │
│  │   "total_registros": 10,                                                      │    │
│  │   "insertados": 10,                                                           │    │
│  │   "duplicados": 0,                                                            │    │
│  │   "errores": 0,                                                               │    │
│  │   "detalles_errores": [],                                                     │    │
│  │   "ids_insertados": [1,2,3,4,5,6,7,8,9,10],                                  │    │
│  │   "mensaje": "Importación exitosa. 10 paciente(s) importado(s)."             │    │
│  │ }                                                                            │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════════════
                           CASOS DE ERROR
═══════════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  ERROR 1: Archivo vacío                                                              │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  Response 400 Bad Request                                                            │
│  {                                                                                   │
│    "detail": "Error al leer el archivo: El archivo está vacío"                       │
│  }                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  ERROR 2: Columnas faltantes                                                         │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  Response 400 Bad Request                                                            │
│  {                                                                                   │
│    "detail": "Error al leer el archivo: Columnas faltantes: Nombres, Apellidos"      │
│  }                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  ERROR 3: Formato de archivo inválido                                                │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  Response 400 Bad Request                                                            │
│  {                                                                                   │
│    "detail": "Error al leer el archivo: Formato de archivo no válido. Solo se        │
│              acepta .xlsx, recibido: .csv"                                           │
│  }                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  ERROR 4: Todos los documentos duplicados                                             │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  Response 200 OK                                                                     │
│  {                                                                                   │
│    "archivo": "pacientes.xlsx",                                                      │
│    "total_registros": 10,                                                           │
│    "insertados": 0,                                                                 │
│    "duplicados": 10,                                                                 │
│    "errores": 0,                                                                    │
│    "mensaje": "No se importaron pacientes. 10 documento(s) ya existen."             │
│  }                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Resumen del Flujo

| Paso | Acción | Resultado |
|------|--------|-----------|
| 1 | Usuario accede al sistema | Swagger UI o Postman |
| 2 | Prepara archivo Excel | Archivo .xlsx con datos de pacientes |
| 3 | Envía POST /importar | Archivo enviado al servidor |
| 4 | Sistema procesa | Validación → Normalización → Inserción |
| 5 | Sistema responde | JSON con resumen |
| 6 | Usuario ve resultado | Mensaje de éxito/parcial/error |
| 7 | Verifica datos | GET /pacientes para confirmar |