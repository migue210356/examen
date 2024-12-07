import json
import sqlite3
from datetime import datetime

# Conectar a la base de datos SQLite (ajusta el nombre si es necesario)
conexion = sqlite3.connect('alumnos.db')  # Asegúrate de usar el nombre correcto de la DB
cursor = conexion.cursor()

# Abrir el archivo estudiante.json
with open('estudiante.json', 'r', encoding='utf-8') as archivo:  # Nombre corregido del archivo
    estudiantes = json.load(archivo)

# Insertar los estudiantes en la base de datos SQLite
for estudiante in estudiantes:
    # Asegúrate de que el JSON tenga los campos correctos que esperas en la tabla SQLite
    nombre = estudiante.get('nombre')
    apellido = estudiante.get('apellido')
    aprobado = estudiante.get('aprobado')
    nota = estudiante.get('nota')
    fecha = estudiante.get('fecha')

    # Convertir la fecha al formato adecuado para SQLite (si es necesario)
    if fecha:
        fecha = datetime.strptime(fecha['$date'], "%Y-%m-%dT%H:%M:%SZ").date()

    # La consulta SQL para insertar los datos en la tabla 'alumnos' (sin incluir el campo id si es autoincrementable)
    cursor.execute('''
        INSERT INTO alumnos (nombre, apellido, aprobado, nota, fecha) 
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, apellido, aprobado, nota, fecha))

# Guardar los cambios y cerrar la conexión
conexion.commit()
conexion.close()

print("Estudiantes insertados correctamente en SQLite.")
