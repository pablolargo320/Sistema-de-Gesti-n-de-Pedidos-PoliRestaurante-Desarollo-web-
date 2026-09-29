from flask import Blueprint


mesa_routes = Blueprint(
    "mesa_routes",
    __name__
)


@mesa_routes.route(
    "/api/mesas",
    methods=["POST"]
)
def crear_mesa():

    pass


@mesa_routes.route(
    "/api/mesas",
    methods=["GET"]
)
def obtener_mesas():

    pass


@mesa_routes.route(
    "/api/mesas/<int:id_mesa>",
    methods=["GET"]
)
def obtener_mesa(id_mesa):

    pass


@mesa_routes.route(
    "/api/mesas/<int:id_mesa>",
    methods=["PUT"]
)
def actualizar_mesa(id_mesa):

    pass


@mesa_routes.route(
    "/api/mesas/<int:id_mesa>",
    methods=["DELETE"]
)
def eliminar_mesa(id_mesa):

    pass
