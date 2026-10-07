from backend.database.database import SessionLocal
from backend.entities.producto import Producto


class ProductoDAO:

    def crear(self, producto):

        db = SessionLocal()

        try:
            db.add(producto)
            db.commit()
            db.refresh(producto)

            return producto

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def obtener_por_id(self, id_producto):

        db = SessionLocal()

        try:
            return db.query(Producto).filter(
                Producto.id_producto == id_producto
            ).first()

        finally:
            db.close()

    def obtener_todos(self):

        db = SessionLocal()

        try:
            return db.query(Producto).all()

        finally:
            db.close()

    def actualizar(self, id_producto, datos):

        db = SessionLocal()

        try:

            producto = db.query(Producto).filter(
                Producto.id_producto == id_producto
            ).first()

            if producto is None:
                return None

            producto.nombre = datos["nombre"]
            producto.descripcion = datos["descripcion"]
            producto.precio = datos["precio"]
            producto.disponible = datos["disponible"]
            producto.id_categoria = datos["id_categoria"]
            producto.Administrador_id_administrador = (
                datos.get("Administrador_id_administrador")
            )

            db.commit()
            db.refresh(producto)

            return producto

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def eliminar(self, id_producto):

        db = SessionLocal()

        try:

            producto = db.query(Producto).filter(
                Producto.id_producto == id_producto
            ).first()

            if producto is None:
                return False

            db.delete(producto)
            db.commit()

            return True

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()