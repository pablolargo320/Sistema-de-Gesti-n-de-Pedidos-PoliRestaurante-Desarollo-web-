from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from backend.dao.domiciliario_dao import DomiciliarioDAO


domiciliario_routes = Blueprint(
    "domiciliario_routes",
    __name__
)

domiciliario_dao = DomiciliarioDAO()


def validar_domiciliario(datos):
    if not isinstance(datos, dict):
        return None, "El cuerpo debe ser un objeto JSON"

    nombre = datos.get("nombre")
    apellido = datos.get("apellido")

    if not isinstance(nombre, str) or not nombre.strip():
        return None, "El nombre es obligatorio"

    if not isinstance(apellido, str) or not apellido.strip():
        return None, "El apellido es obligatorio"

    datos_limpios = {
        "nombre": nombre.strip(),
        "apellido": apellido.strip(),
        "telefono": datos.get("telefono"),
        "correo": datos.get("correo"),
        "direccion": datos.get("direccion"),
        "estado": datos.get("estado"),
        "tipo_vehiculo": datos.get("tipo_vehiculo"),
        "placa_vehiculo": datos.get("placa_vehiculo")
    }

    longitudes = {
        "nombre": 45,
        "apellido": 45,
        "telefono": 20,
        "correo": 45,
        "direccion": 45,
        "estado": 45,
        "tipo_vehiculo": 45,
        "placa_vehiculo": 45
    }

    for campo, longitud in longitudes.items():
        valor = datos_limpios[campo]

        if valor is None:
            continue

        if not isinstance(valor, str):
            return None, f"{campo} debe ser texto"

        valor = valor.strip()

        if campo in ("nombre", "apellido") and not valor:
            return None, f"{campo} es obligatorio"

        if len(valor) > longitud:
            return None, f"{campo} supera la longitud permitida"

        datos_limpios[campo] = valor

    return datos_limpios, None


@domiciliario_routes.route("/api/domiciliarios", methods=["GET"])
def obtener_domiciliarios():
    try:
        return jsonify(domiciliario_dao.obtener_todos()), 200
    except SQLAlchemyError:
        return jsonify({"error": "No fue posible consultar domiciliarios"}), 500


@domiciliario_routes.route(
    "/api/domiciliarios/<int:id_domiciliario>",
    methods=["GET"]
)
def obtener_domiciliario(id_domiciliario):
    try:
        domiciliario = domiciliario_dao.obtener_por_id(id_domiciliario)

        if domiciliario is None:
            return jsonify({"error": "Domiciliario no encontrado"}), 404

        return jsonify(domiciliario), 200

    except SQLAlchemyError:
        return jsonify({"error": "Error al consultar el domiciliario"}), 500


@domiciliario_routes.route("/api/domiciliarios", methods=["POST"])
def crear_domiciliario():
    datos, error = validar_domiciliario(
        request.get_json(silent=True)
    )

    if error:
        return jsonify({"error": error}), 400

    try:
        domiciliario = domiciliario_dao.crear(datos)
        return jsonify(domiciliario), 201

    except SQLAlchemyError:
        return jsonify({"error": "No fue posible crear el domiciliario"}), 500


@domiciliario_routes.route(
    "/api/domiciliarios/<int:id_domiciliario>",
    methods=["PUT"]
)
def actualizar_domiciliario(id_domiciliario):
    datos, error = validar_domiciliario(
        request.get_json(silent=True)
    )

    if error:
        return jsonify({"error": error}), 400

    try:
        domiciliario = domiciliario_dao.actualizar(
            id_domiciliario,
            datos
        )

        if domiciliario is None:
            return jsonify({"error": "Domiciliario no encontrado"}), 404

        return jsonify(domiciliario), 200

    except SQLAlchemyError:
        return jsonify({"error": "No fue posible actualizar el domiciliario"}), 500


@domiciliario_routes.route(
    "/api/domiciliarios/<int:id_domiciliario>",
    methods=["DELETE"]
)
def eliminar_domiciliario(id_domiciliario):
    try:
        eliminado = domiciliario_dao.eliminar(id_domiciliario)

        if not eliminado:
            return jsonify({"error": "Domiciliario no encontrado"}), 404

        return jsonify({
            "mensaje": "Domiciliario eliminado correctamente"
        }), 200

    except IntegrityError:
        return jsonify({
            "error": "No se puede eliminar: el domiciliario tiene pedidos asociados"
        }), 409
    except SQLAlchemyError:
        return jsonify({"error": "No fue posible eliminar el domiciliario"}), 500