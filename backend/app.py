from flask import Flask

from backend.routes.producto_routes import producto_routes
from backend.routes.categoria_routes import categoria_routes
from backend.routes.cliente_routes import cliente_routes


def create_app():

    app = Flask(__name__)

    app.register_blueprint(producto_routes)
    app.register_blueprint(categoria_routes)
    app.register_blueprint(cliente_routes)

    return app