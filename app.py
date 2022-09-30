from flask import Flask, render_template, request, redirect
from datetime import datetime

import pymysql

app=Flask(__name__)
PORT = 5000
DEBUG = False

@app.errorhandler(404)
def not_found(error):
    return "Not Found."

# Database Connection
def connection():
    """
    It connects to the database and returns the connection object
    :return: The connection to the database.
    """
    h = 'localhost'
    d = 'sistema' 
    u = 'root'
    p = 'SQL223010'
    conn = pymysql.connect(host=h, user=u, password=p, database=d)
    return conn

# Route index.html
@app.route('/')
def index():
    """
    We're creating a function called index() that will render the template empleados/index.html
    """
    
    sql = "SELECT * FROM empleados;"
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    
    empleados=cursor.fetchall()
    print(empleados)
    
    conn.commit()
    return render_template('empleados/index.html', empleados=empleados)

# Route destroy/delete users
@app.route("/destroy/<int:id>")
def destroy(id):
    """
    It deletes the employee with the given id from the database
    
    :param id: The id of the employee to be deleted
    :return: the redirect function, which is redirecting to the root route.
    """
    conn = connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM empleados WHERE id=%s", (id))
    conn.commit()
    return redirect('/')

# Route edit users info
@app.route('/edit/<int:id>')
def edit(id):
    """
    It takes the id of an employee, connects to the database, and then queries the database for the
    employee with that id
    
    :param id: The id of the employee to be edited
    :return: The template edit.html is being returned.
    """
    
    conn = connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id))
    
    empleados=cursor.fetchall()
    conn.commit()
    
    return render_template('empleados/edit.html', empleados=empleados)

# Route update users info
@app.route('/update', methods=['POST'])
def update():
    
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    
    _foto=request.files['txtFoto']
    
    id=request.form['txtID']
    
    sql = "UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s ;"
    
    datos=(_nombre, _correo, id)
    
    conn = connection()
    cursor = conn.cursor()
    
    cursor.execute(sql, datos)
    
    conn.commit()
    
    return redirect('/')

# Route create users
@app.route('/create')
def create():
    """
    It renders the create.html template
    :return: The create.html file
    """
    return render_template('empleados/create.html')

# Route next to create users
@app.route('/store', methods=['POST'])
def storage():
    """
    It takes the form data from the form, saves the file to the uploads folder, and then inserts the
    data into the database
    :return: The index.html file is being returned.
    """
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    
    _foto=request.files['txtFoto']
    
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
    
    sql = "INSERT INTO empleados(nombre, correo, foto) VALUES(%s, %s, %s);"
    
    datos=(_nombre, _correo, nuevoNombreFoto)
    
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return render_template('empleados/index.html')

if __name__ == '__main__':
    app.run(port=PORT,debug=True)
    connection()