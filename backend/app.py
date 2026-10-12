
from flask import Flask

from backend.routes.producto_routes import producto_routes
from backend.routes.categoria_routes import categoria_routes
from backend.routes.proveedor_routes import proveedor_routes
from backend.routes.domiciliario_routes import domiciliario_routes


def create_app():
    app = Flask(__name__)

    app.register_blueprint(producto_routes)
    app.register_blueprint(categoria_routes)
    app.register_blueprint(proveedor_routes)
    app.register_blueprint(domiciliario_routes)

    return app
