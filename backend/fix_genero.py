import sqlite3

conn = sqlite3.connect('patients.db')
cursor = conn.cursor()

# Update 'Otro' -> 'Prefiere no informar'
cursor.execute("UPDATE patients SET genero = 'Prefiere no informar' WHERE genero = 'Otro'")
otro_count = cursor.rowcount

# Update 'No binario' -> 'Prefiere no informar'
cursor.execute("UPDATE patients SET genero = 'Prefiere no informar' WHERE genero = 'No binario'")
nobinario_count = cursor.rowcount

# Update 'Prefiere no responder' -> 'Prefiere no informar'
cursor.execute("UPDATE patients SET genero = 'Prefiere no informar' WHERE genero = 'Prefiere no responder'")
responder_count = cursor.rowcount

conn.commit()

# Verify
cursor.execute('SELECT DISTINCT genero FROM patients')
print('Valores de genero en BD:', [r[0] for r in cursor.fetchall()])
print(f'Actualizados: {otro_count} Otro, {nobinario_count} No binario, {responder_count} Prefiere no responder -> todos a Prefiere no informar')
conn.close()