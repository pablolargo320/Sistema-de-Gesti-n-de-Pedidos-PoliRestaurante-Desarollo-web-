from backend.database.database import SessionLocal
from backend.entities.domiciliario import Domiciliario


class DomiciliarioDAO:

    def _convertir_dict(self, domiciliario):
        return {
            "id_domiciliario": domiciliario.id_domiciliario,
            "nombre": domiciliario.nombre,
            "apellido": domiciliario.apellido,
            "telefono": domiciliario.telefono,
            "correo": domiciliario.correo,
            "direccion": domiciliario.direccion,
            "estado": domiciliario.estado,
            "tipo_vehiculo": domiciliario.tipo_vehiculo,
            "placa_vehiculo": domiciliario.placa_vehiculo
        }

    def crear(self, datos):
        db = SessionLocal()

        try:
            domiciliario = Domiciliario(**datos)

            db.add(domiciliario)
            db.commit()
            db.refresh(domiciliario)

            return self._convertir_dict(domiciliario)

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def obtener_todos(self):
        db = SessionLocal()

        try:
            domiciliarios = (
                db.query(Domiciliario)
                .order_by(Domiciliario.id_domiciliario)
                .all()
            )

            return [
                self._convertir_dict(domiciliario)
                for domiciliario in domiciliarios
            ]

        finally:
            db.close()

    def obtener_por_id(self, id_domiciliario):
        db = SessionLocal()

        try:
            domiciliario = db.get(
                Domiciliario,
                id_domiciliario
            )

            if domiciliario is None:
                return None

            return self._convertir_dict(domiciliario)

        finally:
            db.close()

    def actualizar(self, id_domiciliario, datos):
        db = SessionLocal()

        try:
            domiciliario = db.get(
                Domiciliario,
                id_domiciliario
            )

            if domiciliario is None:
                return None

            domiciliario.nombre = datos["nombre"]
            domiciliario.apellido = datos["apellido"]
            domiciliario.telefono = datos["telefono"]
            domiciliario.correo = datos["correo"]
            domiciliario.direccion = datos["direccion"]
            domiciliario.estado = datos["estado"]
            domiciliario.tipo_vehiculo = datos["tipo_vehiculo"]
            domiciliario.placa_vehiculo = datos["placa_vehiculo"]

            db.commit()
            db.refresh(domiciliario)

            return self._convertir_dict(domiciliario)

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def eliminar(self, id_domiciliario):
        db = SessionLocal()

        try:
            domiciliario = db.get(
                Domiciliario,
                id_domiciliario
            )

            if domiciliario is None:
                return False

            db.delete(domiciliario)
            db.commit()

            return True

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()