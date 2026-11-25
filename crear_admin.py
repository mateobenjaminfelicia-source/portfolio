"""Uso: python crear_admin.py -> crea/actualiza tu administrador (contraseña hasheada).
Requiere que ya exista una fila en `perfil` (se vincula por id_perfil)."""
import getpass
from sqlalchemy.exc import OperationalError

from app import create_app, db
from app.models import Administrador

app = create_app()
with app.app_context():
    try:
        with db.engine.connect():
            pass
    except OperationalError as error:
        cause = getattr(error, "orig", error)
        print(
            "No se pudo conectar con MySQL de Clever Cloud. "
            "Revisá DB_HOST, DB_NAME, DB_USER y DB_PASSWORD en .env."
        )
        print(f"Detalle de MySQL: {cause}")
        raise SystemExit(1) from None

    id_perfil = int(input("id_perfil (ej. 1): "))
    usuario = input("Usuario: ").strip()
    email = input("Email: ").strip()
    password = getpass.getpass("Contraseña (no se muestra al escribir): ")
    admin = (Administrador.query.filter_by(usuario=usuario).first()
             or Administrador(id_perfil=id_perfil, usuario=usuario, email=email))
    admin.set_password(password)
    admin.guardar()
    print("Listo.")
