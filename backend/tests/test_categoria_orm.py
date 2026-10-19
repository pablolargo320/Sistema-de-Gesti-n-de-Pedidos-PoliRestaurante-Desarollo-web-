
import os
from sqlalchemy import text

from backend.database.database import engine, SessionLocal
from backend.entities.categoria import Categoria


def pausar(mensaje):
    if os.getenv("PAUSAR_TEST_DB") == "1":
        input(f"\n{mensaje}\nPresiona ENTER para continuar...")


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
        categoria = Categoria(nombre="Categoria ORM Prueba")
        db.add(categoria)
        db.commit()
        db.refresh(categoria)

        id_categoria = categoria.id_categoria
        print(f"\nCategoria creada. ID: {id_categoria}")
        pausar("Revisa en Workbench el registro recién creado.")

        consultada = db.query(Categoria).filter(
            Categoria.id_categoria == id_categoria
        ).first()

        assert consultada is not None
        assert consultada.nombre == "Categoria ORM Prueba"
        print("Categoria consultada:", consultada.nombre)
        pausar("Comprueba los datos consultados.")

        consultada.nombre = "Categoria ORM Actualizada"
        db.commit()
        db.refresh(consultada)

        assert consultada.nombre == "Categoria ORM Actualizada"
        print("Categoria actualizada:", consultada.nombre)
        pausar("Revisa en Workbench el nombre actualizado.")

        db.delete(consultada)
        db.commit()

        eliminada = db.query(Categoria).filter(
            Categoria.id_categoria == id_categoria
        ).first()

        assert eliminada is None
        print(f"Categoria {id_categoria} eliminada correctamente.")

        id_categoria = None
        pausar("Comprueba que el registro ya no existe.")

    except Exception:
        db.rollback()
        raise

    finally:
        if id_categoria is not None:
            try:
                restante = db.query(Categoria).filter(
                    Categoria.id_categoria == id_categoria
                ).first()

                if restante is not None:
                    db.delete(restante)
                    db.commit()
            except Exception:
                db.rollback()

        db.close()