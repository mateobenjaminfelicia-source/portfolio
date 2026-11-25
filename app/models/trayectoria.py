"""Formación, experiencia, capacitaciones, reconocimientos y objetivos."""
from app import db
from app.models.base import Seccion, Traduccion, Traducible
from app.models.catalogos import (Organizacion, AreaConocimiento, experiencia_area,
                                  capacitacion_area, reconocimiento_area, objetivo_area)


def _titulo(obj, campo):
    return getattr(obj.t, campo) if obj.t else f"#{obj.pk}"


class Formacion(Traducible, Seccion):
    __tablename__ = "formaciones"
    id_formacion = db.Column(db.Integer, primary_key=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id_perfil"), nullable=False)
    id_organizacion = db.Column(db.Integer, db.ForeignKey("organizaciones.id_organizacion"), nullable=False)
    anio_inicio = db.Column(db.Integer)
    anio_fin = db.Column(db.Integer)
    estado = db.Column(db.Enum("planificada", "en_curso", "finalizada"), nullable=False)

    organizacion = db.relationship(Organizacion, lazy="joined")
    traducciones = db.relationship("FormacionTraduccion", cascade="all, delete-orphan", lazy="selectin")

    def etiqueta(self):
        return _titulo(self, "titulo")


class FormacionTraduccion(Traduccion):
    __tablename__ = "formacion_traduccion"
    id_formacion = db.Column(db.Integer, db.ForeignKey("formaciones.id_formacion"), primary_key=True)
    titulo = db.Column(db.String(180), nullable=False)
    descripcion = db.Column(db.Text)


class Experiencia(Traducible, Seccion):
    __tablename__ = "experiencias"
    id_experiencia = db.Column(db.Integer, primary_key=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id_perfil"), nullable=False)
    id_organizacion = db.Column(db.Integer, db.ForeignKey("organizaciones.id_organizacion"))
    tipo = db.Column(db.Enum("academica", "colaboracion", "voluntariado", "laboral"), nullable=False)
    anio_inicio = db.Column(db.Integer)
    anio_fin = db.Column(db.Integer)
    actualmente = db.Column(db.Boolean, nullable=False, default=False)

    organizacion = db.relationship(Organizacion, lazy="joined")
    areas = db.relationship(AreaConocimiento, secondary=experiencia_area)
    traducciones = db.relationship("ExperienciaTraduccion", cascade="all, delete-orphan", lazy="selectin")

    def etiqueta(self):
        return _titulo(self, "puesto")


class ExperienciaTraduccion(Traduccion):
    __tablename__ = "experiencia_traduccion"
    id_experiencia = db.Column(db.Integer, db.ForeignKey("experiencias.id_experiencia"), primary_key=True)
    puesto = db.Column(db.String(180), nullable=False)
    descripcion = db.Column(db.Text)
    logros = db.Column(db.Text)


class Capacitacion(Traducible, Seccion):
    __tablename__ = "capacitaciones"
    id_capacitacion = db.Column(db.Integer, primary_key=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id_perfil"), nullable=False)
    id_organizacion = db.Column(db.Integer, db.ForeignKey("organizaciones.id_organizacion"))
    tipo = db.Column(db.Enum("curso", "certificacion"), nullable=False)
    estado = db.Column(db.Enum("planificada", "en_curso", "finalizada"), nullable=False)
    anio_inicio = db.Column(db.Integer)
    anio_fin = db.Column(db.Integer)
    horas = db.Column(db.Integer)
    certificado_url = db.Column(db.String(2048))

    organizacion = db.relationship(Organizacion, lazy="joined")
    areas = db.relationship(AreaConocimiento, secondary=capacitacion_area)
    traducciones = db.relationship("CapacitacionTraduccion", cascade="all, delete-orphan", lazy="selectin")

    def etiqueta(self):
        return _titulo(self, "nombre")


class CapacitacionTraduccion(Traduccion):
    __tablename__ = "capacitacion_traduccion"
    id_capacitacion = db.Column(db.Integer, db.ForeignKey("capacitaciones.id_capacitacion"), primary_key=True)
    nombre = db.Column(db.String(180), nullable=False)
    descripcion = db.Column(db.Text)


class Reconocimiento(Traducible, Seccion):
    __tablename__ = "reconocimientos"
    id_reconocimiento = db.Column(db.Integer, primary_key=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id_perfil"), nullable=False)
    id_organizacion = db.Column(db.Integer, db.ForeignKey("organizaciones.id_organizacion"))
    anio = db.Column(db.Integer)

    organizacion = db.relationship(Organizacion, lazy="joined")
    areas = db.relationship(AreaConocimiento, secondary=reconocimiento_area)
    traducciones = db.relationship("ReconocimientoTraduccion", cascade="all, delete-orphan", lazy="selectin")

    def etiqueta(self):
        return _titulo(self, "nombre")


class ReconocimientoTraduccion(Traduccion):
    __tablename__ = "reconocimiento_traduccion"
    id_reconocimiento = db.Column(db.Integer, db.ForeignKey("reconocimientos.id_reconocimiento"), primary_key=True)
    nombre = db.Column(db.String(180), nullable=False)
    descripcion = db.Column(db.Text)
    resultado = db.Column(db.String(180))


class ObjetivoAcademico(Traducible, Seccion):
    __tablename__ = "objetivos_academicos"
    id_objetivo = db.Column(db.Integer, primary_key=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id_perfil"), nullable=False)
    estado = db.Column(db.Enum("pendiente", "en_progreso", "cumplido"), nullable=False, default="pendiente")
    prioridad = db.Column(db.SmallInteger, nullable=False, default=3)
    anio_objetivo = db.Column(db.Integer)

    areas = db.relationship(AreaConocimiento, secondary=objetivo_area)
    traducciones = db.relationship("ObjetivoTraduccion", cascade="all, delete-orphan", lazy="selectin")

    def etiqueta(self):
        return _titulo(self, "titulo")


class ObjetivoTraduccion(Traduccion):
    __tablename__ = "objetivo_traduccion"
    id_objetivo = db.Column(db.Integer, db.ForeignKey("objetivos_academicos.id_objetivo"), primary_key=True)
    titulo = db.Column(db.String(180), nullable=False)
    descripcion = db.Column(db.Text)
