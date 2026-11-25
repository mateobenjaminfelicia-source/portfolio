from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()
csrf = CSRFProtect()          # protección CSRF de Flask-WTF para todos los formularios
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Iniciá sesión para editar el portfolio."
# Limita cuántas veces por minuto se puede intentar algo (se usa en el login contra la
# fuerza bruta). Cuenta los intentos por dirección IP y los guarda en memoria.
limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Render pone un proxy delante de la app: sin esto, Flask vería la IP del proxy en vez
    # de la del visitante y el límite de intentos castigaría a todos juntos.
    if app.config.get("EN_PRODUCCION"):
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)

    from app.routes.public import public_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.context_processor
    def datos_globales():
        # base.html (navbar, footer, <title>) usa `perfil` y `es_admin` en TODAS las páginas.
        # Un context processor los inyecta en cada template desde un solo lugar, en vez de
        # pasarlos a mano en cada render_template (ese olvido causaba "'perfil' is undefined").
        from flask_login import current_user
        from app.models import Perfil
        return {"perfil": Perfil.query.first(), "es_admin": current_user.is_authenticated}

    return app
