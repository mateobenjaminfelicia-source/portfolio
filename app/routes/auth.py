from urllib.parse import urlparse
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.forms.auth import LoginForm
from app.models import Administrador

auth_bp = Blueprint("auth", __name__)


def _destino_seguro(destino):
    """Solo acepta rutas internas del sitio, como "/admin/". Rechaza "//otro.com",
    "/\\otro.com" o "https://otro.com", que el navegador interpretaría como otro sitio."""
    return (bool(destino) and destino.startswith("/") and not destino.startswith("//")
            and "\\" not in destino and not urlparse(destino).scheme and not urlparse(destino).netloc)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.panel"))
    form = LoginForm()                       # Flask-WTF: validación + token CSRF
    if form.validate_on_submit():
        admin = Administrador.query.filter_by(usuario=form.username.data).first()
        if admin and admin.check_password(form.password.data):   # compara contra el hash
            login_user(admin)
            destino = request.args.get("next")
            if not _destino_seguro(destino):                     # evita open redirect
                destino = url_for("admin.panel")
            return redirect(destino)
        flash("Usuario o contraseña incorrectos.", "danger")
    return render_template("login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for("public.index"))
