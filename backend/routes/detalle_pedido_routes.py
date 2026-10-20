
from flask import Blueprint, request, jsonify

from backend.dao.detalle_pedido_dao import DetallePedidoDAO
from backend.entities.detalle_pedido import DetallePedido


detalle_pedido_routes = Blueprint(
    "detalle_pedido_routes",
    __name__
)

detalle_dao = DetallePedidoDAO()


def serializar_detalle(detalle):
    return {
        "id_detalle": detalle.id_detalle,
        "cantidad": detalle.cantidad,
        "notas": detalle.notas,
        "subtotal": (
            float(detalle.subtotal)
            if detalle.subtotal is not None else None
        ),
        "id_pedido": detalle.id_pedido,
        "id_producto": detalle.id_producto
    }


@detalle_pedido_routes.route(
    "/api/detalles-pedido",
    methods=["GET"]
)
def obtener_detalles():
    detalles = detalle_dao.obtener_todos()
    return jsonify([
        serializar_detalle(d) for d in detalles
    ]), 200


@detalle_pedido_routes.route(
    "/api/detalles-pedido/<int:id_detalle>",
    methods=["GET"]
)
def obtener_detalle(id_detalle):
    detalle = detalle_dao.obtener_por_id(id_detalle)

    if detalle is None:
        return jsonify({
            "mensaje": "Detalle de pedido no encontrado"
        }), 404

    return jsonify(serializar_detalle(detalle)), 200


@detalle_pedido_routes.route(
    "/api/pedidos/<int:id_pedido>/detalles",
    methods=["GET"]
)
def obtener_detalles_por_pedido(id_pedido):
    detalles = detalle_dao.obtener_por_pedido(id_pedido)
    return jsonify([
        serializar_detalle(d) for d in detalles
    ]), 200


@detalle_pedido_routes.route(
    "/api/detalles-pedido",
    methods=["POST"]
)
def crear_detalle():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "mensaje": "Debes enviar un objeto JSON válido"
        }), 400

    detalle = DetallePedido(
        cantidad=datos.get("cantidad"),
        notas=datos.get("notas"),
        subtotal=datos.get("subtotal"),
        id_pedido=datos.get("id_pedido"),
        id_producto=datos.get("id_producto")
    )

    detalle_creado = detalle_dao.crear(detalle)

    return jsonify(serializar_detalle(detalle_creado)), 201


@detalle_pedido_routes.route(
    "/api/detalles-pedido/<int:id_detalle>",
    methods=["PUT"]
)
def actualizar_detalle(id_detalle):
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "mensaje": "Debes enviar un objeto JSON válido"
        }), 400

    detalle = DetallePedido(
        cantidad=datos.get("cantidad"),
        notas=datos.get("notas"),
        subtotal=datos.get("subtotal"),
        id_pedido=datos.get("id_pedido"),
        id_producto=datos.get("id_producto")
    )

    filas = detalle_dao.actualizar(id_detalle, detalle)

    if filas == 0:
        return jsonify({
            "mensaje": "Detalle de pedido no encontrado"
        }), 404

    return jsonify({
        "mensaje": "Detalle de pedido actualizado correctamente"
    }), 200


@detalle_pedido_routes.route(
    "/api/detalles-pedido/<int:id_detalle>",
    methods=["DELETE"]
)
def eliminar_detalle(id_detalle):
    filas = detalle_dao.eliminar(id_detalle)

    if filas == 0:
        return jsonify({
            "mensaje": "Detalle de pedido no encontrado"
        }), 404

    return jsonify({
        "mensaje": "Detalle de pedido eliminado correctamente"
    }), 200
