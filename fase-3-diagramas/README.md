# Fase 3 - Diagramas

Este directorio contiene la documentación visual de la Fase 3 del proyecto GoEcosystem.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `fas3-contxto.md` | Contexto y objetivos de la Fase 3 |
| `03-flujo-usuario.md` | Diagrama de flujo de usuario para importar Excel |
| `04-postman.md` | Colección Postman con requests y respuestas |
| `05-diagrama-clases.md` | Diagrama de clases y arquitectura |

## Resumen de la Fase 3

La Fase 3 implementa la **importación de pacientes desde archivos Excel**.

### Endpoint

```
POST /api/v1/pacientes/importar
```

### Flujo

1. Usuario selecciona archivo `.xlsx`
2. Sistema valida formato y columnas
3. Sistema normaliza datos
4. Sistema inserta en batch
5. Sistema retorna resumen JSON

### Archivos creados

```
backend/
├── utils/
│   └── excel_reader.py          # Lector de Excel con Pandas
├── schemas/
│   └── import_result.py          # Schemas de respuesta
├── services/
│   └── patient_service.py        # Lógica de importación
├── repositories/
│   └── patient_repository.py    # Inserción en batch
└── routes/
    └── patient.py               # Endpoint POST /importar

excel/
├── pacientes_ejemplo.csv        # CSV de ejemplo
├── pacientes_ejemplo.xlsx       # Excel de ejemplo (generado)
└── generar_excel.py            # Script para generar Excel
```

### Documentación de APIs

- **Swagger UI**: http://localhost:8000/docs
- **Postman**: Ver `04-postman.md` para colección completa