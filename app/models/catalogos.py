from app import db
from app.models.base import BaseModel


def _puente(nombre, col_a, tabla_a, col_b="id_area", tabla_b="areas_conocimiento"):
    """Tabla puente N:M: solo dos FK que juntas forman la PK."""
    return db.Table(
        nombre,
        db.Column(col_a, db.Integer, db.ForeignKey(f"{tabla_a}.{col_a}"), primary_key=True),
        db.Column(col_b, db.Integer, db.ForeignKey(f"{tabla_b}.{col_b}"), primary_key=True),
    )


habilidad_area = _puente("habilidad_area", "id_habilidad", "habilidades")
conocimiento_area = _puente("conocimiento_area", "id_conocimiento", "conocimientos_tecnicos")
objetivo_area = _puente("objetivo_area", "id_objetivo", "objetivos_academicos")
proyecto_area = _puente("proyecto_area", "id_proyecto", "proyectos")
experiencia_area = _puente("experiencia_area", "id_experiencia", "experiencias")
reconocimiento_area = _puente("reconocimiento_area", "id_reconocimiento", "reconocimientos")
capacitacion_area = _puente("capacitacion_area", "id_capacitacion", "capacitaciones")
proyecto_tecnologia = _puente("proyecto_tecnologia", "id_proyecto", "proyectos",
                              col_b="id_tecnologia", tabla_b="tecnologias")


class Idioma(BaseModel):
    __tablename__ = "idiomas"
    id_idioma = db.Column(db.SmallInteger, primary_key=True)
    codigo_iso = db.Column(db.String(10), nullable=False, unique=True)
    nombre = db.Column(db.String(80), nullable=False)

    def etiqueta(self):
        return self.nombre


class AreaConocimiento(BaseModel):
    __tablename__ = "areas_conocimiento"
    id_area = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(60), nullable=False, unique=True)

    def etiqueta(self):
        return self.codigo


class Organizacion(BaseModel):
    __tablename__ = "organizaciones"
    id_organizacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(180), nullable=False)
    sitio_web = db.Column(db.String(2048))
    ubicacion = db.Column(db.String(180))

    def etiqueta(self):
        return self.nombre


class PerfilIdioma(BaseModel):
    """Idiomas que habla el propietario y su nivel (PK compuesta)."""
    __tablename__ = "perfil_idioma"
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id_perfil"), primary_key=True)
    id_idioma = db.Column(db.SmallInteger, db.ForeignKey("idiomas.id_idioma"), primary_key=True)
    nivel = db.Column(db.Enum("nativo", "A1", "A2", "B1", "B2", "C1", "C2"), nullable=False)
    idioma = db.relationship("Idioma", lazy="joined")

    def etiqueta(self):
        return f"{self.idioma.nombre} ({self.nivel})"
