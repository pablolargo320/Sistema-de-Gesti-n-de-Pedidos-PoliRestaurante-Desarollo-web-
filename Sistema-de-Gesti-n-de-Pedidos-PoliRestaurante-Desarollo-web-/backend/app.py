from pathlib import Path

from flask import Flask, render_template

from backend.routes.producto_routes import producto_routes
from backend.routes.categoria_routes import categoria_routes
from backend.routes.proveedor_routes import proveedor_routes
from backend.routes.domiciliario_routes import domiciliario_routes

from backend.routes.solicitud_routes import solicitud_routes
from backend.routes.despacho_routes import despacho_routes
from backend.routes.proveedor_panel_routes import proveedor_panel_routes


BASE_DIR = Path(__file__).resolve().parent.parent


def create_app():

    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static")
    )

    # Rutas que ya tenía el proyecto
    app.register_blueprint(producto_routes)
    app.register_blueprint(categoria_routes)
    app.register_blueprint(proveedor_routes)
    app.register_blueprint(domiciliario_routes)

    # Nuevas rutas del proveedor
    app.register_blueprint(solicitud_routes)
    app.register_blueprint(despacho_routes)
    app.register_blueprint(proveedor_panel_routes)

    @app.route("/")
    @app.route("/proveedor")
    def modulo_proveedor():
        return render_template("proveedor/index.html")

    return app