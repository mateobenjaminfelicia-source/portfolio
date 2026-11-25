import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-no-usar-en-produccion")
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
    WTF_CSRF_ENABLED = True
