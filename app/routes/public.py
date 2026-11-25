import os
from flask import (Blueprint, render_template, redirect, url_for, flash,
                   send_from_directory, current_app)
from app.forms.contacto import ContactoForm
from app.models import (Perfil, PerfilIdioma, Contacto, Formacion, Experiencia, Proyecto,
                        Capacitacion, Reconocimiento, ObjetivoAcademico, PerfilTecnologia,
                        Habilidad, ConocimientoTecnico, MensajeContacto)

public_bp = Blueprint("public", __name__)

# Habilidades/conocimientos/áreas guardan un `codigo` estable; la etiqueta visible
# se resuelve acá (solo español). Completá el diccionario con tus códigos.
ETIQUETAS = {
    # "trabajo_en_equipo": "Trabajo en equipo",
    # "desarrollo_web": "Desarrollo web",
}


@public_bp.app_template_filter("etiqueta")
def etiqueta(codigo):
    return ETIQUETAS.get(codigo, codigo.replace("_", " ").capitalize())


@public_bp.route("/")
def index():
    # Todo viaja a Jinja2 (for/if en los templates). Un solo perfil: el del propietario.
    perfil = Perfil.query.first()
    return render_template(
        "index.html",
        perfil=perfil,
        contactos=Contacto.visibles(),
        formaciones=Formacion.visibles(),
        experiencias=Experiencia.visibles(),
        proyectos=Proyecto.visibles(),
        capacitaciones=Capacitacion.visibles(),
        reconocimientos=Reconocimiento.visibles(),
        objetivos=ObjetivoAcademico.visibles(),
        tecnologias=PerfilTecnologia.visibles(),
        habilidades=Habilidad.visibles(),
        conocimientos=ConocimientoTecnico.visibles(),
        idiomas=PerfilIdioma.query.filter_by(id_perfil=perfil.id_perfil).all(),
        form_contacto=ContactoForm(),
    )


@public_bp.route("/contacto", methods=["POST"])
def contacto():
    form = ContactoForm()
    if form.validate_on_submit():
        MensajeContacto(nombre=form.nombre.data, email=form.email.data,
                        mensaje=form.mensaje.data).guardar()
        flash("¡Mensaje enviado! Gracias por escribirme.", "success")
    else:
        flash("Revisá los datos del formulario.", "danger")
    return redirect(url_for("public.index") + "#contacto")


@public_bp.route("/cv")
def descargar_cv():
    # Si el perfil tiene cv_url se redirige ahí; si no, se sirve app/static/cv/cv.pdf
    perfil = Perfil.query.first()
    if perfil and perfil.cv_url:
        return redirect(perfil.cv_url)
    carpeta = os.path.join(current_app.static_folder, "cv")
    return send_from_directory(carpeta, "cv.pdf", as_attachment=True)
