import psycopg2
from flask import Flask, request, redirect, render_template, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
import db
from forms import Sags1Form
from forms import Sags2Form

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY']= 'SUPER SECRETO'
# csrf = CSRFProtect(app)


@app.route('/')
def index():
    return render_template('base.html')

@app.errorhandler(404)
def error404(error):
    return render_template('404.html')

@app.route('/usuarios')
def usuarios():
    conn = db.conectar()
    #crear un cursor (objeto para recorrer las tablas)

    cursor = conn.cursor()
    #ejecutar un consulta en postgres
    cursor.execute('''SELECT * FROM vista_usuarios ORDER BY nombre''')
    #recuperar la informacion
    datos=cursor.fetchall()
    #cerrar cursor y conexion a la base de datos
    cursor.close()
    db.desconectar(conn)
    return render_template('usuarios.html', datos=datos)

@app.route('/insertar_usuario', methods=['GET', 'POST'])
def insertar_usuario():
    form = Sags1Form()
    if form.validate_on_submit():
        nombre = form.nombre.data
        apellido_paterno=form.apellido_paterno.data
        apellido_materno=form.apellido_materno.data
        tipo_usuario=form.tipo_usuario.data
        nombre_de_usuario=form.nombre_de_usuario.data
        contraseña=form-contraseña.data
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO libro (nombre, apellido_paterno, apellido_materno, tipo_usuario, nombre_de_usuario, contraseña)
                     VALUES (%s, %s, %s, %s, %s, %s)
        ''', (nombre, apellido_paterno, apellido_materno, tipo_usuario, nombre_de_usuario, contraseña))
        conn.commit()
        cursor.close()
        db.desconectar(conn)  # Cambio aquí
        flash('LIBRO AÑADIDO CORRECTAMENTE')
        return redirect(url_for('usuarios'))  # Corrige el nombre de la función para redirigir

    return render_template('insertar_producto.html', form=form)




@app.route('/productos')
def productos():
    conn = db.conectar()
    #crear un cursor (objeto para recorrer las tablas)

    cursor = conn.cursor()
    #ejecutar un consulta en postgres
    cursor.execute('''SELECT * FROM vista_productos ORDER BY id_producto''')
    #recuperar la informacion
    datos=cursor.fetchall()
    #cerrar cursor y conexion a la base de datos
    cursor.close()
    db.desconectar(conn)
    return render_template('productos.html', datos=datos)

@app.route('/insertar_producto', methods=['GET', 'POST'])
def insertar_producto():
    form = Sags2Form()
    if form.validate_on_submit():
        nombre_producto = form.nombre_producto.data
        cantidad=form.cantidad.data
        presentacion=form.presentacin.data
        fk_proveedor = form.fk_proveedor.data  # Cambio aquí
        fk_bodega = form.fk_bodega.data
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO libro (nombre_producto, cantidad, presentacion, fk_proveedor, fk_bodega)
                     VALUES (%s, %s, %s, %s, %s)
        ''', (nombre_producto, cantidad, presentacion, fk_proveedor, fk_bodega))
        conn.commit()
        cursor.close()
        db.desconectar(conn)  # Cambio aquí
        flash('LIBRO AÑADIDO CORRECTAMENTE')
        return redirect(url_for('productos'))  # Corrige el nombre de la función para redirigir

    return render_template('insertar_producto.html', form=form)

@app.route('/bodegas')
def bodegas():
    conn = db.conectar()
    #conectar con la base de datos

    #crear un cursor (objeto para recorrer las tablas)

    cursor = conn.cursor()
    #ejecutar un consulta en postgres
    cursor.execute('''SELECT * FROM bodega ORDER BY id_bodega''')
    #recuperar la informacion
    datos=cursor.fetchall()
    #cerrar cursor y conexion a la base de datos
    cursor.close()
    db.desconectar(conn)

    return render_template('bodegas.html', datos=datos)

@app.route('/reportes')
def reportes():
    conn = db.conectar()
    #crear un cursor (objeto para recorrer las tablas)

    cursor = conn.cursor()
    #ejecutar un consulta en postgres
    cursor.execute('''SELECT * FROM vista_usuarios''')
    #recuperar la informacion
    datos=cursor.fetchall()
    #cerrar cursor y conexion a la base de datos
    cursor.close()
    db.desconectar(conn)
    return render_template('usuarios.html', datos=datos)