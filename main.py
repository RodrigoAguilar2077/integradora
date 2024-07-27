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
        apellido_paterno = form.apellido_paterno.data
        apellido_materno = form.apellido_materno.data
        tipo_usuario = form.tipo_usuario.data
        nombre_de_usuario = form.nombre_de_usuario.data
        contraseña = form.contraseña.data  # Corrección aquí
        
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO libro (nombre, apellido_paterno, apellido_materno, tipo_usuario, nombre_de_usuario, contraseña)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (nombre, apellido_paterno, apellido_materno, tipo_usuario, nombre_de_usuario, contraseña))
        conn.commit()
        cursor.close()
        db.desconectar(conn)
        
        flash('Usuario añadido correctamente')
        return redirect(url_for('usuarios'))

    return render_template('insertar_usuario.html', form=form)


    return render_template('insertar_producto.html', form=form)

@app.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
    try:
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        tipo_usuario = request.form['tipo_usuario']
        nombre_usuario = request.form['nombre_usuario']

        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM vista_usuarios 
            WHERE nombre = %s AND apellido_paterno = %s AND apellido_materno = %s AND tipo_usuario = %s AND nombre_de_usuario = %s
        ''', (nombre, apellido_paterno, apellido_materno, tipo_usuario, nombre_usuario))
        conn.commit()
        cursor.close()
        db.desconectar(conn)

        flash('Usuario eliminado correctamente')
        return redirect(url_for('usuarios'))

    except Exception as e:
        print(f"Error al eliminar el usuario: {e}")
        flash('Error al eliminar el usuario')
        return redirect(url_for('usuarios'))


@app.route('/editar_usuario', methods=['GET', 'POST'])
def editar_usuario():
    if request.method == 'POST':
        try:
            # Obtén los valores originales de los campos
            original_nombre = request.form['original_nombre']
            original_apellido_paterno = request.form['original_apellido_paterno']
            original_apellido_materno = request.form['original_apellido_materno']
            original_tipo_usuario = request.form['original_tipo_usuario']
            original_nombre_usuario = request.form['original_nombre_usuario']

            # Obtén los nuevos valores de los campos
            nombre = request.form['nombre']
            apellido_paterno = request.form['apellido_paterno']
            apellido_materno = request.form['apellido_materno']
            tipo_usuario = request.form['tipo_usuario']
            nombre_usuario = request.form['nombre_usuario']
            contraseña = request.form['contraseña']

            # Conecta a la base de datos y realiza la actualización
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE vista_usuarios 
                SET nombre = %s, apellido_paterno = %s, apellido_materno = %s, tipo_usuario = %s, nombre_de_usuario = %s, contraseña = %s
                WHERE nombre = %s AND apellido_paterno = %s AND apellido_materno = %s AND tipo_usuario = %s AND nombre_de_usuario = %s
            ''', (nombre, apellido_paterno, apellido_materno, tipo_usuario, nombre_usuario, contraseña, 
                  original_nombre, original_apellido_paterno, original_apellido_materno, original_tipo_usuario, original_nombre_usuario))
            conn.commit()
            cursor.close()
            db.desconectar(conn)

            flash('Usuario actualizado correctamente')
            return redirect(url_for('usuarios'))

        except Exception as e:
            print(f"Error al actualizar el usuario: {e}")
            flash('Error al actualizar el usuario')
            return redirect(url_for('usuarios'))

    else:
        nombre = request.args.get('nombre')
        apellido_paterno = request.args.get('apellido_paterno')
        apellido_materno = request.args.get('apellido_materno')
        tipo_usuario = request.args.get('tipo_usuario')
        nombre_usuario = request.args.get('nombre_usuario')
        
        return render_template('editar_usuario.html', 
                               nombre=nombre, 
                               apellido_paterno=apellido_paterno, 
                               apellido_materno=apellido_materno, 
                               tipo_usuario=tipo_usuario, 
                               nombre_usuario=nombre_usuario)



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

@app.route('/editar_producto', methods=['GET', 'POST'])
def editar_producto():
    if request.method == 'POST':
        try:
            original_id_producto = request.form['original_id_producto']
            nombre_producto = request.form['nombre_producto']
            cantidad = request.form['cantidad']
            presentacion = request.form['presentacion']
            nombre_bodega = request.form['nombre_bodega']
            nombre_proveedor = request.form['nombre_proveedor']
            categoria = request.form['categoria']

            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE vista_productos
                SET nombre_producto = %s, cantidad = %s, presentacion = %s, nombre_bodega = %s, nombre_proveedor = %s, categoria = %s
                WHERE id_producto = %s
            ''', (nombre_producto, cantidad, presentacion, nombre_bodega, nombre_proveedor, categoria, original_id_producto))
            conn.commit()
            cursor.close()
            db.desconectar(conn)

            flash('Producto actualizado correctamente')
            return redirect(url_for('productos'))

        except Exception as e:
            print(f"Error al actualizar el producto: {e}")
            flash('Error al actualizar el producto')
            return redirect(url_for('productos'))
    
    else:
        id_producto = request.args.get('id_producto')
        nombre_producto = request.args.get('nombre_producto')
        cantidad = request.args.get('cantidad')
        presentacion = request.args.get('presentacion')
        nombre_bodega = request.args.get('nombre_bodega')
        nombre_proveedor = request.args.get('nombre_proveedor')
        categoria = request.args.get('categoria')
        
        return render_template('editar_producto.html', 
                               id_producto=id_producto, 
                               nombre_producto=nombre_producto, 
                               cantidad=cantidad, 
                               presentacion=presentacion, 
                               nombre_bodega=nombre_bodega, 
                               nombre_proveedor=nombre_proveedor, 
                               categoria=categoria)


@app.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    try:
        id_producto = request.form['id_producto']

        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM producto
            WHERE id_producto = %s
        ''', (id_producto,))
        conn.commit()
        cursor.close()
        db.desconectar(conn)

        flash('Producto eliminado correctamente')
        return redirect(url_for('productos'))

    except Exception as e:
        print(f"Error al eliminar el producto: {e}")
        flash('Error al eliminar el producto')
        return redirect(url_for('productos'))



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
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM bodega ORDER BY id_bodega''')
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)
    return render_template('bodegas.html', datos=datos)


@app.route('/editar_bodega', methods=['GET', 'POST'])
def editar_bodega():
    if request.method == 'POST':
        try:
            original_id_bodega = request.form['original_id_bodega']
            nombre_bodega = request.form['nombre_bodega']
            ubicacion = request.form['ubicacion']

            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE bodega
                SET nombre_bodega = %s, ubicacion = %s
                WHERE id_bodega = %s
            ''', (nombre_bodega, ubicacion, original_id_bodega))
            conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Error al actualizar la bodega: {e}")
            flash('Error al actualizar la bodega')
        finally:
            db.desconectar(conn)
        
        flash('Bodega actualizada correctamente')
        return redirect(url_for('bodegas'))
    
    else:
        id_bodega = request.args.get('id_bodega')
        nombre_bodega = request.args.get('nombre_bodega')
        ubicacion = request.args.get('ubicacion')
        
        return render_template('editar_bodega.html', 
                               id_bodega=id_bodega, 
                               nombre_bodega=nombre_bodega, 
                               ubicacion=ubicacion)

@app.route('/eliminar_bodega', methods=['POST'])
def eliminar_bodega():
    try:
        id_bodega = request.form['id_bodega']

        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM bodega
            WHERE id_bodega = %s
        ''', (id_bodega,))
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Error al eliminar la bodega: {e}")
        flash('Error al eliminar la bodega')
    finally:
        db.desconectar(conn)
    
    flash('Bodega eliminada correctamente')
    return redirect(url_for('bodegas'))


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


if __name__ == "__main__":
    app.secret_key="vramcorporation"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
