from flask import Blueprint, request, jsonify
from dao import mesa_dao

mesa_bp = Blueprint("mesa_bp", __name__, url_prefix="/api/mesas")


@mesa_bp.route("/", methods=["GET"])
def listarMesas():
    return jsonify(mesa_dao.findAll()), 200


@mesa_bp.route("/<int:id_mesa>", methods=["GET"])
def obtenerMesa(id_mesa):
    mesa = mesa_dao.buscarMesaPorId(id_mesa)
    if mesa is None:
        return jsonify({"mensaje": "Mesa no encontrada"}), 404
    return jsonify(mesa), 200


@mesa_bp.route("/", methods=["POST"])
def crearMesa():
    data = request.get_json()
    nuevoId = mesa_dao.crearMesa(data.get("numero"), data.get("estado"))
    return jsonify({"id_mesa": nuevoId, "mensaje": "Mesa creada"}), 201


@mesa_bp.route("/<int:id_mesa>", methods=["PUT"])
def actualizarMesa(id_mesa):
    data = request.get_json()
    filas = mesa_dao.editarMesa(id_mesa, data.get("numero"), data.get("estado"))
    if filas == 0:
        return jsonify({"mensaje": "Mesa no encontrada"}), 404
    return jsonify({"mensaje": "Mesa actualizada"}), 200


@mesa_bp.route("/<int:id_mesa>", methods=["DELETE"])
def borrarMesa(id_mesa):
    filas = mesa_dao.eliminarMesa(id_mesa)
    if filas == 0:
        return jsonify({"mensaje": "Mesa no encontrada"}), 404
    return jsonify({"mensaje": "Mesa eliminada"}), 200
