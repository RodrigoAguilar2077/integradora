from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class Sags1Form(FlaskForm):
    nombre_usuario = StringField('Nombre Usuario', validators=[DataRequired()])
    apellido_paterno = IntegerField('Apellido Paterno', validators=[DataRequired()])
    apellido_materno = IntegerField('Apellido Materno', validators=[DataRequired()])
    tipo_usuario = IntegerField('Tipo Usuario', validators=[DataRequired()])
    contraseña = StringField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Agregar Usuario')

class Sags2Form(FlaskForm):
    nombre_producto = StringField('Nombre', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    presentacion = StringField('Presentación', validators=[DataRequired()])
    bodega = StringField('Bodega', validators=[DataRequired()])
    proveedor = StringField('Proveedor', validators=[DataRequired()])
    categoria = StringField('Categoría', validators=[DataRequired()])
    submit = SubmitField('Agregar Producto')
