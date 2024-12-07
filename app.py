import sqlite3
from flask import Flask, render_template, abort, request, redirect, url_for
from db import get_db_connection
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/estudiantes', methods=['GET'])
def get_all_alumno():
    conn = get_db_connection()
    alumnos = conn.execute('SELECT * FROM alumnos').fetchall()  # Se debe usar "fetchall" en vez de "fetchone" para obtener todos los registros.
    conn.close()
    return render_template('alumnos/alumnos.html', alumnos=alumnos)

@app.route('/alumno/<int:alumno_id>', methods=['GET'])
def get_one_alumno(alumno_id):
    conn = get_db_connection()
    alumno = conn.execute('SELECT * FROM alumnos WHERE id = ?', (alumno_id,)).fetchone()
    conn.close()
    return render_template('alumnos/alumno.html', alumno=alumno)

@app.route('/alumno/create', methods=['GET','alumno'])
def create_one_alumno():
    if request.method == 'alumno':
        nombre = request.form['nombre']
        apellido = request.form['apellido'] 
        conn = get_db_connection()
        conn.execute('INSERT INTO alumnos (nombre, apellido) VALUES (?, ?)', (nombre, apellido))
        conn.commit()
        conn.close()
        return redirect(url_for('get_all_alumno'))

    return render_template('alumnos/create.html')

@app.route('/alumno/edit/<int:id>', methods=['GET', 'alumno'])
def edit_one_alumno(id):
    conn = get_db_connection()
    alumno = conn.execute('SELECT * FROM alumnos WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if request.method == 'alumno':
        nombre = request.form['nombre']
        apellido = request.form['apellido']

        conn = get_db_connection()
        conn.execute('UPDATE alumnos SET nombre = ?, apellido = ? WHERE id = ?', (nombre, apellido, id))
        conn.commit()
        conn.close()
        return redirect(url_for('get_all_alumno'))

    elif request.method == 'GET':
        return render_template('alumnos/edit.html', alumno=alumno)

@app.route('/alumno/delete/<alumno_id>', methods=['alumno'])
def delete_one_alumno(alumno_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM alumnos WHERE id = ?', (alumno_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('get_all_alumno'))

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')

