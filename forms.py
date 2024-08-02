from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class Sags1Form(FlaskForm):
    nombre = StringField('Nombre Usuario', validators=[DataRequired()])
    apellido_paterno = StringField('Apellido Paterno', validators=[DataRequired()])
    apellido_materno = StringField('Apellido Materno', validators=[DataRequired()])
    tipo_usuario = StringField('Tipo Usuario', validators=[DataRequired()])
    nombre_de_usuario = StringField('Nombre de Usuario', validators=[DataRequired()])
    contraseña = StringField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Agregar Usuario')

class Sags2Form(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    presentación = StringField('Presentación', validators=[DataRequired()])
    fk_bodega = SelectField('Bodega', choices=[], validators=[DataRequired()])
    fk_proveedores = SelectField('Proveedor', choices=[], validators=[DataRequired()])
    fk_categoria = SelectField('Categoria', choices=[], validators=[DataRequired()])
    submit = SubmitField('Agregar Producto')

class SearchForm(FlaskForm):
    bodega = SelectField('Bodega', choices=[])
    categoria = SelectField('Categoría', choices=[])
    submit = SubmitField('Buscar')


class RegisterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido_paterno = StringField('Apellido Paterno', validators=[DataRequired()])
    apellido_materno = StringField('Apellido Materno', validators=[DataRequired()])
    tipo_usuario = SelectField('Tipo de Usuario', choices=[('admin', 'Administrador'), ('user', 'Almacenista')], validators=[DataRequired()])
    nombre_de_usuario = StringField('Nombre de Usuario', validators=[DataRequired()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('contraseña')])
    submit = SubmitField('Registrar')