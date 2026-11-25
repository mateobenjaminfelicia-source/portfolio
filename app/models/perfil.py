from datetime import datetime
from app import db
from app.models.base import BaseModel, Seccion, Traduccion, Traducible


class Perfil(Traducible, BaseModel):
    __tablename__ = "perfil"
    id_perfil = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    foto_url = db.Column(db.String(2048))
    cv_url = db.Column(db.String(2048))
    ubicacion = db.Column(db.String(150))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    traducciones = db.relationship("PerfilTraduccion", cascade="all, delete-orphan", lazy="selectin")
    contactos = db.relationship("Contacto", lazy="selectin")

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def etiqueta(self):
        return self.nombre_completo

    @property
    def titulo(self):
        return self.t.titular if self.t else None

    @property
    def sobre_mi(self):
        return self.t.sobre_mi if self.t else None

    @property
    def resumen(self):
        texto = self.sobre_mi or ""
        return texto.split(". ", 1)[0] + ("." if ". " in texto else "")

    @property
    def foto(self):
        return self.foto_url

    def _contacto(self, tipo):
        return next((c for c in self.contactos if c.tipo == tipo and c.visible), None)

    @property
    def email(self):
        contacto = self._contacto("email")
        return contacto.valor if contacto else None

    @property
    def github_url(self):
        contacto = self._contacto("github")
        return contacto.url if contacto else None

    @property
    def linkedin_url(self):
        contacto = self._contacto("linkedin")
        return contacto.url if contacto else None


class PerfilTraduccion(Traduccion):
    __tablename__ = "perfil_traduccion"
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id_perfil"), primary_key=True)
    titular = db.Column(db.String(180))
    sobre_mi = db.Column(db.Text)


class Contacto(Seccion):
    __tablename__ = "contactos"
    id_contacto = db.Column(db.Integer, primary_key=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id_perfil"), nullable=False)
    tipo = db.Column(db.Enum("email", "telefono", "github", "linkedin", "sitio_web", "otro"), nullable=False)
    valor = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(2048))

    def etiqueta(self):
        return f"{self.tipo}: {self.valor}"
