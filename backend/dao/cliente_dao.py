
from backend.database.database import SessionLocal
from backend.entities.cliente import Cliente


class ClienteDAO:

    def crear(self, cliente):
        db = SessionLocal()

        try:
            db.add(cliente)
            db.commit()
            db.refresh(cliente)
            return cliente

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def obtener_por_id(self, id_cliente):
        db = SessionLocal()

        try:
            return db.query(Cliente).filter(
                Cliente.id_cliente == id_cliente
            ).first()

        finally:
            db.close()

    def obtener_todos(self):
        db = SessionLocal()

        try:
            return db.query(Cliente).all()

        finally:
            db.close()

    def actualizar(self, id_cliente, cliente_actualizado):
        db = SessionLocal()

        try:
            cliente = db.query(Cliente).filter(
                Cliente.id_cliente == id_cliente
            ).first()

            if cliente is None:
                return 0

            cliente.nombre = cliente_actualizado.nombre
            cliente.telefono = cliente_actualizado.telefono
            cliente.correo = cliente_actualizado.correo
            cliente.direccion = cliente_actualizado.direccion

            db.commit()
            return 1

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def eliminar(self, id_cliente):
        db = SessionLocal()

        try:
            cliente = db.query(Cliente).filter(
                Cliente.id_cliente == id_cliente
            ).first()

            if cliente is None:
                return 0

            db.delete(cliente)
            db.commit()
            return 1

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()