"""Formularios del panel de administración (Flask-WTF).

Idea general: hay UN formulario por sección, pero todos heredan de SeccionForm, que sabe
cargar un registro en el formulario (al editar) y pasar los datos del formulario al
registro (al guardar). Cada formulario solo declara sus campos y dos listas:
  - CAMPOS: columnas de la tabla principal (ej. anio_inicio, estado).
  - CAMPOS_TRADUCCION: columnas de la tabla *_traduccion en español (ej. titulo).
"""
from flask_wtf import FlaskForm
from wtforms import (BooleanField, IntegerField, SelectField, SelectMultipleField,
                     StringField, TextAreaField)
from wtforms.validators import (DataRequired, Length, NumberRange, Optional, URL,
                                ValidationError)

from app.models import Idioma, Organizacion, Tecnologia

SIN_ORGANIZACION = 0   # valor del desplegable cuando el campo es opcional ("— Ninguna —")


def _organizaciones(opcional=False):
    opciones = [(o.id_organizacion, o.nombre) for o in Organizacion.query.order_by(Organizacion.nombre)]
    return ([(SIN_ORGANIZACION, "— Ninguna —")] + opciones) if opcional else opciones


def _anio(etiqueta):
    return IntegerField(etiqueta, validators=[Optional(), NumberRange(min=1900, max=2100)])


def _url(etiqueta):
    return StringField(etiqueta, validators=[Optional(), URL(), Length(max=2048)])


class SeccionForm(FlaskForm):
    # ABSTRACCIÓN: define QUÉ hace cualquier formulario del panel (cargar, aplicar,
    # preparar) sin saber de qué sección es. Las subclases solo declaran sus campos.
    CAMPOS = ()
    CAMPOS_TRADUCCION = ()

    def preparar(self):
        """Llena las opciones de los desplegables. Las subclases lo sobrescriben si lo necesitan."""

    def cargar(self, item):
        """Copia los valores del registro al formulario (pantalla de editar)."""
        for nombre in self.CAMPOS:
            valor = getattr(item, nombre)
            if isinstance(self[nombre], SelectField) and valor is None:
                valor = SIN_ORGANIZACION
            self[nombre].data = valor
        if self.CAMPOS_TRADUCCION and item.t:
            for nombre in self.CAMPOS_TRADUCCION:
                self[nombre].data = getattr(item.t, nombre)

    def aplicar(self, item, id_idioma_es=None):
        """Copia los valores del formulario al registro (antes de guardar)."""
        for nombre in self.CAMPOS:
            setattr(item, nombre, self._valor(nombre))
        if self.CAMPOS_TRADUCCION:
            traduccion = item.traduccion_en(id_idioma_es)
            for nombre in self.CAMPOS_TRADUCCION:
                setattr(traduccion, nombre, self._valor(nombre))

    def _valor(self, nombre):
        """Normaliza lo que escribió el usuario: texto vacío -> NULL, "— Ninguna —" -> NULL."""
        campo = self[nombre]
        dato = campo.data
        if isinstance(dato, str):
            dato = dato.strip() or None
        if isinstance(campo, SelectField) and dato == SIN_ORGANIZACION:
            dato = None
        return dato


class ConOrdenVisible:
    """Campos que comparten todas las secciones que heredan de Seccion en los modelos."""
    orden = IntegerField("Orden", default=0, validators=[Optional(), NumberRange(min=0, max=999)])
    visible = BooleanField("Visible en el portfolio", default=True)


class ValidarAnios:
    """Evita guardar un año de fin anterior al de inicio."""
    def validate_anio_fin(self, campo):
        if campo.data and self.anio_inicio.data and campo.data < self.anio_inicio.data:
            raise ValidationError("El año de fin no puede ser anterior al de inicio.")


# ---------------------------------------------------------------------------------------
# HERENCIA: cada formulario hereda de SeccionForm (y de los mixins) todo el comportamiento.
# ---------------------------------------------------------------------------------------

class PerfilForm(SeccionForm):
    CAMPOS = ("nombre", "apellido", "ubicacion", "foto_url", "cv_url")
    CAMPOS_TRADUCCION = ("titular", "sobre_mi")
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    apellido = StringField("Apellido", validators=[DataRequired(), Length(max=100)])
    titular = StringField("Titular (ej. Estudiante de Programación)", validators=[Optional(), Length(max=180)])
    sobre_mi = TextAreaField("Sobre mí (separá párrafos con una línea en blanco)", validators=[Optional()])
    ubicacion = StringField("Ubicación", validators=[Optional(), Length(max=150)])
    foto_url = StringField("Foto (URL o ruta en static)", validators=[Optional(), Length(max=2048)])
    cv_url = StringField("CV (ruta, ej. /static/docs/cv.pdf)", validators=[Optional(), Length(max=2048)])


class ContactoAdminForm(ConOrdenVisible, SeccionForm):
    CAMPOS = ("tipo", "valor", "url", "orden", "visible")
    tipo = SelectField("Tipo", choices=[("email", "Email"), ("telefono", "Teléfono"), ("github", "GitHub"),
                                        ("linkedin", "LinkedIn"), ("sitio_web", "Sitio web"), ("otro", "Otro")])
    valor = StringField("Valor (lo que se muestra)", validators=[DataRequired(), Length(max=255)])
    url = StringField("Enlace (mailto:, tel:, https://...)", validators=[Optional(), Length(max=2048)])


class OrganizacionForm(SeccionForm):
    CAMPOS = ("nombre", "sitio_web", "ubicacion")
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=180)])
    sitio_web = _url("Sitio web")
    ubicacion = StringField("Ubicación", validators=[Optional(), Length(max=180)])


class FormacionForm(ValidarAnios, ConOrdenVisible, SeccionForm):
    CAMPOS = ("id_organizacion", "anio_inicio", "anio_fin", "estado", "orden", "visible")
    CAMPOS_TRADUCCION = ("titulo", "descripcion")
    id_organizacion = SelectField("Institución", coerce=int, validators=[DataRequired()])
    titulo = StringField("Título", validators=[DataRequired(), Length(max=180)])
    descripcion = TextAreaField("Descripción", validators=[Optional()])
    anio_inicio = _anio("Año de inicio")
    anio_fin = _anio("Año de finalización (vacío = actualidad)")
    estado = SelectField("Estado", choices=[("planificada", "Planificada"), ("en_curso", "En curso"),
                                            ("finalizada", "Finalizada")])

    # POLIMORFISMO: misma firma que en SeccionForm, distinto comportamiento.
    def preparar(self):
        self.id_organizacion.choices = _organizaciones()


class ExperienciaForm(ValidarAnios, ConOrdenVisible, SeccionForm):
    CAMPOS = ("id_organizacion", "tipo", "anio_inicio", "anio_fin", "actualmente", "orden", "visible")
    CAMPOS_TRADUCCION = ("puesto", "descripcion", "logros")
    puesto = StringField("Puesto / rol", validators=[DataRequired(), Length(max=180)])
    id_organizacion = SelectField("Organización", coerce=int)
    tipo = SelectField("Tipo", choices=[("laboral", "Laboral"), ("academica", "Académica"),
                                        ("colaboracion", "Colaboración"), ("voluntariado", "Voluntariado")])
    anio_inicio = _anio("Año de inicio")
    anio_fin = _anio("Año de fin")
    actualmente = BooleanField("La hago actualmente")
    descripcion = TextAreaField("Descripción", validators=[Optional()])
    logros = TextAreaField("Logros", validators=[Optional()])

    def preparar(self):
        self.id_organizacion.choices = _organizaciones(opcional=True)

    def validate_actualmente(self, campo):
        # La tabla tiene un CHECK: si es la actual, no puede tener año de fin.
        if campo.data and self.anio_fin.data:
            raise ValidationError("Si la hacés actualmente, dejá vacío el año de fin.")


class CapacitacionForm(ValidarAnios, ConOrdenVisible, SeccionForm):
    CAMPOS = ("id_organizacion", "tipo", "estado", "anio_inicio", "anio_fin", "horas",
              "certificado_url", "orden", "visible")
    CAMPOS_TRADUCCION = ("nombre", "descripcion")
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=180)])
    id_organizacion = SelectField("Entidad", coerce=int)
    tipo = SelectField("Tipo", choices=[("certificacion", "Certificación"), ("curso", "Curso")])
    estado = SelectField("Estado", choices=[("finalizada", "Finalizada"), ("en_curso", "En curso"),
                                            ("planificada", "Planificada")])
    anio_inicio = _anio("Año de inicio")
    anio_fin = _anio("Año de fin")
    horas = IntegerField("Horas", validators=[Optional(), NumberRange(min=0, max=10000)])
    certificado_url = StringField("Certificado (ruta, ej. /static/docs/...)", validators=[Optional(), Length(max=2048)])
    descripcion = TextAreaField("Descripción", validators=[Optional()])

    def preparar(self):
        self.id_organizacion.choices = _organizaciones(opcional=True)


class ReconocimientoForm(ConOrdenVisible, SeccionForm):
    CAMPOS = ("id_organizacion", "anio", "orden", "visible")
    CAMPOS_TRADUCCION = ("nombre", "resultado", "descripcion")
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=180)])
    resultado = StringField("Resultado (ej. Primer puesto)", validators=[Optional(), Length(max=180)])
    id_organizacion = SelectField("Organización", coerce=int)
    anio = _anio("Año")
    descripcion = TextAreaField("Descripción", validators=[Optional()])

    def preparar(self):
        self.id_organizacion.choices = _organizaciones(opcional=True)


class ObjetivoForm(ConOrdenVisible, SeccionForm):
    CAMPOS = ("estado", "prioridad", "anio_objetivo", "orden", "visible")
    CAMPOS_TRADUCCION = ("titulo", "descripcion")
    titulo = StringField("Objetivo", validators=[DataRequired(), Length(max=180)])
    estado = SelectField("Estado", choices=[("pendiente", "Pendiente"), ("en_progreso", "En progreso"),
                                            ("cumplido", "Cumplido")])
    prioridad = IntegerField("Prioridad (1 a 5)", default=3, validators=[DataRequired(), NumberRange(min=1, max=5)])
    anio_objetivo = _anio("Año objetivo")
    descripcion = TextAreaField("Descripción", validators=[Optional()])


class TecnologiaForm(SeccionForm):
    """Catálogo de tecnologías (Python, Flask...). El nivel se carga aparte en 'tecnologias'."""
    CAMPOS = ("nombre", "tipo", "icono")
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    tipo = SelectField("Tipo", choices=[("lenguaje", "Lenguaje"), ("framework", "Framework"),
                                        ("libreria", "Librería"), ("herramienta", "Herramienta"),
                                        ("marcado", "Marcado"), ("base_datos", "Base de datos"), ("otro", "Otro")])
    icono = StringField("Ícono FontAwesome (ej. fa-brands fa-python)", validators=[Optional(), Length(max=80)])


class PerfilTecnologiaForm(ConOrdenVisible, SeccionForm):
    CAMPOS = ("id_tecnologia", "nivel", "orden", "visible")
    id_tecnologia = SelectField("Tecnología", coerce=int, validators=[DataRequired()])
    nivel = SelectField("Nivel", choices=[("principiante", "Principiante"), ("basico", "Básico"),
                                          ("intermedio", "Intermedio"), ("avanzado", "Avanzado")])

    def preparar(self):
        self.id_tecnologia.choices = [(t.id_tecnologia, t.nombre)
                                      for t in Tecnologia.query.order_by(Tecnologia.nombre)]


class PerfilIdiomaForm(SeccionForm):
    CAMPOS = ("id_idioma", "nivel")
    id_idioma = SelectField("Idioma", coerce=int, validators=[DataRequired()])
    nivel = SelectField("Nivel", choices=[(n, n) for n in ("nativo", "A1", "A2", "B1", "B2", "C1", "C2")])

    def preparar(self):
        self.id_idioma.choices = [(i.id_idioma, i.nombre) for i in Idioma.query.order_by(Idioma.nombre)]


class ProyectoForm(ValidarAnios, ConOrdenVisible, SeccionForm):
    CAMPOS = ("estado", "anio_inicio", "anio_fin", "repositorio_url", "demo_url", "imagen_url",
              "orden", "visible")
    CAMPOS_TRADUCCION = ("nombre", "descripcion", "objetivo", "rol")
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=180)])
    descripcion = TextAreaField("Descripción", validators=[Optional()])
    objetivo = TextAreaField("Objetivo", validators=[Optional()])
    rol = StringField("Tu rol", validators=[Optional(), Length(max=120)])
    estado = SelectField("Estado", choices=[("finalizado", "Finalizado"), ("en_desarrollo", "En desarrollo"),
                                            ("planificado", "Planificado"), ("pausado", "Pausado")])
    anio_inicio = _anio("Año de inicio")
    anio_fin = _anio("Año de fin")
    repositorio_url = _url("Repositorio (https://...)")
    demo_url = _url("Demo (https://...)")
    imagen_url = StringField("Imagen (URL o ruta en static)", validators=[Optional(), Length(max=2048)])
    tecnologias = SelectMultipleField("Tecnologías usadas (Ctrl + clic para elegir varias)", coerce=int)

    def preparar(self):
        self.tecnologias.choices = [(t.id_tecnologia, t.nombre)
                                    for t in Tecnologia.query.order_by(Tecnologia.nombre)]

    # POLIMORFISMO: reutiliza cargar/aplicar del padre (super()) y agrega la relación N:M.
    def cargar(self, item):
        super().cargar(item)
        self.tecnologias.data = [t.id_tecnologia for t in item.tecnologias]

    def aplicar(self, item, id_idioma_es=None):
        super().aplicar(item, id_idioma_es)
        ids = self.tecnologias.data or []
        item.tecnologias = Tecnologia.query.filter(Tecnologia.id_tecnologia.in_(ids)).all() if ids else []


class CodigoForm(ConOrdenVisible, SeccionForm):
    """Habilidades y conocimientos técnicos: en la base solo guardan un código."""
    CAMPOS = ("codigo", "orden", "visible")
    codigo = StringField("Código (ej. trabajo_en_equipo)", validators=[DataRequired(), Length(max=80)])
