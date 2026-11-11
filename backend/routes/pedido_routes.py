from datetime import datetime
from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from backend.dao.pedido_dao import PedidoDAO

pedido_bp = Blueprint("pedido", __name__)
pedido_dao = PedidoDAO()


CAMPOS_PERMITIDOS = {
    "fecha_creacion",
    "estado",
    "total",
    "tipo_pedido",
    "id_mesa",
    "id_cliente",
    "Administrador_id_administrador",
    "metodo_pago_id_metodo_pago",
    "domiciliario_id_domiciliario",
}

CAMPOS_ID = {
    "id_mesa",
    "id_cliente",
    "Administrador_id_administrador",
    "metodo_pago_id_metodo_pago",
    "domiciliario_id_domiciliario",
}


def validar_datos(datos, es_actualizacion=False):
    if not isinstance(datos, dict):
        return None, "El cuerpo debe ser un objeto JSON"

    if es_actualizacion and not datos:
        return None, "Debe enviar al menos un campo para actualizar"

    desconocidos = set(datos) - CAMPOS_PERMITIDOS

    if desconocidos:
        return None, f"Campos no permitidos: {', '.join(sorted(desconocidos))}"

    resultado = dict(datos)

    for campo in ("estado", "tipo_pedido"):
        if campo in resultado:
            valor = resultado[campo]

            if not isinstance(valor, str) or not valor.strip():
                return None, f"El campo {campo} debe ser un texto no vacío"

            resultado[campo] = valor.strip()

            if len(resultado[campo]) > 45:
                return None, f"El campo {campo} no puede superar 45 caracteres"

    if "total" in resultado:
        try:
            total = Decimal(str(resultado["total"]))

            if not total.is_finite() or total < 0:
                return None, "El total debe ser un número válido mayor o igual a cero"

            resultado["total"] = total

        except (InvalidOperation, ValueError, TypeError):
            return None, "El total debe ser numérico"

    for campo in CAMPOS_ID:
        if campo in resultado:
            valor = resultado[campo]

            if valor is not None:
                if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
                    return None, f"El campo {campo} debe ser un ID entero positivo o null"

    if "fecha_creacion" in resultado:
        valor = resultado["fecha_creacion"]

        if valor is not None:
            if not isinstance(valor, str):
                return None, "fecha_creacion debe ser una fecha ISO en texto"

            try:
                resultado["fecha_creacion"] = datetime.fromisoformat(valor)
            except ValueError:
                return None, "fecha_creacion debe tener formato ISO, por ejemplo 2026-10-13T11:00:00"

    return resultado, None


@pedido_bp.route("/api/pedidos", methods=["GET"])
def listar_pedidos():
    try:
        return jsonify(pedido_dao.obtener_todos()), 200
    except SQLAlchemyError:
        return jsonify({"error": "Error al consultar los pedidos"}), 500


@pedido_bp.route("/api/pedidos/<int:id_pedido>", methods=["GET"])
def obtener_pedido(id_pedido):
    try:
        pedido = pedido_dao.obtener_por_id(id_pedido)

        if pedido is None:
            return jsonify({"error": "Pedido no encontrado"}), 404

        return jsonify(pedido), 200
    except SQLAlchemyError:
        return jsonify({"error": "Error al consultar el pedido"}), 500


@pedido_bp.route("/api/pedidos", methods=["POST"])
def crear_pedido():
    datos, error = validar_datos(request.get_json(silent=True))

    if error:
        return jsonify({"error": error}), 400

    try:
        pedido = pedido_dao.crear(datos)
        return jsonify(pedido), 201
    except IntegrityError:
        return jsonify({
            "error": "Alguna clave foránea no corresponde a un registro existente"
        }), 409
    except SQLAlchemyError:
        return jsonify({"error": "No fue posible crear el pedido"}), 500


@pedido_bp.route("/api/pedidos/<int:id_pedido>", methods=["PUT"])
def actualizar_pedido(id_pedido):
    datos, error = validar_datos(
        request.get_json(silent=True),
        es_actualizacion=True
    )

    if error:
        return jsonify({"error": error}), 400

    try:
        pedido = pedido_dao.actualizar(id_pedido, datos)

        if pedido is None:
            return jsonify({"error": "Pedido no encontrado"}), 404

        return jsonify(pedido), 200
    except IntegrityError:
        return jsonify({
            "error": "Alguna clave foránea no corresponde a un registro existente"
        }), 409
    except SQLAlchemyError:
        return jsonify({"error": "No fue posible actualizar el pedido"}), 500


@pedido_bp.route("/api/pedidos/<int:id_pedido>", methods=["DELETE"])
def eliminar_pedido(id_pedido):
    try:
        eliminado = pedido_dao.eliminar(id_pedido)

        if not eliminado:
            return jsonify({"error": "Pedido no encontrado"}), 404

        return jsonify({"mensaje": "Pedido eliminado correctamente"}), 200
    except IntegrityError:
        return jsonify({
            "error": "No se puede eliminar el pedido porque tiene detalles asociados"
        }), 409
    except SQLAlchemyError:
        return jsonify({"error": "No fue posible eliminar el pedido"}), 500