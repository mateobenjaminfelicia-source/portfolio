"""Proyectos y tecnologías (catálogo + nivel por perfil)."""
from app import db
from app.models.base import BaseModel, Seccion, Traduccion, Traducible
from app.models.catalogos import AreaConocimiento, proyecto_area, proyecto_tecnologia


class Tecnologia(BaseModel):
    """Catálogo de tecnologías (nombre propio, no se traduce)."""
    __tablename__ = "tecnologias"
    id_tecnologia = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    tipo = db.Column(db.Enum("lenguaje", "framework", "libreria", "herramienta",
                             "marcado", "base_datos", "otro"), nullable=False)
    icono = db.Column(db.String(80))   # clase FontAwesome, ej: "fa-brands fa-python" (migracion_v3.sql)

    def etiqueta(self):
        return self.nombre


class PerfilTecnologia(Seccion):
    """Nivel de dominio del propietario en cada tecnología (PK compuesta)."""
    __tablename__ = "perfil_tecnologia"
    CLAVE = "id_tecnologia"   # el panel identifica el registro por la tecnología
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id_perfil"), primary_key=True)
    id_tecnologia = db.Column(db.Integer, db.ForeignKey("tecnologias.id_tecnologia"), primary_key=True)
    nivel = db.Column(db.Enum("principiante", "basico", "intermedio", "avanzado"), nullable=False)

    tecnologia = db.relationship(Tecnologia, lazy="joined")

    def etiqueta(self):
        return f"{self.tecnologia.nombre} ({self.nivel})"


class Proyecto(Traducible, Seccion):
    __tablename__ = "proyectos"
    id_proyecto = db.Column(db.Integer, primary_key=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id_perfil"), nullable=False)
    anio_inicio = db.Column(db.Integer)
    anio_fin = db.Column(db.Integer)
    estado = db.Column(db.Enum("planificado", "en_desarrollo", "finalizado", "pausado"), nullable=False)
    repositorio_url = db.Column(db.String(2048))
    demo_url = db.Column(db.String(2048))
    imagen_url = db.Column(db.String(2048))

    tecnologias = db.relationship(Tecnologia, secondary=proyecto_tecnologia)
    areas = db.relationship(AreaConocimiento, secondary=proyecto_area)
    traducciones = db.relationship("ProyectoTraduccion", cascade="all, delete-orphan", lazy="selectin")

    def etiqueta(self):
        return self.t.nombre if self.t else f"#{self.pk}"


class ProyectoTraduccion(Traduccion):
    __tablename__ = "proyecto_traduccion"
    id_proyecto = db.Column(db.Integer, db.ForeignKey("proyectos.id_proyecto"), primary_key=True)
    nombre = db.Column(db.String(180), nullable=False)
    descripcion = db.Column(db.Text)
    objetivo = db.Column(db.Text)
    rol = db.Column(db.String(120))
