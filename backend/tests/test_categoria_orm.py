
from sqlalchemy import text

from backend.database.database import engine, SessionLocal
from backend.entities.categoria import Categoria


def test_conexion_orm():
    with engine.connect() as connection:
        resultado = connection.execute(text("SELECT 1"))
        assert resultado.scalar() == 1


def test_modelo_categoria():
    assert Categoria.__tablename__ == "categoria"
    assert Categoria.id_categoria is not None
    assert Categoria.nombre is not None


def test_crud_categoria_orm():
    db = SessionLocal()
    id_categoria = None

    try:
        categoria = Categoria(
            nombre="Categoria ORM Prueba"
        )
        db.add(categoria)
        db.commit()
        db.refresh(categoria)

        id_categoria = categoria.id_categoria
        assert id_categoria is not None

        consultada = db.query(Categoria).filter(
            Categoria.id_categoria == id_categoria
        ).first()

        assert consultada is not None
        assert consultada.nombre == "Categoria ORM Prueba"

        consultada.nombre = "Categoria ORM Actualizada"
        db.commit()
        db.refresh(consultada)

        assert consultada.nombre == "Categoria ORM Actualizada"

        db.delete(consultada)
        db.commit()
        id_categoria = None

        eliminada = db.query(Categoria).filter(
            Categoria.id_categoria == consultada.id_categoria
        ).first()

        assert eliminada is None

    except Exception:
        db.rollback()
        raise

    finally:
        if id_categoria is not None:
            try:
                categoria_restante = db.query(Categoria).filter(
                    Categoria.id_categoria == id_categoria
                ).first()

                if categoria_restante is not None:
                    db.delete(categoria_restante)
                    db.commit()
            except Exception:
                db.rollback()

        db.close()