import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()

# En Render se carga APP_ENV=production. En tu compu no existe, así que queda en modo desarrollo.
EN_PRODUCCION = os.environ.get("APP_ENV") == "production"


class Config:
    # SECRET_KEY firma la sesión y los tokens CSRF. En producción NO puede faltar: si alguien
    # conoce la clave (y una clave por defecto está en el repo público) puede falsificar sesiones.
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        if EN_PRODUCCION:
            raise RuntimeError("Falta la variable de entorno SECRET_KEY")
        SECRET_KEY = "dev-solo-local"
    # Conexión a MySQL (Clever Cloud) con PyMySQL
    SQLALCHEMY_DATABASE_URI = URL.create(
        "mysql+pymysql",
        username=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 3306)),
        database=os.environ.get("DB_NAME"),
        query={"charset": "utf8mb4"},
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Clever Cloud limita conexiones simultáneas: pool chico y reciclado
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_size": 3, "max_overflow": 0,
                                 "pool_recycle": 280, "pool_pre_ping": True}
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # Secure: la cookie de sesión solo viaja por HTTPS. Render usa HTTPS; tu compu (http://127.0.0.1)
    # no, por eso se activa solo en producción (si no, en local no podrías iniciar sesión).
    SESSION_COOKIE_SECURE = EN_PRODUCCION
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = EN_PRODUCCION
    WTF_CSRF_ENABLED = True
