
from datetime import date

from flask import Blueprint, current_app, jsonify, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from backend.dao.despacho_dao import DespachoDAO


despacho_routes = Blueprint(
    "despacho_routes",
    __name__
)

despacho_dao = DespachoDAO()

ESTADOS_DESPACHO = {
    "preparando",
    "despachado",
    "en_transito",
    "entregado",
    "con_novedad"
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


@despacho_routes.route(
    "/api/despachos",
    methods=["GET"]
)
def listar_despachos():

    try:

        proveedor_raw = request.args.get("proveedor_id")
        proveedor_id = int(proveedor_raw) if proveedor_raw else None

        estado = request.args.get("estado") or None

        if proveedor_id is not None and proveedor_id <= 0:
            return jsonify({
                "error": "El proveedor_id no es válido."
            }), 400

        if estado and estado not in ESTADOS_DESPACHO:
            return jsonify({
                "error": "El filtro de estado no es válido."
            }), 400

        despachos = despacho_dao.listar(
            proveedor_id,
            estado
        )

        return jsonify(despachos), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except SQLAlchemyError:
        current_app.logger.exception(
            "Error consultando despachos"
        )

        return jsonify({
            "error": "No fue posible consultar despachos."
        }), 500


@despacho_routes.route(
    "/api/despachos",
    methods=["POST"]
)
def crear_despacho():

    datos = request.get_json(silent=True) or {}

    solicitud_id = datos.get("solicitud_id_solicitud")
    cantidad = datos.get("cantidad_despachada")

    if type(solicitud_id) is not int or solicitud_id <= 0:
        return jsonify({
            "error": "solicitud_id_solicitud debe ser un entero positivo."
        }), 400

    if type(cantidad) is not int or cantidad <= 0:
        return jsonify({
            "error": "cantidad_despachada debe ser un entero positivo."
        }), 400

    campos = {
        "numero_guia": 60,
        "transportadora": 80,
        "observaciones": 255
    }

    valores = {}

    for campo, maximo in campos.items():

        valor = datos.get(campo)

        if valor is not None and not isinstance(valor, str):
            return jsonify({
                "error": f"{campo} debe ser texto."
            }), 400

        valor = valor.strip() if isinstance(valor, str) else None

        if valor and len(valor) > maximo:
            return jsonify({
                "error": f"{campo} supera {maximo} caracteres."
            }), 400

        valores[campo] = valor or None

    try:

        fecha_estimada = fecha_opcional(
            datos.get("fecha_entrega_estimada"),
            "fecha_entrega_estimada"
        )

        creado = despacho_dao.crear(
            solicitud_id,
            cantidad,
            fecha_estimada,
            valores["numero_guia"],
            valores["transportadora"],
            valores["observaciones"]
        )

        return jsonify(creado), 201

    except ValueError as error:
        return jsonify({"error": str(error)}), 409

    except IntegrityError:
        return jsonify({
            "error": "La solicitud relacionada no existe."
        }), 409

    except SQLAlchemyError:
        current_app.logger.exception(
            "Error creando despacho"
        )

        return jsonify({
            "error": "No fue posible registrar el despacho."
        }), 500


@despacho_routes.route(
    "/api/despachos/<int:id_despacho>/estado",
    methods=["PATCH"]
)
def actualizar_estado_despacho(id_despacho):

    datos = request.get_json(silent=True) or {}

    nuevo_estado = datos.get("estado")

    if nuevo_estado not in ESTADOS_DESPACHO:
        return jsonify({
            "error": "El estado del despacho no es válido."
        }), 400

    try:

        actualizado = despacho_dao.actualizar_estado(
            id_despacho,
            nuevo_estado
        )

        if actualizado is None:
            return jsonify({
                "error": "Despacho no encontrado."
            }), 404

        return jsonify(actualizado), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 409

    except SQLAlchemyError:
        current_app.logger.exception(
            "Error actualizando despacho"
        )

        return jsonify({
            "error": "No fue posible actualizar el despacho."
        }), 500


@despacho_routes.route(
    "/api/despachos/<int:id_despacho>/confirmar-entrega",
    methods=["POST"]
)
def confirmar_entrega(id_despacho):

    try:

        actualizado = despacho_dao.actualizar_estado(
            id_despacho,
            "entregado"
        )

        if actualizado is None:
            return jsonify({
                "error": "Despacho no encontrado."
            }), 404

        return jsonify(actualizado), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 409

    except SQLAlchemyError:
        current_app.logger.exception(
            "Error confirmando entrega"
        )

        return jsonify({
            "error": "No fue posible confirmar la entrega."
        }), 500
