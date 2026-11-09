
from datetime import datetime

from sqlalchemy import func

from backend.database.database import SessionLocal
from backend.entities.proveedor import Proveedor
from backend.entities.producto import Producto
from backend.entities.solicitud_abastecimiento import SolicitudAbastecimiento
from backend.entities.despacho import Despacho


class SolicitudAbastecimientoDAO:

    @staticmethod
    def convertir_fecha(valor):
        if valor is None:
            return None

        return (
            valor.isoformat(sep=" ")
            if isinstance(valor, datetime)
            else valor.isoformat()
        )

    def convertir_dict(
        self,
        solicitud,
        nombre_proveedor=None,
        nombre_producto=None,
        total_despachado=0
    ):
        total_despachado = int(total_despachado or 0)

        return {
            "id_solicitud": solicitud.id_solicitud,
            "proveedor_id_proveedor": solicitud.proveedor_id_proveedor,
            "proveedor_nombre": nombre_proveedor,
            "producto_id_producto": solicitud.producto_id_producto,
            "producto_nombre": nombre_producto,
            "cantidad_solicitada": solicitud.cantidad_solicitada,
            "cantidad_despachada_total": total_despachado,
            "cantidad_pendiente_despacho": max(
                0,
                solicitud.cantidad_solicitada - total_despachado
            ),
            "fecha_solicitud": self.convertir_fecha(
                solicitud.fecha_solicitud
            ),
            "fecha_requerida": self.convertir_fecha(
                solicitud.fecha_requerida
            ),
            "estado": solicitud.estado,
            "observaciones": solicitud.observaciones,
            "motivo_rechazo": solicitud.motivo_rechazo,
            "fecha_respuesta": self.convertir_fecha(
                solicitud.fecha_respuesta
            )
        }

    def listar(self, proveedor_id=None, estado=None, busqueda=None):

        db = SessionLocal()

        try:

            consulta = (
                db.query(
                    SolicitudAbastecimiento,
                    Proveedor.nombre,
                    Producto.nombre
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
                    SolicitudAbastecimiento.estado == estado
                )

            if busqueda:
                termino = f"%{busqueda.strip()}%"

                if busqueda.strip().isdigit():
                    consulta = consulta.filter(
                        (
                            SolicitudAbastecimiento.id_solicitud ==
                            int(busqueda.strip())
                        )
                        | Producto.nombre.ilike(termino)
                    )
                else:
                    consulta = consulta.filter(
                        Producto.nombre.ilike(termino)
                    )

            filas = consulta.order_by(
                SolicitudAbastecimiento.fecha_solicitud.desc(),
                SolicitudAbastecimiento.id_solicitud.desc()
            ).all()

            ids = [fila[0].id_solicitud for fila in filas]

            totales = {}

            if ids:
                agregados = (
                    db.query(
                        Despacho.solicitud_id_solicitud,
                        func.coalesce(
                            func.sum(Despacho.cantidad_despachada),
                            0
                        )
                    )
                    .filter(
                        Despacho.solicitud_id_solicitud.in_(ids)
                    )
                    .group_by(
                        Despacho.solicitud_id_solicitud
                    )
                    .all()
                )

                totales = {
                    identificador: int(total)
                    for identificador, total in agregados
                }

            return [
                self.convertir_dict(
                    solicitud,
                    nombre_proveedor,
                    nombre_producto,
                    totales.get(solicitud.id_solicitud, 0)
                )
                for (
                    solicitud,
                    nombre_proveedor,
                    nombre_producto
                ) in filas
            ]

        finally:
            db.close()

    def obtener_por_id(self, id_solicitud):

        db = SessionLocal()

        try:

            fila = (
                db.query(
                    SolicitudAbastecimiento,
                    Proveedor.nombre,
                    Producto.nombre
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
                .filter(
                    SolicitudAbastecimiento.id_solicitud ==
                    id_solicitud
                )
                .first()
            )

            if fila is None:
                return None

            total = (
                db.query(
                    func.coalesce(
                        func.sum(Despacho.cantidad_despachada),
                        0
                    )
                )
                .filter(
                    Despacho.solicitud_id_solicitud == id_solicitud
                )
                .scalar()
            )

            return self.convertir_dict(
                fila[0],
                fila[1],
                fila[2],
                total
            )

        finally:
            db.close()

    def crear(
        self,
        proveedor_id,
        cantidad,
        fecha_requerida=None,
        observaciones=None
    ):

        db = SessionLocal()

        try:

            proveedor = db.get(Proveedor, proveedor_id)

            if proveedor is None:
                raise ValueError("El proveedor no existe.")

            if proveedor.producto_id_producto is None:
                raise ValueError(
                    "El proveedor no tiene un producto asociado."
                )

            producto = db.get(
                Producto,
                proveedor.producto_id_producto
            )

            if producto is None:
                raise ValueError(
                    "El producto asociado no existe."
                )

            solicitud = SolicitudAbastecimiento(
                proveedor_id_proveedor=proveedor.id_proveedor,
                producto_id_producto=producto.id_producto,
                cantidad_solicitada=cantidad,
                fecha_requerida=fecha_requerida,
                estado="pendiente",
                observaciones=observaciones
            )

            db.add(solicitud)
            db.commit()
            db.refresh(solicitud)

            return self.convertir_dict(
                solicitud,
                proveedor.nombre,
                producto.nombre
            )

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def actualizar_estado(
        self,
        id_solicitud,
        nuevo_estado,
        motivo_rechazo=None
    ):

        db = SessionLocal()

        try:

            solicitud = db.get(
                SolicitudAbastecimiento,
                id_solicitud
            )

            if solicitud is None:
                return None

            if solicitud.estado != "pendiente":
                raise ValueError(
                    "La solicitud ya fue respondida."
                )

            if nuevo_estado not in ("aceptada", "rechazada"):
                raise ValueError(
                    "El estado no es válido."
                )

            if nuevo_estado == "rechazada":

                if not (motivo_rechazo or "").strip():
                    raise ValueError(
                        "Debes indicar el motivo del rechazo."
                    )

                solicitud.motivo_rechazo = motivo_rechazo.strip()

            else:
                solicitud.motivo_rechazo = None

            solicitud.estado = nuevo_estado
            solicitud.fecha_respuesta = datetime.now()

            db.commit()
            db.refresh(solicitud)

            proveedor = db.get(
                Proveedor,
                solicitud.proveedor_id_proveedor
            )

            producto = db.get(
                Producto,
                solicitud.producto_id_producto
            )

            total = (
                db.query(
                    func.coalesce(
                        func.sum(Despacho.cantidad_despachada),
                        0
                    )
                )
                .filter(
                    Despacho.solicitud_id_solicitud == id_solicitud
                )
                .scalar()
            )

            return self.convertir_dict(
                solicitud,
                proveedor.nombre if proveedor else None,
                producto.nombre if producto else None,
                total
            )

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()
