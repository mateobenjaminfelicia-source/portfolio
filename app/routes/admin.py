from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from app import db
from app.forms import admin as formularios
from app.models import (SECCIONES, MensajeContacto, Organizacion, Perfil, PerfilIdioma, Idioma,
                        Contacto, Formacion, Experiencia, Proyecto, Capacitacion, Reconocimiento,
                        ObjetivoAcademico, Tecnologia, PerfilTecnologia, Habilidad, ConocimientoTecnico)

admin_bp = Blueprint("admin", __name__)


@admin_bp.before_request
@login_required
def proteger_admin():
    # Todo /admin exige sesión: cualquier ruta nueva queda protegida aunque nos olvidemos
    # del decorador. Si no hay sesión, login_required redirige al login.
    pass


# Registro de lo que se puede editar desde el panel: nombre en la URL -> (modelo, formulario).
# Los nombres coinciden con los que usan los templates en controles('formaciones', ...).
EDITABLES = {
    "perfil": (Perfil, formularios.PerfilForm),
    "contactos": (Contacto, formularios.ContactoAdminForm),
    "idiomas": (PerfilIdioma, formularios.PerfilIdiomaForm),
    "formaciones": (Formacion, formularios.FormacionForm),
    "experiencias": (Experiencia, formularios.ExperienciaForm),
    "proyectos": (Proyecto, formularios.ProyectoForm),
    "capacitaciones": (Capacitacion, formularios.CapacitacionForm),
    "reconocimientos": (Reconocimiento, formularios.ReconocimientoForm),
    "objetivos": (ObjetivoAcademico, formularios.ObjetivoForm),
    "tecnologias": (PerfilTecnologia, formularios.PerfilTecnologiaForm),
    "habilidades": (Habilidad, formularios.CodigoForm),
    "conocimientos": (ConocimientoTecnico, formularios.CodigoForm),
    # Catálogos: se cargan antes, porque los desplegables de otras secciones salen de acá.
    "organizaciones": (Organizacion, formularios.OrganizacionForm),
    "catalogo_tecnologias": (Tecnologia, formularios.TecnologiaForm),
}
NO_SE_CREAN_NI_BORRAN = {"perfil"}   # hay un único perfil; borrarlo arrastraría todo el portfolio

# Nombre visible e ícono de FontAwesome de cada sección (menú lateral, tarjetas y títulos).
SECCIONES_UI = {
    "perfil": ("Perfil", "fa-regular fa-id-card"),
    "contactos": ("Contactos", "fa-solid fa-at"),
    "idiomas": ("Idiomas", "fa-solid fa-language"),
    "formaciones": ("Estudios", "fa-solid fa-graduation-cap"),
    "experiencias": ("Experiencia", "fa-solid fa-briefcase"),
    "proyectos": ("Proyectos", "fa-solid fa-diagram-project"),
    "capacitaciones": ("Certificaciones", "fa-solid fa-certificate"),
    "reconocimientos": ("Reconocimientos", "fa-solid fa-award"),
    "objetivos": ("Objetivos", "fa-solid fa-bullseye"),
    "tecnologias": ("Tecnologías", "fa-solid fa-code"),
    "habilidades": ("Habilidades", "fa-solid fa-people-group"),
    "conocimientos": ("Conocimientos", "fa-solid fa-brain"),
    "organizaciones": ("Organizaciones", "fa-solid fa-building-columns"),
    "catalogo_tecnologias": ("Catálogo de tecnologías", "fa-solid fa-layer-group"),
}


@admin_bp.context_processor
def datos_panel():
    # Solo para los templates de este blueprint (panel y formularios).
    return {"SECCIONES_UI": SECCIONES_UI}


def _volver(seccion):
    """Después de guardar: si veníamos del panel volvemos ahí; si no, al portfolio."""
    if request.args.get("desde") == "panel":
        return redirect(url_for("admin.panel") + f"#{seccion}")
    return redirect(url_for("public.index"))


def _seccion(nombre):
    if nombre not in EDITABLES:
        abort(404)   # nadie puede apuntar a una tabla que no esté en la lista
    return EDITABLES[nombre]


def _id_espanol():
    idioma = Idioma.query.filter_by(codigo_iso="es").first()
    return idioma.id_idioma if idioma else None


def _guardar(item):
    """Guarda y, si la base rechaza el cambio (dato duplicado o en uso), deshace y avisa."""
    try:
        item.guardar()
        return True
    except IntegrityError:
        db.session.rollback()
        flash("La base rechazó el cambio: puede haber un dato repetido o un registro relacionado.", "danger")
        return False


@admin_bp.route("/")
def panel():
    return render_template(
        "admin/panel.html",
        mensajes=MensajeContacto.query.order_by(MensajeContacto.fecha.desc()).all(),
        secciones={nombre: modelo.todas() for nombre, modelo in SECCIONES.items()},
        organizaciones=Organizacion.query.order_by(Organizacion.nombre).all(),
        catalogo=Tecnologia.query.order_by(Tecnologia.nombre).all(),
        idiomas=PerfilIdioma.query.all(),
        perfil_admin=Perfil.query.first(),
    )


# --- CRUD GENÉRICO ------------------------------------------------------------------------
# POLIMORFISMO: las mismas tres rutas sirven para TODAS las secciones. Eligen el modelo y el
# formulario por el nombre de la URL, y cada formulario sabe cargar/aplicar sus propios campos.

@admin_bp.route("/<seccion>/nuevo", methods=["GET", "POST"])
def nuevo(seccion):
    if seccion in NO_SE_CREAN_NI_BORRAN:
        abort(404)
    modelo, clase_form = _seccion(seccion)
    form = clase_form()
    form.preparar()
    if form.validate_on_submit():
        item = modelo()
        if hasattr(item, "id_perfil"):                 # todo lo personal cuelga del único perfil
            item.id_perfil = Perfil.query.first().id_perfil
        form.aplicar(item, _id_espanol())
        if _guardar(item):
            flash("Guardado.", "success")
            return _volver(seccion)
    return render_template("admin/form.html", form=form, seccion=seccion,
                           titulo=f"Nuevo · {SECCIONES_UI[seccion][0]}")


@admin_bp.route("/<seccion>/<int:ident>/editar", methods=["GET", "POST"])
def editar(seccion, ident):
    modelo, clase_form = _seccion(seccion)
    item = modelo.obtener_o_404(ident)
    form = clase_form()
    form.preparar()
    if form.validate_on_submit():
        form.aplicar(item, _id_espanol())
        if _guardar(item):
            flash("Cambios guardados.", "success")
            return _volver(seccion)
    elif not form.is_submitted():
        form.cargar(item)                               # GET: el formulario arranca con los datos actuales
    return render_template("admin/form.html", form=form, seccion=seccion,
                           titulo=f"Editar · {SECCIONES_UI[seccion][0]}")


@admin_bp.route("/<seccion>/<int:ident>/eliminar", methods=["POST"])
def eliminar(seccion, ident):
    if seccion in NO_SE_CREAN_NI_BORRAN:
        abort(404)
    modelo, _ = _seccion(seccion)
    item = modelo.obtener_o_404(ident)
    try:
        item.eliminar()
        flash("Eliminado.", "success")
    except IntegrityError:
        db.session.rollback()
        flash("No se puede eliminar: hay otros registros que dependen de este.", "danger")
    return _volver(seccion)


@admin_bp.route("/<seccion>/<int:ident>/visible", methods=["POST"])
def alternar_visible(seccion, ident):
    # Una sola ruta para TODAS las secciones (POLIMORFISMO): el modelo se elige por nombre.
    modelo = SECCIONES.get(seccion) or abort(404)
    item = modelo.obtener_o_404(ident)
    item.visible = not item.visible
    item.guardar()
    flash("Actualizado.", "success")
    return redirect(url_for("admin.panel") + f"#{seccion}")


@admin_bp.route("/mensajes/<int:ident>/leido", methods=["POST"])
def marcar_leido(ident):
    m = db.get_or_404(MensajeContacto, ident)
    m.leido = True
    m.guardar()
    return redirect(url_for("admin.panel"))
