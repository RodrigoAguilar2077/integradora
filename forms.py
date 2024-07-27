from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

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
    submit = SubmitField('Agregar Producto')
