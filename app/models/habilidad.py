from app import db
from app.models.base import Seccion
from app.models.catalogos import habilidad_area, conocimiento_area, AreaConocimiento


class Habilidad(Seccion):
    # HERENCIA: hereda orden/visible/visibles()/todas() de Seccion.
    __tablename__ = "habilidades"
    id_habilidad = db.Column(db.Integer, primary_key=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id_perfil"), nullable=False)
    codigo = db.Column(db.String(80), nullable=False, unique=True)
    areas = db.relationship(AreaConocimiento, secondary=habilidad_area)

    # POLIMORFISMO: cada modelo responde distinto a etiqueta() y to_dict().
    def etiqueta(self):
        return self.codigo

    def to_dict(self):
        return {"id": self.id_habilidad, "codigo": self.codigo, "orden": self.orden,
                "visible": self.visible, "areas": [a.codigo for a in self.areas]}


class ConocimientoTecnico(Seccion):
    __tablename__ = "conocimientos_tecnicos"
    id_conocimiento = db.Column(db.Integer, primary_key=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id_perfil"), nullable=False)
    codigo = db.Column(db.String(80), nullable=False, unique=True)
    areas = db.relationship(AreaConocimiento, secondary=conocimiento_area)

    def etiqueta(self):
        return self.codigo

    def to_dict(self):
        return {"id": self.id_conocimiento, "codigo": self.codigo, "orden": self.orden,
                "visible": self.visible, "areas": [a.codigo for a in self.areas]}
