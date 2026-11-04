#saul vargas condori 8393710
from flask import Flask
from config import Config
from .extensions import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)

    from .main.routes import bp as main_bp
    from .auth.routes import bp as auth_bp
    from .usuarios.routes import bp as usuarios_bp
    from .categorias.routes import bp as categorias_bp
    from .anuncios.routes import bp as anuncios_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(categorias_bp, url_prefix="/categorias")
    app.register_blueprint(anuncios_bp, url_prefix="/anuncios")

    with app.app_context():
        from .models import Usuario
        db.create_all()
        if not Usuario.query.first():  # usuario inicial
            u = Usuario(nombre="Administrador", email="admin@upea.bo")
            u.set_password("admin123")
            db.session.add(u); db.session.commit()
    return app
