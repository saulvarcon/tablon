#saul vargas condori 8393710
import os
BASE = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "cambia-esta-clave")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE, "bd_anuncios.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
