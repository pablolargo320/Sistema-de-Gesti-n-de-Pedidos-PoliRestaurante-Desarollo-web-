
from flask import Flask

from backend.routes.pedido_routes import pedido_bp
from backend.routes.detalle_pedido_routes import detalle_pedido_routes


def create_app():
    app = Flask(__name__)

    app.register_blueprint(pedido_bp)
    app.register_blueprint(detalle_pedido_routes)

    return app