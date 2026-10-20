from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from backend.dao.proveedor_dao import ProveedorDAO
from backend.dao.producto_dao import ProductoDAO


proveedor_routes = Blueprint(
    "proveedor_routes",
    __name__
)

proveedor_dao = ProveedorDAO()
producto_dao = ProductoDAO()


def validar_proveedor(datos):
    if not isinstance(datos, dict):
        return None, "El cuerpo debe ser un objeto JSON"

    nombre = datos.get("nombre")

    if not isinstance(nombre, str) or not nombre.strip():
        return None, "El nombre del proveedor es obligatorio"

    nombre = nombre.strip()

    if len(nombre) > 45:
        return None, "El nombre no puede superar 45 caracteres"

    campos = {
        "telefono": 20,
        "correo": 45,
        "direccion": 45
    }

    datos_limpios = {
        "nombre": nombre,
        "telefono": datos.get("telefono"),
        "correo": datos.get("correo"),
        "direccion": datos.get("direccion"),
        "producto_id_producto": datos.get("producto_id_producto")
    }

    for campo, longitud in campos.items():
        valor = datos_limpios[campo]

        if valor is not None:
            if not isinstance(valor, str):
                return None, f"{campo} debe ser texto"

            valor = valor.strip()

            if len(valor) > longitud:
                return None, f"{campo} supera la longitud permitida"

            datos_limpios[campo] = valor

    id_producto = datos_limpios["producto_id_producto"]

    if id_producto is not None:
        if type(id_producto) is not int:
            return None, "producto_id_producto debe ser un entero"

        if producto_dao.obtener_por_id(id_producto) is None:
            return None, "El producto asociado no existe"

    return datos_limpios, None


@proveedor_routes.route("/api/proveedores", methods=["GET"])
def obtener_proveedores():
    try:
        return jsonify(proveedor_dao.obtener_todos()), 200
    except SQLAlchemyError:
        return jsonify({"error": "No fue posible consultar proveedores"}), 500


@proveedor_routes.route(
    "/api/proveedores/<int:id_proveedor>",
    methods=["GET"]
)
def obtener_proveedor(id_proveedor):
    try:
        proveedor = proveedor_dao.obtener_por_id(id_proveedor)

        if proveedor is None:
            return jsonify({"error": "Proveedor no encontrado"}), 404

        return jsonify(proveedor), 200

    except SQLAlchemyError:
        return jsonify({"error": "Error al consultar el proveedor"}), 500


@proveedor_routes.route("/api/proveedores", methods=["POST"])
def crear_proveedor():
    datos, error = validar_proveedor(request.get_json(silent=True))

    if error:
        return jsonify({"error": error}), 400

    try:
        proveedor = proveedor_dao.crear(datos)
        return jsonify(proveedor), 201

    except IntegrityError:
        return jsonify({"error": "Los datos relacionados no son válidos"}), 409
    except SQLAlchemyError:
        return jsonify({"error": "No fue posible crear el proveedor"}), 500


@proveedor_routes.route(
    "/api/proveedores/<int:id_proveedor>",
    methods=["PUT"]
)
def actualizar_proveedor(id_proveedor):
    datos, error = validar_proveedor(request.get_json(silent=True))

    if error:
        return jsonify({"error": error}), 400

    try:
        proveedor = proveedor_dao.actualizar(id_proveedor, datos)

        if proveedor is None:
            return jsonify({"error": "Proveedor no encontrado"}), 404

        return jsonify(proveedor), 200

    except IntegrityError:
        return jsonify({"error": "Los datos relacionados no son válidos"}), 409
    except SQLAlchemyError:
        return jsonify({"error": "No fue posible actualizar el proveedor"}), 500


@proveedor_routes.route(
    "/api/proveedores/<int:id_proveedor>",
    methods=["DELETE"]
)
def eliminar_proveedor(id_proveedor):
    try:
        eliminado = proveedor_dao.eliminar(id_proveedor)

        if not eliminado:
            return jsonify({"error": "Proveedor no encontrado"}), 404

        return jsonify({
            "mensaje": "Proveedor eliminado correctamente"
        }), 200

    except SQLAlchemyError:
        return jsonify({"error": "No fue posible eliminar el proveedor"}), 500