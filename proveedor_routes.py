from flask import Blueprint


proveedor_routes = Blueprint(
    "proveedor_routes",
    __name__
)


@proveedor_routes.route(
    "/api/proveedores",
    methods=["POST"]
)
def crear_proveedor():

    pass


@proveedor_routes.route(
    "/api/proveedores",
    methods=["GET"]
)
def obtener_proveedores():

    pass


@proveedor_routes.route(
    "/api/proveedores/<int:id_proveedor>",
    methods=["GET"]
)
def obtener_proveedor(id_proveedor):

    pass


@proveedor_routes.route(
    "/api/proveedores/<int:id_proveedor>",
    methods=["PUT"]
)
def actualizar_proveedor(id_proveedor):

    pass


@proveedor_routes.route(
    "/api/proveedores/<int:id_proveedor>",
    methods=["DELETE"]
)
def eliminar_proveedor(id_proveedor):

    pass


@proveedor_routes.route(
    "/api/proveedores/nombre/<string:nombre>",
    methods=["GET"]
)
def buscar_por_nombre(nombre):

    pass


@proveedor_routes.route(
    "/api/proveedores/producto/<int:id_producto>",
    methods=["GET"]
)
def buscar_por_producto(id_producto):

    pass