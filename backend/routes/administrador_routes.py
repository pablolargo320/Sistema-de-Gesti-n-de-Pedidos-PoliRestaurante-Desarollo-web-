from flask import Blueprint, request, jsonify
from backend.dao import administrador_dao

administrador_bp = Blueprint("administrador_bp", __name__, url_prefix="/api/administradores")


@administrador_bp.route("/", methods=["GET"])
def listarAdministradores():
    return jsonify(administrador_dao.findAll()), 200


@administrador_bp.route("/<int:id_administrador>", methods=["GET"])
def obtenerAdministrador(id_administrador):
    admin = administrador_dao.buscarAdministradorPorId(id_administrador)
    if admin is None:
        return jsonify({"mensaje": "Administrador no encontrado"}), 404
    return jsonify(admin), 200


@administrador_bp.route("/", methods=["POST"])
def crearAdministrador():
    data = request.get_json()
    nuevoId = administrador_dao.crearAdministrador(
        data.get("nombre"), data.get("correo"), data.get("usuario"),
        data.get("contrasena"), data.get("telefono")
    )
    return jsonify({"id_administrador": nuevoId, "mensaje": "Administrador creado"}), 201


@administrador_bp.route("/<int:id_administrador>", methods=["PUT"])
def actualizarAdministrador(id_administrador):
    data = request.get_json()
    filas = administrador_dao.editarAdministrador(
        id_administrador, data.get("nombre"), data.get("correo"),
        data.get("usuario"), data.get("contrasena"), data.get("telefono")
    )
    if filas == 0:
        return jsonify({"mensaje": "Administrador no encontrado"}), 404
    return jsonify({"mensaje": "Administrador actualizado"}), 200


@administrador_bp.route("/<int:id_administrador>", methods=["DELETE"])
def borrarAdministrador(id_administrador):
    filas = administrador_dao.eliminarAdministrador(id_administrador)
    if filas == 0:
        return jsonify({"mensaje": "Administrador no encontrado"}), 404
    return jsonify({"mensaje": "Administrador eliminado"}), 200
