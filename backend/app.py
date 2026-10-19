
from flask import Flask

from backend.routes.pedido_routes import pedido_bp
from backend.routes.detalle_pedido_routes import detalle_pedido_routes


def create_app():
    app = Flask(__name__)

    app.register_blueprint(pedido_bp)
    app.register_blueprint(detalle_pedido_routes)
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