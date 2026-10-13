from backend.database.database import SessionLocal
from backend.entities.proveedor import Proveedor


class ProveedorDAO:

    def _convertir_dict(self, proveedor):
        return {
            "id_proveedor": proveedor.id_proveedor,
            "nombre": proveedor.nombre,
            "telefono": proveedor.telefono,
            "correo": proveedor.correo,
            "direccion": proveedor.direccion,
            "producto_id_producto": proveedor.producto_id_producto
        }

    def crear(self, datos):
        db = SessionLocal()

        try:
            proveedor = Proveedor(**datos)

            db.add(proveedor)
            db.commit()
            db.refresh(proveedor)

            return self._convertir_dict(proveedor)

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def obtener_todos(self):
        db = SessionLocal()

        try:
            proveedores = (
                db.query(Proveedor)
                .order_by(Proveedor.id_proveedor)
                .all()
            )

            return [
                self._convertir_dict(proveedor)
                for proveedor in proveedores
            ]

        finally:
            db.close()

    def obtener_por_id(self, id_proveedor):
        db = SessionLocal()

        try:
            proveedor = db.get(Proveedor, id_proveedor)

            if proveedor is None:
                return None

            return self._convertir_dict(proveedor)

        finally:
            db.close()

    def actualizar(self, id_proveedor, datos):
        db = SessionLocal()

        try:
            proveedor = db.get(Proveedor, id_proveedor)

            if proveedor is None:
                return None

            proveedor.nombre = datos["nombre"]
            proveedor.telefono = datos["telefono"]
            proveedor.correo = datos["correo"]
            proveedor.direccion = datos["direccion"]
            proveedor.producto_id_producto = (
                datos["producto_id_producto"]
            )

            db.commit()
            db.refresh(proveedor)

            return self._convertir_dict(proveedor)

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def eliminar(self, id_proveedor):
        db = SessionLocal()

        try:
            proveedor = db.get(Proveedor, id_proveedor)

            if proveedor is None:
                return False

            db.delete(proveedor)
            db.commit()

            return True

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()