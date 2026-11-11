
from datetime import datetime

from sqlalchemy import func

from backend.database.database import SessionLocal
from backend.entities.despacho import Despacho
from backend.entities.solicitud_abastecimiento import SolicitudAbastecimiento
from backend.entities.proveedor import Proveedor
from backend.entities.producto import Producto


class DespachoDAO:

    def convertir_fecha(self, valor):
        if valor is None:
            return None

        return (
            valor.isoformat(sep=" ")
            if isinstance(valor, datetime)
            else valor.isoformat()
        )

    def convertir_dict(
        self,
        despacho,
        solicitud=None,
        proveedor_nombre=None,
        producto_nombre=None
    ):

        return {
            "id_despacho": despacho.id_despacho,
            "solicitud_id_solicitud": despacho.solicitud_id_solicitud,
            "proveedor_id_proveedor": (
                solicitud.proveedor_id_proveedor
                if solicitud else None
            ),
            "proveedor_nombre": proveedor_nombre,
            "producto_nombre": producto_nombre,
            "cantidad_solicitada": (
                solicitud.cantidad_solicitada
                if solicitud else None
            ),
            "cantidad_despachada": despacho.cantidad_despachada,
            "fecha_despacho": self.convertir_fecha(
                despacho.fecha_despacho
            ),
            "fecha_entrega_estimada": self.convertir_fecha(
                despacho.fecha_entrega_estimada
            ),
            "fecha_entrega_real": self.convertir_fecha(
                despacho.fecha_entrega_real
            ),
            "numero_guia": despacho.numero_guia,
            "transportadora": despacho.transportadora,
            "estado": despacho.estado,
            "observaciones": despacho.observaciones
        }

    def listar(self, proveedor_id=None, estado=None):

        db = SessionLocal()

        try:

            consulta = (
                db.query(
                    Despacho,
                    SolicitudAbastecimiento,
                    Proveedor.nombre,
                    Producto.nombre
                )
                .join(
                    SolicitudAbastecimiento,
                    SolicitudAbastecimiento.id_solicitud ==
                    Despacho.solicitud_id_solicitud
                )
                .join(
                    Proveedor,
                    Proveedor.id_proveedor ==
                    SolicitudAbastecimiento.proveedor_id_proveedor
                )
                .join(
                    Producto,
                    Producto.id_producto ==
                    SolicitudAbastecimiento.producto_id_producto
                )
            )

            if proveedor_id is not None:
                consulta = consulta.filter(
                    SolicitudAbastecimiento.proveedor_id_proveedor ==
                    proveedor_id
                )

            if estado:
                consulta = consulta.filter(
                    Despacho.estado == estado
                )

            filas = consulta.order_by(
                Despacho.fecha_despacho.desc(),
                Despacho.id_despacho.desc()
            ).all()

            return [
                self.convertir_dict(
                    despacho,
                    solicitud,
                    proveedor_nombre,
                    producto_nombre
                )
                for (
                    despacho,
                    solicitud,
                    proveedor_nombre,
                    producto_nombre
                ) in filas
            ]

        finally:
            db.close()

    def crear(
        self,
        solicitud_id,
        cantidad,
        fecha_entrega_estimada=None,
        numero_guia=None,
        transportadora=None,
        observaciones=None
    ):

        db = SessionLocal()

        try:

            solicitud = db.get(
                SolicitudAbastecimiento,
                solicitud_id
            )

            if solicitud is None:
                raise ValueError(
                    "La solicitud seleccionada no existe."
                )

            if solicitud.estado not in ("aceptada", "en_despacho"):
                raise ValueError(
                    "Solo se pueden registrar despachos para solicitudes aceptadas."
                )

            total_actual = (
                db.query(
                    func.coalesce(
                        func.sum(Despacho.cantidad_despachada),
                        0
                    )
                )
                .filter(
                    Despacho.solicitud_id_solicitud == solicitud_id
                )
                .scalar()
            )

            restante = (
                solicitud.cantidad_solicitada -
                int(total_actual or 0)
            )

            if cantidad > restante:
                raise ValueError(
                    f"La cantidad supera lo pendiente. Máximo disponible: {restante}."
                )

            despacho = Despacho(
                solicitud_id_solicitud=solicitud_id,
                cantidad_despachada=cantidad,
                fecha_entrega_estimada=fecha_entrega_estimada,
                numero_guia=numero_guia,
                transportadora=transportadora,
                estado="preparando",
                observaciones=observaciones
            )

            db.add(despacho)
            solicitud.estado = "en_despacho"

            db.commit()
            db.refresh(despacho)

            proveedor = db.get(
                Proveedor,
                solicitud.proveedor_id_proveedor
            )

            producto = db.get(
                Producto,
                solicitud.producto_id_producto
            )

            return self.convertir_dict(
                despacho,
                solicitud,
                proveedor.nombre if proveedor else None,
                producto.nombre if producto else None
            )

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def actualizar_estado(self, id_despacho, nuevo_estado):

        transiciones = {
            "preparando": {"despachado", "con_novedad"},
            "despachado": {"en_transito", "entregado", "con_novedad"},
            "en_transito": {"entregado", "con_novedad"},
            "con_novedad": {"despachado", "en_transito"},
            "entregado": set()
        }

        if nuevo_estado not in transiciones:
            raise ValueError(
                "El estado del despacho no es válido."
            )

        db = SessionLocal()

        try:

            despacho = db.get(Despacho, id_despacho)

            if despacho is None:
                return None

            if nuevo_estado not in transiciones[despacho.estado]:
                raise ValueError(
                    f"No se puede cambiar de {despacho.estado} a {nuevo_estado}."
                )

            despacho.estado = nuevo_estado

            if nuevo_estado == "entregado":
                despacho.fecha_entrega_real = datetime.now()

            solicitud = db.get(
                SolicitudAbastecimiento,
                despacho.solicitud_id_solicitud
            )

            db.flush()

            if nuevo_estado == "entregado" and solicitud:

                despachos = (
                    db.query(Despacho)
                    .filter(
                        Despacho.solicitud_id_solicitud ==
                        solicitud.id_solicitud
                    )
                    .all()
                )

                total_despachado = sum(
                    item.cantidad_despachada
                    for item in despachos
                )

                todos_entregados = all(
                    item.estado == "entregado"
                    for item in despachos
                )

                if (
                    todos_entregados
                    and total_despachado >= solicitud.cantidad_solicitada
                ):
                    solicitud.estado = "completada"

            db.commit()
            db.refresh(despacho)

            proveedor = db.get(
                Proveedor,
                solicitud.proveedor_id_proveedor
            ) if solicitud else None

            producto = db.get(
                Producto,
                solicitud.producto_id_producto
            ) if solicitud else None

            return self.convertir_dict(
                despacho,
                solicitud,
                proveedor.nombre if proveedor else None,
                producto.nombre if producto else None
            )

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def obtener_historial(self, proveedor_id):

        db = SessionLocal()
        eventos = []

        try:

            solicitudes = (
                db.query(
                    SolicitudAbastecimiento,
                    Producto.nombre
                )
                .join(
                    Producto,
                    Producto.id_producto ==
                    SolicitudAbastecimiento.producto_id_producto
                )
                .filter(
                    SolicitudAbastecimiento.proveedor_id_proveedor ==
                    proveedor_id
                )
                .all()
            )

            for solicitud, producto_nombre in solicitudes:

                eventos.append({
                    "tipo": "Solicitud",
                    "id": solicitud.id_solicitud,
                    "fecha": self.convertir_fecha(
                        solicitud.fecha_solicitud
                    ),
                    "referencia": f"Solicitud #{solicitud.id_solicitud}",
                    "detalle": (
                        f"{solicitud.cantidad_solicitada} unidades "
                        f"de {producto_nombre}"
                    ),
                    "estado": solicitud.estado
                })

            despachos = (
                db.query(
                    Despacho,
                    SolicitudAbastecimiento,
                    Producto.nombre
                )
                .join(
                    SolicitudAbastecimiento,
                    SolicitudAbastecimiento.id_solicitud ==
                    Despacho.solicitud_id_solicitud
                )
                .join(
                    Producto,
                    Producto.id_producto ==
                    SolicitudAbastecimiento.producto_id_producto
                )
                .filter(
                    SolicitudAbastecimiento.proveedor_id_proveedor ==
                    proveedor_id
                )
                .all()
            )

            for despacho, solicitud, producto_nombre in despachos:

                eventos.append({
                    "tipo": "Despacho",
                    "id": despacho.id_despacho,
                    "fecha": self.convertir_fecha(
                        despacho.fecha_entrega_real or despacho.fecha_despacho
                    ),
                    "referencia": (
                        despacho.numero_guia or
                        f"Despacho #{despacho.id_despacho}"
                    ),
                    "detalle": (
                        f"{despacho.cantidad_despachada} unidades "
                        f"de {producto_nombre} · "
                        f"Solicitud #{solicitud.id_solicitud}"
                    ),
                    "estado": despacho.estado
                })

            eventos.sort(
                key=lambda item: item["fecha"] or "",
                reverse=True
            )

            return eventos

        finally:
            db.close()
