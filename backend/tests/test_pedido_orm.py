import os
from sqlalchemy import text

from backend.database.database import engine, SessionLocal
from backend.entities.administrador import Administrador
from backend.entities.pedido import Pedido
from backend.entities.cliente import Cliente
from backend.entities.mesa import Mesa
from backend.entities.domiciliario import Domiciliario
from backend.entities.metodo_pago import MetodoPago


def pausar(mensaje):
    if os.getenv("PAUSAR_TEST_DB") == "1":
        input(f"\n{mensaje}\nPresiona ENTER para continuar...")


def test_conexion_orm():
    with engine.connect() as connection:
        resultado = connection.execute(text("SELECT 1"))
        assert resultado.scalar() == 1


def test_modelo_pedido():
    assert Pedido.__tablename__ == "pedido"
    assert Pedido.id_pedido is not None
    assert Pedido.fecha_creacion is not None
    assert Pedido.estado is not None
    assert Pedido.total is not None
    assert Pedido.tipo_pedido is not None


def test_crud_pedido_orm():
    db = SessionLocal()
    id_pedido = None

    try:
        # CREATE
        pedido = Pedido(
            estado="Pendiente (ORM)",
            total=18000,
            tipo_pedido="Prueba ORM",
        )

        db.add(pedido)
        db.commit()
        db.refresh(pedido)

        id_pedido = pedido.id_pedido

        print(f"\nPedido creado con ORM. ID: {id_pedido}")
        pausar("Revisa en Workbench el pedido recién creado por ORM.")

        # READ
        consultado = db.query(Pedido).filter(
            Pedido.id_pedido == id_pedido
        ).first()

        assert consultado is not None
        assert consultado.estado == "Pendiente (ORM)"
        assert float(consultado.total) == 18000.00
        assert consultado.tipo_pedido == "Prueba ORM"

        print("Pedido consultado:", consultado.estado, consultado.total)
        pausar("Comprueba los datos consultados por ORM.")

        # UPDATE
        consultado.estado = "Preparando (ORM)"
        consultado.total = 25000

        db.commit()
        db.refresh(consultado)

        assert consultado.estado == "Preparando (ORM)"
        assert float(consultado.total) == 25000.00

        print("Pedido actualizado:", consultado.estado, consultado.total)
        pausar("Revisa en Workbench los datos actualizados por ORM.")

        # DELETE
        db.delete(consultado)
        db.commit()

        eliminada = db.query(Pedido).filter(
            Pedido.id_pedido == id_pedido
        ).first()

        assert eliminada is None

        print(f"Pedido {id_pedido} eliminado correctamente con ORM.")
        id_pedido = None
        pausar("Comprueba que el pedido temporal ya no existe.")

    except Exception:
        db.rollback()
        raise

    finally:
        # Limpiar el registro si la prueba falla
        if id_pedido is not None:
            try:
                restante = db.query(Pedido).filter(
                    Pedido.id_pedido == id_pedido
                ).first()

                if restante is not None:
                    db.delete(restante)
                    db.commit()

            except Exception:
                db.rollback()

        db.close()