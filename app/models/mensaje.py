from datetime import datetime
from app import db
from app.models.base import BaseModel


class MensajeContacto(BaseModel):
    # Tabla nueva: se crea con migracion_v3.sql
    __tablename__ = "mensajes_contacto"
    id_mensaje = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    leido = db.Column(db.Boolean, nullable=False, default=False)

    def etiqueta(self):
        return f"{self.nombre} <{self.email}>"
