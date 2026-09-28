from flask import Blueprint

producto_routes = Blueprint("producto_routes", __name__)


@producto_routes.route("/api/productos", methods=["POST"])
def crear_producto():
    pass


@producto_routes.route("/api/productos", methods=["GET"])
def obtener_productos():
    pass


@producto_routes.route("/api/productos/<int:id_producto>", methods=["GET"])
def obtener_producto(id_producto):
    pass


@producto_routes.route("/api/productos/<int:id_producto>", methods=["PUT"])
def actualizar_producto(id_producto):
    pass


@producto_routes.route("/api/productos/<int:id_producto>", methods=["DELETE"])
def eliminar_producto(id_producto):
    pass