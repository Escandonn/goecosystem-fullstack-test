"""Script para generar el archivo Excel de ejemplo con pacientes."""

import pandas as pd
from pathlib import Path


def create_sample_excel():
    """Crea un archivo Excel de ejemplo con datos de pacientes."""
    
    data = {
        "TipoDocumento": ["CC", "CC", "CC", "CE", "CC", "TI", "CC", "CC", "CC", "CC"],
        "NumeroDocumento": [
            "1001234567", "1007654321", "1012345678", "1023456789", "1034567890",
            "1045678901", "1056789012", "1067890123", "1078901234", "1089012345"
        ],
        "Nombres": [
            "JUAN CARLOS", "MARIA ELENA", "CARLOS ANDRES", "ANA LUCIA", "PEDRO JOSE",
            "LAURA FERNANDA", "JORGE ENRIQUE", "PATRICIA DEL PILAR", "ALEJANDRO JOSE", "CLAUDIA PATRICIA"
        ],
        "Apellidos": [
            "PEREZ GOMEZ", "RODRIGUEZ LOPEZ", "GOMEZ VARGAS", "MARTINEZ SANCHEZ", "DIAZ RAMIREZ",
            "CASTRO MORENO", "LOPEZ GUERRA", "VEGA HERRERA", "MENDOZA TORRES", "ORTIZ RAMOS"
        ],
        "FechaNacimiento": [
            "1985-03-15", "1990-07-22", "1978-11-30", "1995-01-10", "1982-09-05",
            "2005-04-18", "1970-12-25", "1988-06-08", "1992-02-14", "1975-08-30"
        ],
        "Sexo": ["M", "F", "M", "F", "M", "F", "M", "F", "M", "F"],
        "Telefono": [
            "3001234567", "3009876543", "3012345678", "3023456789", "3034567890",
            "3045678901", "3056789012", "3067890123", "3078901234", "3089012345"
        ],
        "Correo": [
            "juan.perez@email.com", "maria.rodriguez@email.com", "carlos.gomez@email.com",
            "ana.martinez@email.com", "pedro.diaz@email.com", "laura.castro@email.com",
            "jorge.lopez@email.com", "patricia.vega@email.com", "alejandro.mendoza@email.com",
            "claudia.ortiz@email.com"
        ],
        "Direccion": [
            "Cra 1 #2-3 Bogota", "Calle 5 #10-15 Medellin", "Av Caracas #45-67 Cali",
            "Transversal 7 #23-89 Bogota", "Calle 12 #8-45 Bucaramanga", "Cra 15 #3-67 Cartagena",
            "Av Boyaca #56-23 Barranquilla", "Calle 80 #15-90 Bogota", "Av 80 #45-12 Medellin",
            "Calle 100 #20-45 Bogota"
        ],
        "Estado": [True, True, True, True, True, True, True, True, False, True]
    }
    
    df = pd.DataFrame(data)
    
    # Guardar como Excel
    output_path = Path(__file__).parent / "pacientes_ejemplo.xlsx"
    df.to_excel(output_path, index=False, sheet_name="Pacientes")
    
    print(f"✅ Archivo Excel creado: {output_path}")
    print(f"   Total de registros: {len(df)}")


if __name__ == "__main__":
    create_sample_excel()