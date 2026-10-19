
import os

from sqlalchemy import text

from backend.database.database import engine, SessionLocal
from backend.entities.detalle_pedido import DetallePedido
from backend.entities.producto import Producto
from backend.entities.pedido import Pedido
from backend.entities.producto import Producto



def pausar(mensaje):
    if os.getenv("PAUSAR_TEST_DB") == "1":
        input(f"\n{mensaje}\nPresiona ENTER para continuar...")


def test_conexion_orm():
    with engine.connect() as connection:
        resultado = connection.execute(text("SELECT 1"))
        assert resultado.scalar() == 1


def test_modelo_detalle_pedido():
    assert DetallePedido.__tablename__ == "detalle_pedido"
    assert DetallePedido.id_detalle is not None
    assert DetallePedido.cantidad is not None
    assert DetallePedido.notas is not None
    assert DetallePedido.subtotal is not None
    assert DetallePedido.id_pedido is not None
    assert DetallePedido.id_producto is not None


def test_crud_detalle_pedido_orm():
    db = SessionLocal()
    id_detalle = None

    try:
        # Buscar registros existentes para respetar las claves foraneas.
        id_pedido = db.execute(
            text("SELECT id_pedido FROM pedido LIMIT 1")
        ).scalar()

        id_producto = db.execute(
            text("SELECT id_producto FROM producto LIMIT 1")
        ).scalar()

        assert id_pedido is not None, (
            "No hay pedidos en la base de datos."
        )
        assert id_producto is not None, (
            "No hay productos en la base de datos."
        )

        # CREATE
        detalle = DetallePedido(
            cantidad=2,
            notas="Prueba ORM temporal",
            subtotal=10000.00,
            id_pedido=id_pedido,
            id_producto=id_producto
        )

        db.add(detalle)
        db.commit()
        db.refresh(detalle)

        id_detalle = detalle.id_detalle

        print(f"\nDetalle creado. ID: {id_detalle}")
        pausar("Revisa en Workbench el detalle recién creado.")

        # READ
        consultado = db.query(DetallePedido).filter(
            DetallePedido.id_detalle == id_detalle
        ).first()

        assert consultado is not None
        assert consultado.cantidad == 2
        assert consultado.notas == "Prueba ORM temporal"

        print("Detalle consultado:", consultado.notas)
        pausar("Comprueba los datos consultados.")

        # UPDATE
        consultado.cantidad = 3
        consultado.notas = "Prueba ORM actualizada"
        consultado.subtotal = 15000.00

        db.commit()
        db.refresh(consultado)

        assert consultado.cantidad == 3
        assert consultado.notas == "Prueba ORM actualizada"
        assert float(consultado.subtotal) == 15000.00

        print("Detalle actualizado:", consultado.notas)
        pausar("Revisa en Workbench los cambios realizados.")

        # DELETE
        db.delete(consultado)
        db.commit()

        eliminado = db.query(DetallePedido).filter(
            DetallePedido.id_detalle == id_detalle
        ).first()

        assert eliminado is None

        print(f"Detalle {id_detalle} eliminado correctamente.")
        id_detalle = None

        pausar("Comprueba que el registro ya no existe.")

    except Exception:
        db.rollback()
        raise

    finally:
        # Si falla la prueba, intentar eliminar el registro temporal.
        if id_detalle is not None:
            try:
                restante = db.query(DetallePedido).filter(
                    DetallePedido.id_detalle == id_detalle
                ).first()

                if restante is not None:
                    db.delete(restante)
                    db.commit()
            except Exception:
                db.rollback()

        db.close()