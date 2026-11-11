
from datetime import date

from flask import Blueprint, current_app, jsonify, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from backend.dao.solicitud_abastecimiento_dao import SolicitudAbastecimientoDAO


solicitud_routes = Blueprint(
    "solicitud_routes",
    __name__
)

solicitud_dao = SolicitudAbastecimientoDAO()

ESTADOS_SOLICITUD = {
    "pendiente",
    "aceptada",
    "rechazada",
    "en_despacho",
    "completada",
    "cancelada"
}


def fecha_opcional(valor, campo):

    if valor in (None, ""):
        return None

    try:
        return date.fromisoformat(valor)

    except (TypeError, ValueError):
        raise ValueError(
            f"{campo} debe tener formato AAAA-MM-DD."
        )


@solicitud_routes.route(
    "/api/solicitudes-abastecimiento",
    methods=["GET"]
)
def listar_solicitudes():

    try:

        proveedor_raw = request.args.get("proveedor_id")
        proveedor_id = int(proveedor_raw) if proveedor_raw else None

        estado = request.args.get("estado") or None
        busqueda = request.args.get("q") or None

        if proveedor_id is not None and proveedor_id <= 0:
            return jsonify({
                "error": "El proveedor_id no es válido."
            }), 400

        if estado and estado not in ESTADOS_SOLICITUD:
            return jsonify({
                "error": "El filtro de estado no es válido."
            }), 400

        solicitudes = solicitud_dao.listar(
            proveedor_id,
            estado,
            busqueda
        )

        return jsonify(solicitudes), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except SQLAlchemyError:
        current_app.logger.exception(
            "Error consultando solicitudes"
        )

        return jsonify({
            "error": "No fue posible consultar las solicitudes."
        }), 500


@solicitud_routes.route(
    "/api/solicitudes-abastecimiento/<int:id_solicitud>",
    methods=["GET"]
)
def obtener_solicitud(id_solicitud):

    try:

        solicitud = solicitud_dao.obtener_por_id(
            id_solicitud
        )

        if solicitud is None:
            return jsonify({
                "error": "Solicitud no encontrada."
            }), 404

        return jsonify(solicitud), 200

    except SQLAlchemyError:
        current_app.logger.exception(
            "Error consultando solicitud"
        )

        return jsonify({
            "error": "No fue posible consultar la solicitud."
        }), 500


@solicitud_routes.route(
    "/api/solicitudes-abastecimiento",
    methods=["POST"]
)
def crear_solicitud():

    datos = request.get_json(silent=True) or {}

    proveedor_id = datos.get("proveedor_id_proveedor")
    cantidad = datos.get("cantidad_solicitada")

    if type(proveedor_id) is not int or proveedor_id <= 0:
        return jsonify({
            "error": "proveedor_id_proveedor debe ser un entero positivo."
        }), 400

    if type(cantidad) is not int or cantidad <= 0:
        return jsonify({
            "error": "cantidad_solicitada debe ser un entero positivo."
        }), 400

    observaciones = datos.get("observaciones")

    if observaciones is not None:
        if not isinstance(observaciones, str) or len(observaciones) > 255:
            return jsonify({
                "error": "observaciones debe ser texto de máximo 255 caracteres."
            }), 400

    try:

        fecha_requerida = fecha_opcional(
            datos.get("fecha_requerida"),
            "fecha_requerida"
        )

        creada = solicitud_dao.crear(
            proveedor_id,
            cantidad,
            fecha_requerida,
            observaciones
        )

        return jsonify(creada), 201

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except IntegrityError:
        return jsonify({
            "error": "Los datos de proveedor o producto no son válidos."
        }), 409

    except SQLAlchemyError:
        current_app.logger.exception(
            "Error creando solicitud"
        )

        return jsonify({
            "error": "No fue posible registrar la solicitud."
        }), 500


@solicitud_routes.route(
    "/api/solicitudes-abastecimiento/<int:id_solicitud>/estado",
    methods=["PATCH"]
)
def responder_solicitud(id_solicitud):

    datos = request.get_json(silent=True) or {}

    nuevo_estado = datos.get("estado")
    motivo = datos.get("motivo_rechazo")

    if nuevo_estado not in ("aceptada", "rechazada"):
        return jsonify({
            "error": "Solo puedes aceptar o rechazar una solicitud pendiente."
        }), 400

    if motivo is not None:
        if not isinstance(motivo, str) or len(motivo) > 255:
            return jsonify({
                "error": "El motivo no puede superar 255 caracteres."
            }), 400

    try:

        actualizada = solicitud_dao.actualizar_estado(
            id_solicitud,
            nuevo_estado,
            motivo
        )

        if actualizada is None:
            return jsonify({
                "error": "Solicitud no encontrada."
            }), 404

        return jsonify(actualizada), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 409

    except SQLAlchemyError:
        current_app.logger.exception(
            "Error actualizando solicitud"
        )

        return jsonify({
            "error": "No fue posible actualizar la solicitud."
        }), 500
