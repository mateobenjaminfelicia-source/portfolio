"""Clases base del proyecto. Acá viven los 4 pilares de POO (marcados con comentarios)."""
import datetime
from sqlalchemy import inspect
from sqlalchemy.orm import declared_attr
from app import db


class BaseModel(db.Model):
    # ABSTRACCIÓN: clase abstracta (no tiene tabla) que define QUÉ puede hacer cualquier
    # modelo (guardar, eliminar, serializar, mostrar una etiqueta) sin saber de qué tabla es.
    __abstract__ = True

    @property
    def pk(self):
        """Valor de la PK, sin importar cómo se llame la columna (id_habilidad, id_perfil...)."""
        return getattr(self, inspect(type(self)).primary_key[0].key)

    def guardar(self):
        db.session.add(self)
        db.session.commit()
        return self

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """Serialización genérica (columnas -> dict). Las subclases pueden sobrescribirla."""
        datos = {}
        for col in inspect(type(self)).columns:
            valor = getattr(self, col.key)
            datos[col.key] = valor.isoformat() if isinstance(valor, (datetime.date, datetime.datetime)) else valor
        return datos

    def etiqueta(self):
        """Texto corto para listar el registro en el panel. Se sobrescribe en cada modelo."""
        return f"#{self.pk}"

    # --- Identificación en las URLs del panel ---------------------------------------
    # Se movió desde Seccion a BaseModel para que también lo usen Perfil y PerfilIdioma
    # (que no tienen orden/visible) en las rutas genéricas de editar/eliminar.
    CLAVE = None   # columna por la que el panel busca el registro (si no es la PK)

    @property
    def ident(self):
        """Identificador que usa el panel en las URLs (CLAVE si existe, si no la PK)."""
        return getattr(self, self.CLAVE) if self.CLAVE else self.pk

    @classmethod
    def obtener_o_404(cls, ident):
        clave = cls.CLAVE or inspect(cls).primary_key[0].key
        return cls.query.filter(getattr(cls, clave) == ident).first_or_404()


class Seccion(BaseModel):
    # HERENCIA: todas las secciones editables (formaciones, proyectos, habilidades...)
    # heredan orden/visible y las consultas comunes de esta clase.
    __abstract__ = True

    orden = db.Column(db.SmallInteger, nullable=False, default=0)
    visible = db.Column(db.Boolean, nullable=False, default=True)

    @classmethod
    def visibles(cls):
        return cls.query.filter_by(visible=True).order_by(cls.orden).all()

    @classmethod
    def todas(cls):
        return cls.query.order_by(cls.orden).all()


class Traduccion(BaseModel):
    # HERENCIA: las 7 tablas *_traduccion comparten la columna/relación del idioma.
    __abstract__ = True

    @declared_attr
    def id_idioma(cls):
        return db.Column(db.SmallInteger, db.ForeignKey("idiomas.id_idioma"), primary_key=True)

    @declared_attr
    def idioma(cls):
        return db.relationship("Idioma", lazy="joined")


class Traducible:
    # Mixin para las entidades que tienen tabla *_traduccion.
    # Expone `.t` = la traducción en el idioma por defecto (español), o la primera disponible.
    IDIOMA_DEFECTO = "es"

    @property
    def t(self):
        for tr in self.traducciones:
            if tr.idioma.codigo_iso == self.IDIOMA_DEFECTO:
                return tr
        return self.traducciones[0] if self.traducciones else None

    def traduccion_en(self, id_idioma):
        """Devuelve la traducción en ese idioma. Si todavía no existe, la crea vacía.
        Así el panel puede guardar el texto en español tanto al crear como al editar."""
        for tr in self.traducciones:
            if tr.id_idioma == id_idioma:
                return tr
        # La clase de la traducción (FormacionTraduccion, ProyectoTraduccion...) se obtiene
        # de la relación `traducciones`, así este método sirve para TODAS las entidades.
        clase = type(self).traducciones.property.mapper.class_
        nueva = clase(id_idioma=id_idioma)
        self.traducciones.append(nueva)
        return nueva
