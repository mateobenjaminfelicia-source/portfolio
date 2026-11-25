"""
demo_app.py — SOLO PARA PREVISUALIZAR EL FRONT (borrar cuando esté el backend real).
Usa datos de ejemplo del diseño de Figma y formularios "falsos", sin BD ni Flask-WTF.
Correr:  pip install flask  ->  python demo_app.py  ->  http://127.0.0.1:5000
Modo edición (admin):  http://127.0.0.1:5000/?admin=1
"""
from types import SimpleNamespace as NS
from flask import Flask, render_template, request, redirect, url_for, flash
from markupsafe import Markup, escape

app = Flask(__name__)
app.secret_key = "demo"
app.jinja_env.globals["csrf_token"] = lambda: "demo-token"   # con Flask-WTF real esto lo da CSRFProtect


class Campo:
    """Imita un campo de WTForms: se 'llama' para dibujar el input."""
    def __init__(self, nombre, tipo="StringField", html="input", input_type="text"):
        self.name, self.type, self.html, self.input_type = nombre, tipo, html, input_type
        self.label = NS(text=nombre.capitalize()); self.errors = []
    def __call__(self, **kw):
        attrs = " ".join(f'{k}="{escape(v)}"' for k, v in kw.items() if v is not True and k != "rows")
        if self.html == "textarea":
            return Markup(f'<textarea name="{self.name}" rows="{kw.get("rows", 4)}" {attrs}></textarea>')
        return Markup(f'<input name="{self.name}" type="{self.input_type}" {attrs}>')


class FormFalso:
    def __init__(self, **campos):
        self.__dict__.update(campos); self._c = list(campos.values()); self.errors = {}
    def hidden_tag(self): return Markup('<input type="hidden" name="csrf_token" value="demo-token">')
    def __iter__(self): return iter(self._c)


perfil = NS(id=1, nombre="Nicolás", apellido="Ferreyra", titulo="Estudiante de Renault", disponible=True, edad=20,
            resumen="Transformo ideas en soluciones digitales simples, útiles y pensadas para las personas.",
            sobre_mi="Me apasiona entender cómo funcionan las cosas y encontrar maneras de hacerlas más simples.\n\n"
                     "Soy estudiante del Centro de Formación Renault, donde combino pensamiento lógico, diseño y tecnología.\n\n"
                     "Hoy busco mi próxima oportunidad para aportar energía, criterio y muchas ganas de crecer.",
            ubicacion="Córdoba, Argentina", intereses="Tecnología · Autos", frase_footer=None,
            github_url="https://github.com/", linkedin_url="https://linkedin.com/", email="nicolas@example.com",
            cv_url="files/cv.pdf",
            foto="https://images.unsplash.com/photo-1565120130276-dfbd9a7a3ad7?auto=format&fit=crop&w=900&q=85")
estudios = [NS(id=1, titulo="Tecnicatura en Programación", institucion="Centro de Formación Renault", periodo="2024 — Actualidad",
               descripcion="Desarrollo de software, bases de datos y metodologías ágiles."),
            NS(id=2, titulo="Bachiller en Informática", institucion="Instituto Técnico Córdoba", periodo="2018 — 2023", descripcion="")]
experiencias = [NS(id=1, puesto="Desarrollador trainee", empresa="Laboratorio Renault", periodo="Mar 2025 — Actualidad",
                   descripcion="Herramientas internas con Python, Flask y MySQL.")]
certificaciones = [NS(id=1, nombre="Python Essentials", entidad="Cisco", anio=2025, url="https://example.com")]
idiomas = [NS(id=1, nombre="Español", nivel="Nativo"), NS(id=2, nombre="Inglés", nivel="B1")]
tecnologias = [NS(id=1, nombre="Python", icono="fa-brands fa-python", nivel="avanzado"),
               NS(id=2, nombre="Flask", icono="fa-solid fa-flask", nivel="intermedio"),
               NS(id=3, nombre="MySQL", icono="fa-solid fa-database", nivel="intermedio"),
               NS(id=4, nombre="Git", icono="fa-brands fa-git-alt", nivel="basico")]
proyectos = [NS(id=1, titulo="Control de producción", categoria="Dashboard industrial", anio=2025,
                descripcion="Panel web para monitorear métricas de producción.", url="https://github.com/",
                imagen="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=82",
                tecnologias=[NS(nombre="Flask"), NS(nombre="MySQL")])]


@app.context_processor
def globales():   # en el backend real: perfil sale de la BD y es_admin de la sesión
    return dict(perfil=perfil, es_admin=request.args.get("admin") == "1")

@app.route("/")
def index():
    form = FormFalso(nombre=Campo("nombre"), email=Campo("email", input_type="email"), asunto=Campo("asunto"),
                     mensaje=Campo("mensaje", html="textarea"))
    return render_template("index.html", estudios=estudios, experiencias=experiencias, certificaciones=certificaciones,
                           idiomas=idiomas, tecnologias=tecnologias, proyectos=proyectos, form_contacto=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = FormFalso(username=Campo("username"), password=Campo("password", input_type="password"))
    return render_template("login.html", form=form)

@app.route("/logout", methods=["POST"])
def logout(): flash("Sesión cerrada", "ok"); return redirect(url_for("index"))

@app.route("/contacto", methods=["POST"])
def contacto(): flash("¡Gracias! Tu mensaje fue enviado.", "ok"); return redirect(url_for("index") + "#contacto")

@app.route("/admin/<seccion>/nuevo", defaults={"id": None}, methods=["GET", "POST"])
@app.route("/admin/<seccion>/<int:id>/editar", methods=["GET", "POST"])
def admin_form(seccion, id):
    form = FormFalso(titulo=Campo("titulo"), descripcion=Campo("descripcion", "TextAreaField", "textarea"))
    return render_template("admin/form.html", form=form, titulo=("Editar " if id else "Agregar ") + seccion)

@app.route("/admin/<seccion>/<int:id>/eliminar", methods=["POST"])
def admin_eliminar(seccion, id): flash("Eliminado", "ok"); return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
