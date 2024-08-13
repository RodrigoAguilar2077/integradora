from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class Sags1Form(FlaskForm):
    nombre_completo = StringField('Nombre', validators=[DataRequired()])
    tipo_usuario = StringField('Tipo Usuario', validators=[DataRequired()])
    correo = StringField('Correo', validators=[DataRequired()])
    contrasena = StringField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Agregar Usuario')

class Sags2Form(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    presentacion = StringField('Presentación', validators=[DataRequired()])
    fk_bodega = SelectField('Bodega', choices=[], validators=[DataRequired()])
    fk_marca = SelectField('Marca', choices=[], validators=[DataRequired()])
    fk_categoria = SelectField('Categoria', choices=[], validators=[DataRequired()])
    submit = SubmitField('Agregar Producto')

class SearchForm(FlaskForm):
    bodega = SelectField('Bodega', choices=[])
    categoria = SelectField('Categoría', choices=[])
    submit = SubmitField('Buscar')


class RegisterForm(FlaskForm):
    nombre_completo = StringField('Nombre', validators=[DataRequired()])
    tipo_usuario = SelectField('Tipo de Usuario', choices=[('Administrador', 'Administrador'), ('Almacenista', 'Almacenista')], validators=[DataRequired()])
    correo = StringField('Nombre de Usuario', validators=[DataRequired()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('contraseña')])
    submit = SubmitField('Registrar')

class EditarProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    presentacion = StringField('Presentación', validators=[DataRequired()])
    fk_bodega = SelectField('Bodega', choices=[], validators=[DataRequired()], coerce=int)
    fk_marca = SelectField('Marca', choices=[], validators=[DataRequired()], coerce=int)
    fk_categoria = SelectField('Categoría', choices=[], validators=[DataRequired()], coerce=int)
    submit = SubmitField('Actualizar Producto')

class EliminarUsuarioForm(FlaskForm):
    nombre = StringField('Nombre')
    tipo_usuario = StringField('Tipo de Usuario')
    nombre_usuario = StringField('Nombre de Usuario')
    submit = SubmitField('Eliminar')