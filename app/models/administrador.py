from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from app.models.base import BaseModel


class Administrador(UserMixin, BaseModel):
    __tablename__ = "administradores"

    id_administrador = db.Column(db.Integer, primary_key=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id_perfil"), nullable=False, unique=True)
    usuario = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    # ENCAPSULAMIENTO: el hash vive en un atributo "privado" (_password_hash, mapeado a la
    # columna password_hash) y solo se toca mediante set_password / check_password.
    _password_hash = db.Column("password_hash", db.String(255), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password_plano):
        self._password_hash = generate_password_hash(password_plano)

    def check_password(self, password_plano):
        return self.activo and check_password_hash(self._password_hash, password_plano)

    # Flask-Login necesita saber cuál es el id (nuestra PK no se llama "id")
    def get_id(self):
        return str(self.id_administrador)

    @property
    def is_active(self):
        return self.activo

    # POLIMORFISMO: mismo to_dict() que el resto de modelos, pero NUNCA expone el hash.
    def to_dict(self):
        return {"id": self.id_administrador, "usuario": self.usuario, "email": self.email}


@login_manager.user_loader
def cargar_usuario(user_id):
    return db.session.get(Administrador, int(user_id))
