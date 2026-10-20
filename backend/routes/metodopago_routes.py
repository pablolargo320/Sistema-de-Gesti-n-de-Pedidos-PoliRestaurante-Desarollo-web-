from flask import Blueprint, request, jsonify
from backend.dao import metodopago_dao

metodopago_bp = Blueprint("metodopago_bp", __name__, url_prefix="/api/metodos-pago")


@metodopago_bp.route("/", methods=["GET"])
def listarMetodosPago():
    return jsonify(metodopago_dao.findAll()), 200


@metodopago_bp.route("/<int:id_metodo_pago>", methods=["GET"])
def obtenerMetodoPago(id_metodo_pago):
    metodo = metodopago_dao.buscarMetodoPagoPorId(id_metodo_pago)
    if metodo is None:
        return jsonify({"mensaje": "Metodo de pago no encontrado"}), 404
    return jsonify(metodo), 200


@metodopago_bp.route("/", methods=["POST"])
def crearMetodoPago():
    data = request.get_json()
    nuevoId = metodopago_dao.crearMetodoPago(
        data.get("efectivo"), data.get("aplicacion"), data.get("tarjeta"),
        data.get("descripcion"), data.get("estado")
    )
    return jsonify({"id_metodo_pago": nuevoId, "mensaje": "Metodo de pago creado"}), 201


@metodopago_bp.route("/<int:id_metodo_pago>", methods=["PUT"])
def actualizarMetodoPago(id_metodo_pago):
    data = request.get_json()
    filas = metodopago_dao.editarMetodoPago(
        id_metodo_pago, data.get("efectivo"), data.get("aplicacion"),
        data.get("tarjeta"), data.get("descripcion"), data.get("estado")
    )
    if filas == 0:
        return jsonify({"mensaje": "Metodo de pago no encontrado"}), 404
    return jsonify({"mensaje": "Metodo de pago actualizado"}), 200


@metodopago_bp.route("/<int:id_metodo_pago>", methods=["DELETE"])
def borrarMetodoPago(id_metodo_pago):
    filas = metodopago_dao.eliminarMetodoPago(id_metodo_pago)
    if filas == 0:
        return jsonify({"mensaje": "Metodo de pago no encontrado"}), 404
    return jsonify({"mensaje": "Metodo de pago eliminado"}), 200
