from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash
from datetime import datetime
from db import connection

import os

app=Flask(__name__)
PORT = 5000
DEBUG = False

app.secret_key=('SECRET_KEY')

CARPETA = os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

@app.errorhandler(404)
def not_found(error):
    return "Not Found."

# Route index.html
@app.route('/')
def index():
    """
    We're creating a function called index() that will render the template empleados/index.html
    """
    
    sql = "SELECT * FROM empleados;"
    db = connection()
    cursor = db.cursor()
    cursor.execute(sql)
    
    empleados=cursor.fetchall()
    print(empleados)
    
    db.commit()
    return render_template('empleados/index.html', empleados=empleados)

# Route destroy/delete users
@app.route("/destroy/<int:id>")
def destroy(id):
    """
    It deletes the employee with the given id from the database
    
    :param id: The id of the employee to be deleted
    :return: the redirect function, which is redirecting to the root route.
    """
    db = connection()
    cursor = db.cursor()
    
    cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    
    cursor.execute("DELETE FROM empleados WHERE id=%s", (id))
    db.commit()
    return redirect('/')

# Route edit users info
@app.route('/edit/<int:id>')
def edit(id):
    """
    Toma la identificación de un empleado, se conecta a la base de datos y luego consulta la base de datos para el
    empleado con esa identificación.
    
    :param id: El id del empleado a editar
    :return: Se devuelve la plantilla edit.html.
    """
    
    db = connection()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id))
    
    empleados=cursor.fetchall()
    db.commit()
    
    return render_template('empleados/edit.html', empleados=empleados)

# Route update users info
@app.route('/update', methods=['POST'])
def update():
    """
    Estamos actualizando la base de datos con los nuevos valores del formulario
    :return: la función de redirección, que está redirigiendo al usuario a la página raíz.
    """
    
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    
    _foto=request.files['txtFoto']
    
    id=request.form['txtID']
    
    sql = "UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s ;"
    
    datos=(_nombre, _correo, id)
    
    db = connection()
    cursor = db.cursor()
    
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    
    if _foto.filename!='':
        
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
        
        cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)
        fila = cursor.fetchall()
        
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE empleados SET foto=%s WHERE id=%s", (nuevoNombreFoto, id))
        db.commit()
    
    cursor.execute(sql, datos)
    
    db.commit()
    
    return redirect('/')

# Route create users
@app.route('/create')
def create():
    """
    Representa la plantilla create.html
    :return: El archivo create.html
    """
    return render_template('empleados/create.html')

# Route next to create users
@app.route('/store', methods=['POST'])
def storage():
    """
    Toma los datos del formulario, guarda el archivo en la carpeta de carga y luego inserta el
    datos en la base de datos
    :return: El archivo index.html está siendo devuelto.
    """
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    
    _foto=request.files['txtFoto']
    
    if _nombre=='' or _correo=='' or _foto=='':
        flash('¡¡ Recuerda llenar todos los campos !!')
        return redirect(url_for('create'))

    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
    
    sql = "INSERT INTO empleados(nombre, correo, foto) VALUES(%s, %s, %s);"
    
    datos=(_nombre, _correo, nuevoNombreFoto)
    
    db = connection()
    cursor = db.cursor()
    cursor.execute(sql, datos)
    db.commit()
    return render_template('empleados/confirmacion.html')

if __name__ == '__main__':
    app.run(port=PORT,debug=True)
    connection()