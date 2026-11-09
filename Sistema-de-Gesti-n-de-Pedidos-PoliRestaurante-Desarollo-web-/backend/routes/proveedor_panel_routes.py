from flask import Blueprint, current_app, jsonify

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from backend.database.database import SessionLocal

from backend.entities.proveedor import Proveedor
from backend.entities.despacho import Despacho
from backend.entities.solicitud_abastecimiento import SolicitudAbastecimiento

from backend.dao.despacho_dao import DespachoDAO


proveedor_panel_routes = Blueprint(
    "proveedor_panel_routes",
    __name__
)

despacho_dao = DespachoDAO()


@proveedor_panel_routes.route(
    "/api/proveedores/<int:id_proveedor>/historial",
    methods=["GET"]
)
def historial_proveedor(id_proveedor):

    db = SessionLocal()

    try:

        proveedor = db.get(Proveedor, id_proveedor)

        if proveedor is None:
            return jsonify({
                "error": "Proveedor no encontrado."
            }), 404

    except SQLAlchemyError:
        current_app.logger.exception(
            "Error verificando proveedor"
        )

        return jsonify({
            "error": "No fue posible consultar el historial."
        }), 500

    finally:
        db.close()

    try:

        historial = despacho_dao.obtener_historial(
            id_proveedor
        )

        return jsonify(historial), 200

    except SQLAlchemyError:
        current_app.logger.exception(
            "Error consultando historial"
        )

        return jsonify({
            "error": "No fue posible consultar el historial."
        }), 500


@proveedor_panel_routes.route(
    "/api/proveedores/<int:id_proveedor>/resumen",
    methods=["GET"]
)
def resumen_proveedor(id_proveedor):

    db = SessionLocal()

    try:

        proveedor = db.get(Proveedor, id_proveedor)

        if proveedor is None:
            return jsonify({
                "error": "Proveedor no encontrado."
            }), 404

        solicitudes_pendientes = (
            db.query(
                func.count(
                    SolicitudAbastecimiento.id_solicitud
                )
            )
            .filter(
                SolicitudAbastecimiento.proveedor_id_proveedor
                == id_proveedor,
                SolicitudAbastecimiento.estado == "pendiente"
            )
            .scalar()
        )

        despachos_en_proceso = (
            db.query(func.count(Despacho.id_despacho))
            .join(
                SolicitudAbastecimiento,
                SolicitudAbastecimiento.id_solicitud
                == Despacho.solicitud_id_solicitud
            )
            .filter(
                SolicitudAbastecimiento.proveedor_id_proveedor
                == id_proveedor,
                Despacho.estado.in_([
                    "preparando",
                    "despachado",
                    "en_transito",
                    "con_novedad"
                ])
            )
            .scalar()
        )

        return jsonify({
            "id_proveedor": id_proveedor,
            "solicitudes_pendientes": int(
                solicitudes_pendientes or 0
            ),
            "despachos_en_proceso": int(
                despachos_en_proceso or 0
            ),
            "productos_asociados": (
                1 if proveedor.producto_id_producto else 0
            )
        }), 200

    except SQLAlchemyError:
        current_app.logger.exception(
            "Error consultando resumen"
        )

        return jsonify({
            "error": "No fue posible consultar el resumen."
        }), 500

    finally:
        db.close()