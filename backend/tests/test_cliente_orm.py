
import os
from sqlalchemy import text

from backend.database.database import engine, SessionLocal
from backend.entities.cliente import Cliente


def pausar(mensaje):
    if os.getenv("PAUSAR_TEST_DB") == "1":
        input(f"\n{mensaje}\nPresiona ENTER para continuar...")


def test_conexion_orm():
    with engine.connect() as connection:
        resultado = connection.execute(text("SELECT 1"))
        assert resultado.scalar() == 1


def test_modelo_cliente():
    assert Cliente.__tablename__ == "Cliente"
    assert Cliente.id_cliente is not None
    assert Cliente.nombre is not None
    assert Cliente.telefono is not None
    assert Cliente.correo is not None
    assert Cliente.direccion is not None


def test_crud_cliente_orm():
    db = SessionLocal()
    id_cliente = None

    try:
        cliente = Cliente(
            nombre="Cliente ORM Prueba",
            telefono="3001112233",
            correo="orm.prueba@example.com",
            direccion="Calle ORM 123",
        )

        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        id_cliente = cliente.id_cliente

        print(f"\nCliente creado. ID: {id_cliente}")
        pausar("Revisa en Workbench el cliente recién creado.")

        consultado = db.query(Cliente).filter(
            Cliente.id_cliente == id_cliente
        ).first()

        assert consultado is not None
        assert consultado.nombre == "Cliente ORM Prueba"
        assert consultado.correo == "orm.prueba@example.com"

        print("Cliente consultado:", consultado.nombre)
        pausar("Comprueba los datos consultados.")

        consultado.nombre = "Cliente ORM Actualizado"
        consultado.telefono = "3009998877"

        db.commit()
        db.refresh(consultado)

        assert consultado.nombre == "Cliente ORM Actualizado"
        assert consultado.telefono == "3009998877"

        print(
            "Cliente actualizado:",
            consultado.nombre,
            consultado.telefono,
        )
        pausar("Revisa en Workbench los cambios realizados.")

        db.delete(consultado)
        db.commit()

        eliminado = db.query(Cliente).filter(
            Cliente.id_cliente == id_cliente
        ).first()

        assert eliminado is None

        print(f"Cliente {id_cliente} eliminado correctamente.")
        id_cliente = None
        pausar("Comprueba que el cliente ya no existe.")

    except Exception:
        db.rollback()
        raise

    finally:
        if id_cliente is not None:
            try:
                restante = db.query(Cliente).filter(
                    Cliente.id_cliente == id_cliente
                ).first()

                if restante is not None:
                    db.delete(restante)
                    db.commit()
            except Exception:
                db.rollback()

        db.close()