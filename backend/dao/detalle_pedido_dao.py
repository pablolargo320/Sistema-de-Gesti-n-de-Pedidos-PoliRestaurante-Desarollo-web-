
from backend.database.database import SessionLocal
from backend.entities.detalle_pedido import DetallePedido
from backend.database.database import SessionLocal, registrar_modelos


registrar_modelos()


class DetallePedidoDAO:

    def crear(self, detalle):
        db = SessionLocal()
        try:
            db.add(detalle)
            db.commit()
            db.refresh(detalle)
            return detalle
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def obtener_por_id(self, id_detalle):
        db = SessionLocal()
        try:
            return db.query(DetallePedido).filter(
                DetallePedido.id_detalle == id_detalle
            ).first()
        finally:
            db.close()

    def obtener_todos(self):
        db = SessionLocal()
        try:
            return db.query(DetallePedido).all()
        finally:
            db.close()

    def obtener_por_pedido(self, id_pedido):
        db = SessionLocal()
        try:
            return db.query(DetallePedido).filter(
                DetallePedido.id_pedido == id_pedido
            ).all()
        finally:
            db.close()

    def actualizar(self, id_detalle, detalle_actualizado):
        db = SessionLocal()
        try:
            detalle = db.query(DetallePedido).filter(
                DetallePedido.id_detalle == id_detalle
            ).first()

            if detalle is None:
                return 0

            detalle.cantidad = detalle_actualizado.cantidad
            detalle.notas = detalle_actualizado.notas
            detalle.subtotal = detalle_actualizado.subtotal
            detalle.id_pedido = detalle_actualizado.id_pedido
            detalle.id_producto = detalle_actualizado.id_producto

            db.commit()
            return 1

        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def eliminar(self, id_detalle):
        db = SessionLocal()
        try:
            detalle = db.query(DetallePedido).filter(
                DetallePedido.id_detalle == id_detalle
            ).first()

            if detalle is None:
                return 0

            db.delete(detalle)
            db.commit()
            return 1

        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

