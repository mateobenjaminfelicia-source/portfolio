from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

db = SQLAlchemy()
csrf = CSRFProtect()          # protección CSRF de Flask-WTF para todos los formularios
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Iniciá sesión para editar el portfolio."


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

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
