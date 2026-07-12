# Fase 3 — Colección Postman

## Importar Pacientes desde Excel

```
═══════════════════════════════════════════════════════════════════════════════════════
                           COLECCIÓN POSTMAN - GOECOSYSTEM API
═══════════════════════════════════════════════════════════════════════════════════════

Colección: GoEcosystem - Fase 3: Importación Excel
Carpeta: /excel/
Base URL: http://localhost:8000/api/v1


═══════════════════════════════════════════════════════════════════════════════════════
                           REQUEST 1: Importar Pacientes desde Excel
═══════════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  IMPORTAR PACIENTES                                                                  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  Método: POST                                                                         │
│  URL: {{baseURL}}/pacientes/importar                                                 │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │  Body                                                                          │    │
│  │  ─────                                                                          │    │
│  │  Tipo: form-data                                                                │    │
│  │                                                                                │    │
│  │  ┌──────────┬────────────────────────────────────────────────────────────┐   │    │
│  │  │ KEY      │ VALUE                                                         │   │    │
│  │  ├──────────┼────────────────────────────────────────────────────────────┤   │    │
│  │  │ file     │ [Seleccionar archivo] pacientes_ejemplo.xlsx               │   │    │
│  │  └──────────┴────────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                      │
│  Headers:                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │  Content-Type: multipart/form-data                                            │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════════════
                           CÓDIGO CURL
═══════════════════════════════════════════════════════════════════════════════════════

curl --location 'http://localhost:8000/api/v1/pacientes/importar' \
--form 'file=@"/ruta/a/pacientes_ejemplo.xlsx"'


═══════════════════════════════════════════════════════════════════════════════════════
                           RESPONSE EXITOSA (200 OK)
═══════════════════════════════════════════════════════════════════════════════════════

{
  "archivo": "pacientes_ejemplo.xlsx",
  "total_registros": 10,
  "insertados": 10,
  "duplicados": 0,
  "errores": 0,
  "detalles_errores": [],
  "ids_insertados": [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10
  ],
  "mensaje": "Importación exitosa. 10 paciente(s) importado(s)."
}


═══════════════════════════════════════════════════════════════════════════════════════
                           RESPONSE PARCIAL (200 OK)
═══════════════════════════════════════════════════════════════════════════════════════

{
  "archivo": "pacientes_ejemplo.xlsx",
  "total_registros": 10,
  "insertados": 8,
  "duplicados": 1,
  "errores": 1,
  "detalles_errores": [
    {
      "row": 5,
      "column": "Nombres",
      "value": null,
      "error": "Nombres es requerido"
    }
  ],
  "ids_insertados": [
    1,
    2,
    3,
    4,
    6,
    7,
    8,
    9
  ],
  "mensaje": "Importación parcial. 8 paciente(s) importado(s), 1 duplicado(s), 1 error(es)."
}


═══════════════════════════════════════════════════════════════════════════════════════
                           RESPONSE ERROR (400 Bad Request)
═══════════════════════════════════════════════════════════════════════════════════════

{
  "detail": "Error al leer el archivo: Columnas faltantes en el Excel: Nombres"
}


═══════════════════════════════════════════════════════════════════════════════════════
                           COLECCIÓN COMPLETA - POSTMAN EXPORT
═══════════════════════════════════════════════════════════════════════════════════════

{
  "info": {
    "name": "GoEcosystem - Fase 3: Importación Excel",
    "description": "Endpoints para importar pacientes desde archivos Excel",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Importar Pacientes desde Excel",
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "formdata",
          "formdata": [
            {
              "key": "file",
              "type": "file",
              "description": "Archivo Excel (.xlsx) con los pacientes a importar"
            }
          ]
        },
        "url": {
          "raw": "{{baseURL}}/pacientes/importar",
          "host": ["{{baseURL}}"],
          "path": ["pacientes", "importar"]
        }
      },
      "response": [
        {
          "name": "Importación Exitosa",
          "status": "200 OK",
          "body": "{\n  \"archivo\": \"pacientes_ejemplo.xlsx\",\n  \"total_registros\": 10,\n  \"insertados\": 10,\n  \"duplicados\": 0,\n  \"errores\": 0,\n  \"detalles_errores\": [],\n  \"ids_insertados\": [1,2,3,4,5,6,7,8,9,10],\n  \"mensaje\": \"Importación exitosa. 10 paciente(s) importado(s).\"\n}"
        },
        {
          "name": "Importación Parcial",
          "status": "200 OK",
          "body": "{\n  \"archivo\": \"pacientes_ejemplo.xlsx\",\n  \"total_registros\": 10,\n  \"insertados\": 8,\n  \"duplicados\": 1,\n  \"errores\": 1,\n  \"detalles_errores\": [{\"row\": 5, \"column\": \"Nombres\", \"error\": \"Nombres es requerido\"}],\n  \"ids_insertados\": [1,2,3,4,6,7,8,9],\n  \"mensaje\": \"Importación parcial. 8 paciente(s) importado(s), 1 duplicado(s), 1 error(es).\"\n}"
        },
        {
          "name": "Error - Columnas Faltantes",
          "status": "400 Bad Request",
          "body": "{\n  \"detail\": \"Error al leer el archivo: Columnas faltantes en el Excel: Nombres\"\n}"
        },
        {
          "name": "Error - Formato Inválido",
          "status": "400 Bad Request",
          "body": "{\n  \"detail\": \"Error al leer el archivo: Formato de archivo no válido. Solo se acepta .xlsx, recibido: .csv\"\n}"
        }
      ]
    }
  ],
  "variable": [
    {
      "key": "baseURL",
      "value": "http://localhost:8000/api/v1"
    }
  ]
}


═══════════════════════════════════════════════════════════════════════════════════════
                           CONFIGURACIÓN DE VARIABLES
═══════════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  Environment: GoEcosystem Local                                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  Variable          Valor                    Tipo                                     │
│  ─────────────────────────────────────────────────────────────────────────────      │
│  baseURL           http://localhost:8000/api/v1    String                            │
│  host              localhost                 String                                  │
│  port              8000                      Number                                  │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════════════
                           PRUEBAS EN POSTMAN
═══════════════════════════════════════════════════════════════════════════════════════

// Test: Verificar que la respuesta sea exitosa
pm.test("Respuesta exitosa", function() {
    pm.response.to.have.status(200);
});

// Test: Verificar que se insertaron pacientes
pm.test("Pacientes insertados", function() {
    var jsonData = pm.response.json();
    pm.expect(jsonData.insertados).to.be.above(0);
});

// Test: Verificar estructura de respuesta
pm.test("Estructura correcta", function() {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('archivo');
    pm.expect(jsonData).to.have.property('total_registros');
    pm.expect(jsonData).to.have.property('insertados');
    pm.expect(jsonData).to.have.property('duplicados');
    pm.expect(jsonData).to.have.property('errores');
    pm.expect(jsonData).to.have.property('ids_insertados');
    pm.expect(jsonData).to.have.property('mensaje');
});

// Test: Verificar mensaje de éxito
pm.test("Mensaje de éxito", function() {
    var jsonData = pm.response.json();
    pm.expect(jsonData.mensaje).to.include("Importación exitosa");
});


═══════════════════════════════════════════════════════════════════════════════════════
                           SCRIPTS PRE-REQUEST
═══════════════════════════════════════════════════════════════════════════════════════

// Verificar que se seleccionó un archivo
if (!pm.iterationData.get("file")) {
    console.log("Advertencia: No se encontró archivo en iterationData");
}
```

---

## Endpoints Relacionados para Verificar Importación

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  VERIFICAR IMPORTACIÓN                                                              │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  GET {{baseURL}}/pacientes/count                                                    │
│  ───────────────────────────────────────────────────────────────────────────────    │
│  Verifica el total de pacientes en la base de datos                                  │
│                                                                                      │
│  Response:                                                                           │
│  { "total": 10 }                                                                     │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  LISTAR PACIENTES                                                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  GET {{baseURL}}/pacientes?skip=0&limit=10                                          │
│  ───────────────────────────────────────────────────────────────────────────────    │
│  Lista los pacientes importados                                                      │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  BUSCAR PACIENTE                                                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  GET {{baseURL}}/pacientes/search?q=JUAN                                            │
│  ───────────────────────────────────────────────────────────────────────────────    │
│  Busca pacientes por nombre, apellido o documento                                    │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```