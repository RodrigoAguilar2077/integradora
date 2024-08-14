import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, redirect, render_template, url_for, flash, session, send_file, make_response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
from fpdf import FPDF
from datetime import datetime 
import db
from forms import Sags1Form
from forms import Sags2Form
from forms import SearchForm
from forms import RegisterForm
from forms import EditarProductoForm
from forms import EliminarUsuarioForm

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
    return render_template('login2.html')

import psycopg2
from psycopg2.extras import RealDictCursor

# Ruta para el endpoint 'login_view'
@app.route('/login')
def login_view():
    return render_template('login2.html')

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
                SELECT * FROM usuarios WHERE correo = %s AND contrasena = %s
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
    return render_template('login2.html')

@app.route('/admin')
def admin():
    if session.get('logueado'):
        return render_template('base.html')
    else:
        return render_template('login2.html', mensaje="Acceso no autorizado")
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        tipo_usuario = form.tipo_usuario.data
        correo = form.nombre.data
        contraseña = form.contraseña.data

        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO vista_usuarios (nombre, tipo_usuario, correo, contraseña)
        VALUES (%s, %s, %s, %s)
        ''', (nombre, tipo_usuario, correo, contraseña))
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
    cursor.execute('''SELECT * FROM usuarios ORDER BY nombre_completo''')
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
        nombre_completo = form.nombre_completo.data
        tipo_usuario = form.tipo_usuario.data
        correo = form.correo.data
        contrasena = form.contrasena.data
        
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO usuarios (nombre_completo, tipo_usuario, correo, contrasena)
        VALUES (%s, %s, %s, %s)
        ''', (nombre_completo, tipo_usuario, correo, contrasena))
        conn.commit()
        cursor.close()
        db.desconectar(conn)
        
        flash('Usuario añadido correctamente')
        return redirect(url_for('usuarios'))

    return render_template('insertar_usuario.html', form=form)


@app.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
    try:
        id_usuario = request.form['id_usuario']

        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM usuarios 
            WHERE id_usuario = %s
        ''', (id_usuario,))
        conn.commit()
        cursor.close()
        db.desconectar(conn)

        flash('Usuario eliminado correctamente')
        return redirect(url_for('usuarios'))

    except Exception as e:
        print(f"Error al eliminar el usuario: {e}")
        flash('Error al eliminar el usuario')
        return redirect(url_for('usuarios'))


@app.route('/editar1_usuario/<int:id_usuario>', methods=['GET'])
def update1_usuario(id_usuario):
    conn = db.conectar()
    cursor = conn.cursor()

    # Recuperar los datos del usuario seleccionado
    cursor.execute('''SELECT * FROM usuarios WHERE id_usuario=%s''', (id_usuario,))
    datos = cursor.fetchone()
    cursor.close()
    db.desconectar(conn)

    return render_template('editar_usuario.html', datos=datos)

@app.route('/editar2_usuario/<int:id_usuario>', methods=['POST'])
def update2_usuario(id_usuario):
    try:
        nombre_completo = request.form['nombre_completo']
        tipo_usuario = request.form['tipo_usuario']
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        conn = db.conectar()
        cursor = conn.cursor()

        # Actualizar los datos del usuario
        cursor.execute('''
            UPDATE usuarios
            SET nombre_completo = %s, tipo_usuario = %s, correo = %s, contrasena = %s
            WHERE id_usuario = %s
        ''', (nombre_completo, tipo_usuario, correo, contrasena, id_usuario))
        
        conn.commit()
        cursor.close()
        db.desconectar(conn)

        flash('Usuario actualizado correctamente')
        return redirect(url_for('usuarios'))

    except Exception as e:
        print(f"Error al actualizar el usuario: {e}")
        flash('Error al actualizar el usuario')
        return redirect(url_for('usuarios'))


@app.route('/productos')
def productos():
    nombre = request.args.get('nombre')  # Obtener el nombre del parámetro de búsqueda
    conn = db.conectar()
    cursor = conn.cursor()

    if nombre:
        # Si se proporciona un nombre, filtra los resultados
        cursor.execute('''
            SELECT * FROM vista_productos
            WHERE nombre ILIKE %s
            ORDER BY id_producto
        ''', ('%' + nombre + '%',))
    else:
        # Si no se proporciona un nombre, muestra todos los productos
        cursor.execute('''
            SELECT * FROM vista_productos
            ORDER BY id_producto
        ''')
    
    datos = cursor.fetchall()

    cursor.close()
    db.desconectar(conn)

    return render_template('productos.html', datos=datos)


@app.route('/productos/total')
def productos_total():
    conn = db.conectar()
    cursor = conn.cursor()
    
    cursor.execute('''SELECT * FROM vista_productos ORDER BY id_producto''')
    datos = cursor.fetchall()
    
    cursor.close()
    db.desconectar(conn)
    
    return render_template('productos_total.html', datos=datos)


@app.route('/editar_producto/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    form = EditarProductoForm()

    # Conectar a la base de datos
    conn = db.conectar()
    cursor = conn.cursor()

    # Obtener opciones para los SelectField
    cursor.execute('SELECT id_bodega, nombre FROM bodega ORDER BY nombre')
    form.fk_bodega.choices = [(b[0], b[1]) for b in cursor.fetchall()]

    cursor.execute('SELECT id_marca, nombre FROM marca ORDER BY nombre')
    form.fk_marca.choices = [(m[0], m[1]) for m in cursor.fetchall()]

    cursor.execute('SELECT id_categoria, nombre FROM categoria ORDER BY nombre')
    form.fk_categoria.choices = [(c[0], c[1]) for c in cursor.fetchall()]

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                nombre = form.nombre.data
                cantidad = form.cantidad.data
                presentacion = form.presentacion.data
                fk_bodega = form.fk_bodega.data
                fk_marca = form.fk_marca.data
                fk_categoria = form.fk_categoria.data

                print(f"Datos recibidos: nombre={nombre}, cantidad={cantidad}, presentacion={presentacion}, "
                      f"fk_bodega={fk_bodega}, fk_marca={fk_marca}, fk_categoria={fk_categoria}")

                cursor.execute('''
                    UPDATE productos
                    SET nombre = %s, cantidad = %s, presentacion = %s, fk_bodega = %s, fk_marca = %s, fk_categoria = %s
                    WHERE id_producto = %s
                ''', (nombre, cantidad, presentacion, fk_bodega, fk_marca, fk_categoria, id_producto))

                print(f"Consulta SQL ejecutada con éxito.")

                conn.commit()
                flash('Producto actualizado correctamente')
                return redirect(url_for('productos'))
            
            except Exception as e:
                print(f"Error al actualizar el producto: {e}")
                flash('Error al actualizar el producto')
                return redirect(url_for('productos'))
        else:
            flash('Formulario no válido. Por favor, corrige los errores.')
            print("Formulario no válido.")
    else:
        cursor.execute('''
            SELECT nombre, cantidad, presentacion, fk_bodega, fk_marca, fk_categoria
            FROM productos
            WHERE id_producto = %s
        ''', (id_producto,))
        producto = cursor.fetchone()

        if producto:
            form.nombre.data = producto[0]
            form.cantidad.data = producto[1]
            form.presentacion.data = producto[2]
            form.fk_bodega.data = producto[3]
            form.fk_marca.data = producto[4]
            form.fk_categoria.data = producto[5]
            print(f"Producto encontrado: {producto}")
        else:
            flash('Producto no encontrado.')
            print("Producto no encontrado.")
            return redirect(url_for('productos'))

    cursor.close()
    db.desconectar(conn)

    return render_template('editar_producto.html', form=form, id_producto=id_producto)





@app.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    try:
        id_producto = request.form['id_producto']

        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM productos
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

    cursor.execute("SELECT id_marca, nombre FROM marca ORDER BY nombre")
    marcas = cursor.fetchall()
    form.fk_marca.choices = [(marca[0], marca[1]) for marca in marcas]

    cursor.execute("SELECT id_bodega, nombre FROM bodega ORDER BY nombre")
    bodegas = cursor.fetchall()
    form.fk_bodega.choices = [(bodega[0], bodega[1]) for bodega in bodegas]

    cursor.execute("SELECT id_categoria, nombre FROM categoria ORDER BY nombre")
    categoria = cursor.fetchall()
    form.fk_categoria.choices = [(categoria[0], categoria[1]) for categoria in categoria]

    cursor.close()
    db.desconectar(conn)

    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = form.cantidad.data
        presentacion = form.presentacion.data
        fk_marca = form.fk_marca.data
        fk_bodega = form.fk_bodega.data
        fk_categoria=form.fk_categoria.data

        print(f"Nombre: {nombre}, Cantidad: {cantidad}, Presentación: {presentacion}, Marca: {fk_marca}, Bodega: {fk_bodega}, Categoria: {fk_categoria} ")

        conn = db.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO productos (nombre, cantidad, presentacion, fk_marca, fk_bodega, fk_categoria)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (nombre, cantidad, presentacion, fk_marca, fk_bodega, fk_categoria))
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
        SELECT p.id_producto, p.nombre, p.cantidad, p.presentacion, b.nombre_bodega, c.nombre
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
    descargar_pdf = request.form.get('descargar_pdf', False)
    productos = []

    conn = db.conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT nombre, cantidad
        FROM productos
        WHERE fk_bodega = (SELECT id_bodega FROM bodega WHERE nombre = %s);
    ''', (bodega,))

    productos = cursor.fetchall()
    cursor.close()
    conn.close()

    if descargar_pdf:
        # Obtener la fecha actual
        fecha_actual = datetime.now().strftime("%d/%m/%Y")

        pdf = FPDF()
        pdf.add_page()

        # Título del PDF
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(200, 10, txt="Reporte de Productos en " + bodega, ln=True, align='C')

        # Agregar la fecha al PDF
        pdf.set_font('Arial', 'I', 12)
        pdf.cell(200, 10, txt="Fecha del Reporte: " + fecha_actual, ln=True, align='C')

        # Añadir productos al PDF
        pdf.set_font('Arial', '', 12)
        pdf.ln(10)  # Espacio adicional
        for producto in productos:
            pdf.cell(200, 10, txt=f"Producto: {producto[0]} - Cantidad: {producto[1]} pz", ln=True)

        # Enviar el PDF como respuesta
        response = make_response(pdf.output(dest='S').encode('latin1'))
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=reporte_productos.pdf'
        return response
    
    return render_template('reportes.html', productos=productos, bodega=bodega)


# ALMACENISTA
@app.route('/base_almacenista')
def base_almacenista():
    return render_template('base_almacenista.html')

@app.route('/productos2')
def productos2():
    nombre = request.args.get('nombre')  # Obtener el nombre del parámetro de búsqueda
    conn = db.conectar()
    cursor = conn.cursor()

    if nombre:
        # Si se proporciona un nombre, filtra los resultados
        cursor.execute('''
            SELECT * FROM vista_productos
            WHERE nombre ILIKE %s
            ORDER BY id_producto
        ''', ('%' + nombre + '%',))
    else:
        # Si no se proporciona un nombre, muestra todos los productos
        cursor.execute('''
            SELECT * FROM vista_productos
            ORDER BY id_producto
        ''')
    
    datos = cursor.fetchall()

    cursor.close()
    db.desconectar(conn)

    return render_template('productos2.html', datos=datos)

@app.route('/editar_producto2/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto2(id_producto):
    form = EditarProductoForm()

    # Conectar a la base de datos
    conn = db.conectar()
    cursor = conn.cursor()

    # Obtener opciones para los SelectField
    cursor.execute('SELECT id_bodega, nombre FROM bodega ORDER BY nombre')
    form.fk_bodega.choices = [(b[0], b[1]) for b in cursor.fetchall()]

    cursor.execute('SELECT id_marca, nombre FROM marca ORDER BY nombre')
    form.fk_marca.choices = [(m[0], m[1]) for m in cursor.fetchall()]

    cursor.execute('SELECT id_categoria, nombre FROM categoria ORDER BY nombre')
    form.fk_categoria.choices = [(c[0], c[1]) for c in cursor.fetchall()]

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                nombre = form.nombre.data
                cantidad = form.cantidad.data
                presentacion = form.presentacion.data
                fk_bodega = form.fk_bodega.data
                fk_marca = form.fk_marca.data
                fk_categoria = form.fk_categoria.data

                print(f"Datos recibidos: nombre={nombre}, cantidad={cantidad}, presentacion={presentacion}, "
                      f"fk_bodega={fk_bodega}, fk_marca={fk_marca}, fk_categoria={fk_categoria}")

                cursor.execute('''
                    UPDATE productos
                    SET nombre = %s, cantidad = %s, presentacion = %s, fk_bodega = %s, fk_marca = %s, fk_categoria = %s
                    WHERE id_producto = %s
                ''', (nombre, cantidad, presentacion, fk_bodega, fk_marca, fk_categoria, id_producto))

                print(f"Consulta SQL ejecutada con éxito.")

                conn.commit()
                flash('Producto actualizado correctamente')
                return redirect(url_for('productos'))
            
            except Exception as e:
                print(f"Error al actualizar el producto: {e}")
                flash('Error al actualizar el producto')
                return redirect(url_for('productos'))
        else:
            flash('Formulario no válido. Por favor, corrige los errores.')
            print("Formulario no válido.")
    else:
        cursor.execute('''
            SELECT nombre, cantidad, presentacion, fk_bodega, fk_marca, fk_categoria
            FROM productos
            WHERE id_producto = %s
        ''', (id_producto,))
        producto = cursor.fetchone()

        if producto:
            form.nombre.data = producto[0]
            form.cantidad.data = producto[1]
            form.presentacion.data = producto[2]
            form.fk_bodega.data = producto[3]
            form.fk_marca.data = producto[4]
            form.fk_categoria.data = producto[5]
            print(f"Producto encontrado: {producto}")
        else:
            flash('Producto no encontrado.')
            print("Producto no encontrado.")
            return redirect(url_for('productos2'))

    cursor.close()
    db.desconectar(conn)

    return render_template('editar_producto2.html', form=form, id_producto=id_producto)

@app.route('/insertar_producto2', methods=['GET', 'POST'])
def insertar_producto2():
    form = Sags2Form()

    conn = db.conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id_marca, nombre FROM marca ORDER BY nombre")
    marcas = cursor.fetchall()
    form.fk_marca.choices = [(marca[0], marca[1]) for marca in marcas]

    cursor.execute("SELECT id_bodega, nombre FROM bodega ORDER BY nombre")
    bodegas = cursor.fetchall()
    form.fk_bodega.choices = [(bodega[0], bodega[1]) for bodega in bodegas]

    cursor.execute("SELECT id_categoria, nombre FROM categoria ORDER BY nombre")
    categoria = cursor.fetchall()
    form.fk_categoria.choices = [(categoria[0], categoria[1]) for categoria in categoria]

    cursor.close()
    db.desconectar(conn)

    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = form.cantidad.data
        presentacion = form.presentacion.data
        fk_marca = form.fk_marca.data
        fk_bodega = form.fk_bodega.data
        fk_categoria=form.fk_categoria.data

        print(f"Nombre: {nombre}, Cantidad: {cantidad}, Presentación: {presentacion}, Marca: {fk_marca}, Bodega: {fk_bodega}, Categoria: {fk_categoria} ")

        conn = db.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO productos (nombre, cantidad, presentacion, fk_marca, fk_bodega, fk_categoria)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (nombre, cantidad, presentacion, fk_marca, fk_bodega, fk_categoria))
            conn.commit()
            flash('Producto añadido correctamente')
        except Exception as e:
            conn.rollback()
            flash(f'Error al añadir el producto: {str(e)}')
        finally:
            cursor.close()
            db.desconectar(conn)

        return redirect(url_for('productos2'))

    return render_template('insertar_producto.html', form=form)

@app.route('/buscar_productos2', methods=['GET', 'POST'])
def buscar_productos2():
    form = SearchForm()

    conn = db.conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id_bodega, nombre_bodega FROM bodega")
    bodegas = cursor.fetchall()
    form.bodega.choices = [(bodega[0], bodega[1]) for bodega in bodegas]

    cursor.execute("SELECT id_categoria, nombre FROM categoria ORDER BY nombre")
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

    return render_template('buscar_producto2.html', form=form, productos=productos)

@app.route('/bodegas2')
def bodegas2():
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM bodega ORDER BY id_bodega''')
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)
    return render_template('bodegas2.html', datos=datos)

@app.route('/editar_bodega2', methods=['GET', 'POST'])
def editar_bodega2():
    if request.method == 'POST':
        try:
            original_id_bodega = request.form['original_id_bodega']
            nombre_bodega = request.form['nombre_bodega']
            ubicacion = request.form['ubicacion']

            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE bodega
                SET nombre = %s, ubicacion = %s
                WHERE id_bodega = %s
            ''', (nombre, ubicacion, original_id_bodega))
            conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Error al actualizar la bodega: {e}")
            flash('Error al actualizar la bodega')
        finally:
            db.desconectar(conn)
        
        flash('Bodega actualizada correctamente')
        return redirect(url_for('bodegas2'))
    
    else:
        id_bodega = request.args.get('id_bodega')
        nombre = request.args.get('nombre')
        ubicacion = request.args.get('ubicacion')
        
        return render_template('editar_bodega2.html', 
                                id_bodega=id_bodega, 
                                nombre=nombre, 
                                ubicacion=ubicacion)


@app.route('/reportes2', methods=['GET', 'POST'])
def reportes2():
    bodega = request.form.get('bodega')
    productos = []
    conn = db.conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT nombre, cantidad
        FROM productos
        WHERE fk_bodega = (SELECT id_bodega FROM bodega WHERE nombre = %s);
    ''', (bodega,))
    
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('reportes2.html', productos=productos, bodega=bodega)

if __name__ == "__main__":
    app.secret_key="vramcorporation"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)