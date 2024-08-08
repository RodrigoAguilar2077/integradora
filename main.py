import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, redirect, render_template, url_for, flash, session, send_file
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
import db
from forms import Sags1Form
from forms import Sags2Form
from forms import SearchForm
from forms import RegisterForm

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY']= 'SUPER SECRETO'
# csrf = CSRFProtect(app)

# ADMINISTRADOR
@app.route('/base')
def base():
    return render_template('base.html')

app.secret_key = "vramcorporation"
@app.route('/')
def index():
    if 'tipo_usuario' not in session or session['tipo_usuario'] != 'Administrador':
        flash('Acceso denegado. Debes ser ADMINISTRADOR para acceder a esta página.')
        return redirect(url_for('login'))
    return render_template('login.html')

import psycopg2
from psycopg2.extras import RealDictCursor

# Ruta para el endpoint 'login_view'
@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        _correo = request.form['username']
        _password = request.form['password']

        conn = None
        cursor = None
        cuenta = None

        try:
            conn = db.conectar()  # Conexión a la base de datos usando tu método
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('''
                SELECT * FROM usuarios WHERE usuario_usuario = %s AND contrasena_usuario = %s
            ''', (_correo, _password))
            cuenta = cursor.fetchone()

        except Exception as e:
            print(f"Error: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        if cuenta:
            if cuenta['tipo_usuario'] == 'Administrador':
                session['tipo_usuario'] = 'Administrador'
                return redirect(url_for('base'))
            elif cuenta['tipo_usuario'] == 'Almacenista':
                session['tipo_usuario'] = 'Almacenista'
                return redirect(url_for('base_almacenista'))
            else:
                return redirect(url_for('login_view'))
        else:
            return redirect(url_for('login_view'))
    return render_template('login.html')

@app.route('/admin')
def admin():
    if session.get('logueado'):
        return render_template('base.html')
    else:
        return render_template('login.html', mensaje="Acceso no autorizado")
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        apellido_paterno = form.apellido_paterno.data
        apellido_materno = form.apellido_materno.data
        tipo_usuario = form.tipo_usuario.data
        nombre_de_usuario = form.nombre_de_usuario.data
        contraseña = form.contraseña.data

        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO vista_usuarios (nombre, apellido_paterno, apellido_materno, tipo_usuario, nombre_de_usuario, contraseña)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (nombre, apellido_paterno, apellido_materno, tipo_usuario, nombre_de_usuario, contraseña))
        conn.commit()
        cursor.close()
        db.desconectar(conn)

        flash('Te has registrado con éxito!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


app.route('/admin')
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
        contraseña = form.contraseña.data
        
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO vista_usuarios (nombre, apellido_paterno, apellido_materno, tipo_usuario, nombre_de_usuario, contraseña)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (nombre, apellido_paterno, apellido_materno, tipo_usuario, nombre_de_usuario, contraseña))
        conn.commit()
        cursor.close()
        db.desconectar(conn)
        
        flash('Usuario añadido correctamente')
        return redirect(url_for('usuarios'))

    return render_template('insertar_usuario.html', form=form)


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
            original_nombre = request.form['original_nombre']
            original_apellido_paterno = request.form['original_apellido_paterno']
            original_apellido_materno = request.form['original_apellido_materno']
            original_tipo_usuario = request.form['original_tipo_usuario']
            original_nombre_usuario = request.form['original_nombre_usuario']

            nombre = request.form['nombre']
            apellido_paterno = request.form['apellido_paterno']
            apellido_materno = request.form['apellido_materno']
            tipo_usuario = request.form['tipo_usuario']
            nombre_usuario = request.form['nombre_usuario']
            contraseña = request.form['contraseña']

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

    conn = db.conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id_proveedor, nombre_proveedor FROM proveedores")
    proveedores = cursor.fetchall()
    form.fk_proveedores.choices = [(proveedor[0], proveedor[1]) for proveedor in proveedores]

    cursor.execute("SELECT id_bodega, nombre_bodega FROM bodega")
    bodegas = cursor.fetchall()
    form.fk_bodega.choices = [(bodega[0], bodega[1]) for bodega in bodegas]

    cursor.execute("SELECT id_categoria, nombre FROM categoria")
    categoria = cursor.fetchall()
    form.fk_categoria.choices = [(categoria[0], categoria[1]) for categoria in categoria]

    cursor.close()
    db.desconectar(conn)

    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = form.cantidad.data
        presentación = form.presentación.data
        fk_proveedores = form.fk_proveedores.data
        fk_bodega = form.fk_bodega.data
        fk_categoria=form.fk_categoria.data

        print(f"Nombre: {nombre}, Cantidad: {cantidad}, Presentación: {presentación}, Proveedor: {fk_proveedores}, Bodega: {fk_bodega}, Categoria: {fk_categoria} ")

        conn = db.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO productos (nombre, cantidad, presentación, fk_proveedores, fk_bodega, fk_categoria)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (nombre, cantidad, presentación, fk_proveedores, fk_bodega, fk_categoria))
            conn.commit()
            flash('Producto añadido correctamente')
        except Exception as e:
            conn.rollback()
            flash(f'Error al añadir el producto: {str(e)}')
        finally:
            cursor.close()
            db.desconectar(conn)

        return redirect(url_for('productos'))

    return render_template('insertar_producto.html', form=form)

@app.route('/buscar_productos', methods=['GET', 'POST'])
def buscar_productos():
    form = SearchForm()

    conn = db.conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id_bodega, nombre_bodega FROM bodega")
    bodegas = cursor.fetchall()
    form.bodega.choices = [(bodega[0], bodega[1]) for bodega in bodegas]

    cursor.execute("SELECT id_categoria, nombre FROM categoria")
    categorias = cursor.fetchall()
    form.categoria.choices = [(categoria[0], categoria[1]) for categoria in categorias]

    cursor.close()
    db.desconectar(conn)

    productos = []

    if form.validate_on_submit():
        bodega_id = form.bodega.data
        categoria_id = form.categoria.data

        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT p.id_producto, p.nombre, p.cantidad, p.presentación, b.nombre_bodega, c.nombre
        FROM productos p
        JOIN bodega b ON p.fk_bodega = b.id_bodega
        JOIN categoria c ON p.fk_categoria = c.id_categoria
        WHERE p.fk_bodega = %s AND p.fk_categoria = %s
        ''', (bodega_id, categoria_id))
        productos = cursor.fetchall()
        cursor.close()
        db.desconectar(conn)

    return render_template('buscar_productos.html', form=form, productos=productos)


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


@app.route('/reportes', methods=['GET', 'POST'])
def reportes():
    bodega = request.form.get('bodega')
    productos = []
    conn = db.conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT nombre, cantidad
        FROM productos
        WHERE fk_bodega = (SELECT id_bodega FROM bodega WHERE nombre_bodega = %s);
    ''', (bodega,))
    
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('reportes.html', productos=productos, bodega=bodega)


# ALMACENISTA
@app.route('/base_almacenista')
def base_almacenista():
    return render_template('base_almacenista.html')

@app.route('/productos2')
def productos2():
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
    return render_template('productos2.html', datos=datos)

@app.route('/editar_producto2', methods=['GET', 'POST'])
def editar_producto2():
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

        return render_template('editar_producto2.html',
                                id_producto=id_producto,
                                nombre_producto=nombre_producto,
                                cantidad=cantidad,
                                presentacion=presentacion,
                                nombre_bodega=nombre_bodega,
                                nombre_proveedor=nombre_proveedor,
                                categoria=categoria)

@app.route('/insertar_producto2', methods=['GET', 'POST'])
def insertar_producto2():
    form = Sags2Form()

    conn = db.conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id_proveedor, nombre_proveedor FROM proveedores")
    proveedores = cursor.fetchall()
    form.fk_proveedores.choices = [(proveedor[0], proveedor[1]) for proveedor in proveedores]

    cursor.execute("SELECT id_bodega, nombre_bodega FROM bodega")
    bodegas = cursor.fetchall()
    form.fk_bodega.choices = [(bodega[0], bodega[1]) for bodega in bodegas]

    cursor.execute("SELECT id_categoria, nombre FROM categoria")
    categoria = cursor.fetchall()
    form.fk_categoria.choices = [(categoria[0], categoria[1]) for categoria in categoria]

    cursor.close()
    db.desconectar(conn)

    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = form.cantidad.data
        presentación = form.presentación.data
        fk_proveedores = form.fk_proveedores.data
        fk_bodega = form.fk_bodega.data
        fk_categoria=form.fk_categoria.data

        print(f"Nombre: {nombre}, Cantidad: {cantidad}, Presentación: {presentación}, Proveedor: {fk_proveedores}, Bodega: {fk_bodega}, Categoria: {fk_categoria} ")

        conn = db.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO productos (nombre, cantidad, presentación, fk_proveedores, fk_bodega, fk_categoria)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (nombre, cantidad, presentación, fk_proveedores, fk_bodega, fk_categoria))
            conn.commit()
            flash('Producto añadido correctamente')
        except Exception as e:
            conn.rollback()
            flash(f'Error al añadir el producto: {str(e)}')
        finally:
            cursor.close()
            db.desconectar(conn)

        return redirect(url_for('productos'))

    return render_template('insertar_producto2.html', form=form)

@app.route('/buscar_productos2', methods=['GET', 'POST'])
def buscar_productos2():
    form = SearchForm()

    conn = db.conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id_bodega, nombre_bodega FROM bodega")
    bodegas = cursor.fetchall()
    form.bodega.choices = [(bodega[0], bodega[1]) for bodega in bodegas]

    cursor.execute("SELECT id_categoria, nombre FROM categoria")
    categorias = cursor.fetchall()
    form.categoria.choices = [(categoria[0], categoria[1]) for categoria in categorias]

    cursor.close()
    db.desconectar(conn)

    productos = []

    if form.validate_on_submit():
        bodega_id = form.bodega.data
        categoria_id = form.categoria.data

        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT p.id_producto, p.nombre, p.cantidad, p.presentación, b.nombre_bodega, c.nombre
        FROM productos p
        JOIN bodega b ON p.fk_bodega = b.id_bodega
        JOIN categoria c ON p.fk_categoria = c.id_categoria
        WHERE p.fk_bodega = %s AND p.fk_categoria = %s
        ''', (bodega_id, categoria_id))
        productos = cursor.fetchall()
        cursor.close()
        db.desconectar(conn)

    return render_template('buscar_productos2.html', form=form, productos=productos)

@app.route('/bodegas2')
def bodegas2():
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM bodega ORDER BY id_bodega''')
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)
    return render_template('bodegas2.html', datos=datos)

@app.route('/reportes2', methods=['GET', 'POST'])
def reportes2():
    bodega = request.form.get('bodega')
    productos = []
    conn = db.conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT nombre, cantidad
        FROM productos
        WHERE fk_bodega = (SELECT id_bodega FROM bodega WHERE nombre_bodega = %s);
    ''', (bodega,))
    
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('reportes2.html', productos=productos, bodega=bodega)

if __name__ == "__main__":
    app.secret_key="vramcorporation"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)