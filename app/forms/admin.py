from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, URL


class OrganizacionForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=180)])
    sitio_web = StringField("Sitio web", validators=[Optional(), URL(), Length(max=2048)])
    ubicacion = StringField("Ubicación", validators=[Optional(), Length(max=180)])


class FormacionForm(FlaskForm):
    id_organizacion = SelectField("Organización", coerce=int, validators=[DataRequired()])
    titulo = StringField("Título", validators=[DataRequired(), Length(max=180)])
    descripcion = TextAreaField("Descripción", validators=[Optional()])
    anio_inicio = IntegerField("Año de inicio", validators=[Optional(), NumberRange(min=1900, max=2100)])
    anio_fin = IntegerField("Año de finalización", validators=[Optional(), NumberRange(min=1900, max=2100)])
    estado = SelectField(
        "Estado",
        choices=[("planificada", "Planificada"), ("en_curso", "En curso"), ("finalizada", "Finalizada")],
        validators=[DataRequired()],
    )
