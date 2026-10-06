from backend.database.database import SessionLocal
from backend.entities.categoria import Categoria


class CategoriaDAO:

    def crear(self, categoria):
        db = SessionLocal()

        try:
            db.add(categoria)
            db.commit()
            db.refresh(categoria)

            return categoria

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def obtener_por_id(self, id_categoria):
        db = SessionLocal()

        try:
            return db.query(Categoria).filter(
                Categoria.id_categoria == id_categoria
            ).first()

        finally:
            db.close()

    def obtener_todas(self):
        db = SessionLocal()

        try:
            return db.query(Categoria).all()

        finally:
            db.close()

    def actualizar(self, id_categoria, categoria_actualizada):
        db = SessionLocal()

        try:
            categoria = db.query(Categoria).filter(
                Categoria.id_categoria == id_categoria
            ).first()

            if categoria is None:
                return 0

            categoria.nombre = categoria_actualizada.nombre

            db.commit()

            return 1

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def eliminar(self, id_categoria):
        db = SessionLocal()

        try:
            categoria = db.query(Categoria).filter(
                Categoria.id_categoria == id_categoria
            ).first()

            if categoria is None:
                return 0

            db.delete(categoria)
            db.commit()

            return 1

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()