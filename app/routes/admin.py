from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required
from app import db
from app.forms.admin import FormacionForm, OrganizacionForm
from app.models import (SECCIONES, MensajeContacto, Organizacion, Formacion,
                        Perfil, Idioma, Experiencia, Capacitacion, Reconocimiento)
from app.models.trayectoria import FormacionTraduccion

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@login_required
def panel():
    return render_template(
        "admin/panel.html",
        mensajes=MensajeContacto.query.order_by(MensajeContacto.fecha.desc()).all(),
        secciones={nombre: modelo.todas() for nombre, modelo in SECCIONES.items()},
        organizaciones=Organizacion.query.order_by(Organizacion.nombre).all(),
    )


@admin_bp.route("/organizaciones/nueva", methods=["GET", "POST"])
@login_required
def crear_organizacion():
    form = OrganizacionForm()
    if form.validate_on_submit():
        Organizacion(
            nombre=form.nombre.data.strip(),
            sitio_web=form.sitio_web.data or None,
            ubicacion=form.ubicacion.data or None,
        ).guardar()
        flash("Organización creada.", "success")
        return redirect(url_for("admin.panel"))
    return render_template("admin/form.html", titulo="Nueva organización", form=form)


@admin_bp.route("/organizaciones/<int:ident>/eliminar", methods=["POST"])
@login_required
def eliminar_organizacion(ident):
    organizacion = db.get_or_404(Organizacion, ident)
    modelos_vinculados = (Formacion, Experiencia, Capacitacion, Reconocimiento)
    if any(modelo.query.filter_by(id_organizacion=ident).first() for modelo in modelos_vinculados):
        flash("No se puede eliminar: la organización todavía está vinculada a registros.", "danger")
        return redirect(url_for("admin.panel"))
    organizacion.eliminar()
    flash("Organización eliminada.", "success")
    return redirect(url_for("admin.panel"))


@admin_bp.route("/formaciones/nueva", methods=["GET", "POST"])
@login_required
def crear_formacion():
    form = FormacionForm()
    organizaciones = Organizacion.query.order_by(Organizacion.nombre).all()
    form.id_organizacion.choices = [(o.id_organizacion, o.nombre) for o in organizaciones]
    if form.validate_on_submit():
        perfil = Perfil.query.first()
        idioma = Idioma.query.filter_by(codigo_iso="es").first()
        if not perfil or not idioma:
            flash("Hace falta un perfil y el idioma español para crear una formación.", "danger")
            return redirect(url_for("admin.panel"))
        formacion = Formacion(
            id_perfil=perfil.id_perfil,
            id_organizacion=form.id_organizacion.data,
            anio_inicio=form.anio_inicio.data,
            anio_fin=form.anio_fin.data,
            estado=form.estado.data,
            visible=True,
        )
        formacion.traducciones.append(FormacionTraduccion(
            id_idioma=idioma.id_idioma,
            titulo=form.titulo.data.strip(),
            descripcion=form.descripcion.data or None,
        ))
        formacion.guardar()
        flash("Formación creada.", "success")
        return redirect(url_for("admin.panel"))
    return render_template("admin/form.html", titulo="Nueva formación", form=form)


@admin_bp.route("/formaciones/<int:ident>/eliminar", methods=["POST"])
@login_required
def eliminar_formacion(ident):
    formacion = db.get_or_404(Formacion, ident)
    formacion.eliminar()
    flash("Formación eliminada.", "success")
    return redirect(url_for("admin.panel"))


@admin_bp.route("/<seccion>/<int:ident>/visible", methods=["POST"])
@login_required
def alternar_visible(seccion, ident):
    # Una sola ruta para TODAS las secciones (POLIMORFISMO): el modelo se elige por nombre.
    modelo = SECCIONES.get(seccion) or abort(404)
    item = modelo.obtener_o_404(ident)
    item.visible = not item.visible
    item.guardar()
    flash("Actualizado.", "success")
    return redirect(url_for("admin.panel"))


@admin_bp.route("/mensajes/<int:id>/leido", methods=["POST"])
@login_required
def marcar_leido(id):
    m = db.get_or_404(MensajeContacto, id)
    m.leido = True
    m.guardar()
    return redirect(url_for("admin.panel"))
