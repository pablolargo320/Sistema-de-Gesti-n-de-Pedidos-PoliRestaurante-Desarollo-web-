
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
from backend.routes.proveedor_routes import proveedor_routes
from backend.routes.domiciliario_routes import domiciliario_routes
from backend.routes.mesa_routes import mesa_bp
from backend.routes.administrador_routes import administrador_bp
from backend.routes.metodopago_routes import metodopago_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(producto_routes)
    app.register_blueprint(categoria_routes)
    app.register_blueprint(proveedor_routes)
    app.register_blueprint(domiciliario_routes)
    app.register_blueprint(mesa_bp)
    app.register_blueprint(administrador_bp)
    app.register_blueprint(metodopago_bp)

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)