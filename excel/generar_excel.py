"""Script para generar el archivo Excel de ejemplo con pacientes."""

import pandas as pd
from pathlib import Path


def create_sample_excel():
    """Crea un archivo Excel de ejemplo con datos de pacientes."""
    
    data = {
        "paciente_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "tipo_documento": ["CC", "CC", "CC", "CE", "CC", "TI", "CC", "CC", "CC", "CC"],
        "documento": [
            "1001234567", "1007654321", "1012345678", "1023456789", "1034567890",
            "1045678901", "1056789012", "1067890123", "1078901234", "1089012345"
        ],
        "nombre_completo": [
            "JUAN CARLOS PEREZ GOMEZ", "MARIA ELENA RODRIGUEZ LOPEZ", "CARLOS ANDRES GOMEZ VARGAS",
            "ANA LUCIA MARTINEZ SANCHEZ", "PEDRO JOSE DIAZ RAMIREZ", "LAURA FERNANDA CASTRO MORENO",
            "JORGE ENRIQUE LOPEZ GUERRA", "PATRICIA DEL PILAR VEGA HERRERA",
            "ALEJANDRO JOSE MENDOZA TORRES", "CLAUDIA PATRICIA ORTIZ RAMOS"
        ],
        "fecha_nacimiento": [
            "1985-03-15", "1990-07-22", "1978-11-30", "1995-01-10", "1982-09-05",
            "2005-04-18", "1970-12-25", "1988-06-08", "1992-02-14", "1975-08-30"
        ],
        "genero": [
            "Masculino", "Femenino", "Masculino", "Femenino", "Masculino",
            "Femenino", "Masculino", "Femenino", "Masculino", "Femenino"
        ],
        "telefono": [
            "3001234567", "3009876543", "3012345678", "3023456789", "3034567890",
            "3045678901", "3056789012", "3067890123", "3078901234", "3089012345"
        ],
        "correo": [
            "juan.perez@example.test", "maria.rodriguez@example.test", "carlos.gomez@example.test",
            "ana.martinez@example.test", "pedro.diaz@example.test", "laura.castro@example.test",
            "jorge.lopez@example.test", "patricia.vega@example.test", "alejandro.mendoza@example.test",
            "claudia.ortiz@example.test"
        ],
        "eps_codigo": ["EPS001", "EPS002", "EPS001", "EPS003", "EPS002", "EPS001", "EPS003", "EPS002", "EPS001", "EPS003"],
        "eps_nombre": [
            "Sanitas", "Sura", "Sanitas", "Coosalud", "Sura",
            "Sanitas", "Coosalud", "Sura", "Sanitas", "Coosalud"
        ],
        "ciudad": [
            "Bogota", "Medellin", "Cali", "Bogota", "Bucaramanga",
            "Cartagena", "Barranquilla", "Bogota", "Medellin", "Bogota"
        ],
        "prioridad": [
            "Alta", "Media", "Baja", "Alta", "Media",
            "Baja", "Alta", "Media", "Baja", "Alta"
        ],
        "estado": [
            "Pendiente", "Pendiente", "Atendido", "Pendiente", "En atencion",
            "Pendiente", "Atendido", "Pendiente", "Pendiente", "Pendiente"
        ],
        "fecha_creacion": [
            "2026-01-01 08:00:00", "2026-01-01 08:05:00", "2026-01-01 08:10:00",
            "2026-01-01 08:15:00", "2026-01-01 08:20:00", "2026-01-01 08:25:00",
            "2026-01-01 08:30:00", "2026-01-01 08:35:00", "2026-01-01 08:40:00",
            "2026-01-01 08:45:00"
        ],
        "fecha_actualizacion": [
            "2026-01-01 08:00:00", "2026-01-01 08:05:00", "2026-01-01 08:10:00",
            "2026-01-01 08:15:00", "2026-01-01 08:20:00", "2026-01-01 08:25:00",
            "2026-01-01 08:30:00", "2026-01-01 08:35:00", "2026-01-01 08:40:00",
            "2026-01-01 08:45:00"
        ],
    }
    
    df = pd.DataFrame(data)
    
    # Guardar como Excel
    output_path = Path(__file__).parent / "pacientes_ejemplo.xlsx"
    df.to_excel(output_path, index=False, sheet_name="Pacientes")
    
    print(f"Archivo Excel creado: {output_path}")
    print(f"   Total de registros: {len(df)}")
    print(f"   Columnas: {', '.join(df.columns)}")


if __name__ == "__main__":
    create_sample_excel()