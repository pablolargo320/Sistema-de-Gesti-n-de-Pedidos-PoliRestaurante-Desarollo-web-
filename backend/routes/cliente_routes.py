
from flask import Blueprint, request, jsonify

from backend.dao.cliente_dao import ClienteDAO
from backend.entities.cliente import Cliente


cliente_routes = Blueprint(
    "cliente_routes",
    __name__
)

cliente_dao = ClienteDAO()


def cliente_a_json(cliente):
    return {
        "id_cliente": cliente.id_cliente,
        "nombre": cliente.nombre,
        "telefono": cliente.telefono,
        "correo": cliente.correo,
        "direccion": cliente.direccion
    }


@cliente_routes.route("/api/clientes", methods=["GET"])
def obtener_clientes():
    clientes = cliente_dao.obtener_todos()

    return jsonify([
        cliente_a_json(cliente)
        for cliente in clientes
    ]), 200


@cliente_routes.route(
    "/api/clientes/<int:id_cliente>",
    methods=["GET"]
)
def obtener_cliente(id_cliente):
    cliente = cliente_dao.obtener_por_id(id_cliente)

    if cliente is None:
        return jsonify({
            "mensaje": "Cliente no encontrado"
        }), 404

    return jsonify(cliente_a_json(cliente)), 200


@cliente_routes.route("/api/clientes", methods=["POST"])
def crear_cliente():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "mensaje": "Debes enviar un objeto JSON válido"
        }), 400

    if not datos.get("nombre"):
        return jsonify({
            "mensaje": "El nombre es obligatorio"
        }), 400

    cliente = Cliente(
        nombre=datos.get("nombre"),
        telefono=datos.get("telefono"),
        correo=datos.get("correo"),
        direccion=datos.get("direccion")
    )

    cliente_creado = cliente_dao.crear(cliente)

    return jsonify(cliente_a_json(cliente_creado)), 201


@cliente_routes.route(
    "/api/clientes/<int:id_cliente>",
    methods=["PUT"]
)
def actualizar_cliente(id_cliente):
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "mensaje": "Debes enviar un objeto JSON válido"
        }), 400

    if not datos.get("nombre"):
        return jsonify({
            "mensaje": "El nombre es obligatorio"
        }), 400

    cliente = Cliente(
        nombre=datos.get("nombre"),
        telefono=datos.get("telefono"),
        correo=datos.get("correo"),
        direccion=datos.get("direccion")
    )

    filas_afectadas = cliente_dao.actualizar(
        id_cliente,
        cliente
    )

    if filas_afectadas == 0:
        return jsonify({
            "mensaje": "Cliente no encontrado"
        }), 404

    return jsonify({
        "mensaje": "Cliente actualizado correctamente"
    }), 200


@cliente_routes.route(
    "/api/clientes/<int:id_cliente>",
    methods=["DELETE"]
)
def eliminar_cliente(id_cliente):
    filas_afectadas = cliente_dao.eliminar(id_cliente)

    if filas_afectadas == 0:
        return jsonify({
            "mensaje": "Cliente no encontrado"
        }), 404

    return jsonify({
        "mensaje": "Cliente eliminado correctamente"
    }), 200