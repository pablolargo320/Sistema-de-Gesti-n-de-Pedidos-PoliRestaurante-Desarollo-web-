from flask import Flask

from backend.routes.producto_routes import producto_routes


def create_app():

    app = Flask(__name__)

    app.register_blueprint(producto_routes)

    return app