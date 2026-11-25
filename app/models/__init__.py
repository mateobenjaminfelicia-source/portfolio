from app.models.catalogos import Idioma, AreaConocimiento, Organizacion, PerfilIdioma
from app.models.perfil import Perfil, PerfilTraduccion, Contacto
from app.models.trayectoria import (Formacion, Experiencia, Capacitacion,
                                    Reconocimiento, ObjetivoAcademico)
from app.models.proyectos import Tecnologia, PerfilTecnologia, Proyecto
from app.models.habilidad import Habilidad, ConocimientoTecnico
from app.models.administrador import Administrador
from app.models.mensaje import MensajeContacto

# Secciones editables desde el panel. POLIMORFISMO: todas responden a
# todas() / visibles() / obtener_o_404() / etiqueta() sin que el panel sepa cuál es cuál.
SECCIONES = {
    "contactos": Contacto,
    "formaciones": Formacion,
    "experiencias": Experiencia,
    "proyectos": Proyecto,
    "capacitaciones": Capacitacion,
    "reconocimientos": Reconocimiento,
    "objetivos": ObjetivoAcademico,
    "tecnologias": PerfilTecnologia,
    "habilidades": Habilidad,
    "conocimientos": ConocimientoTecnico,
}
