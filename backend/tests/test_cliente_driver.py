
import os

from backend.database.connection import get_connection


def pausar(mensaje):
    if os.getenv("PAUSAR_TEST_DB") == "1":
        input(f"\n{mensaje}\nPresiona ENTER para continuar...")


def test_crud_cliente_driver():
    conexion = get_connection()
    cursor = conexion.cursor()
    id_cliente = None

    try:
        cursor.execute(
            """
            INSERT INTO Cliente (nombre, telefono, correo, direccion)
            VALUES (%s, %s, %s, %s)
            """,
            (
                "Cliente Driver Prueba",
                "3001112233",
                "driver.prueba@example.com",
                "Calle de prueba 123",
            )
        )
        conexion.commit()
        id_cliente = cursor.lastrowid

        print(f"\nCliente creado. ID: {id_cliente}")
        pausar("Revisa en Workbench el cliente recién creado.")

        cursor.execute(
            """
            SELECT id_cliente, nombre, telefono, correo, direccion
            FROM Cliente WHERE id_cliente = %s
            """,
            (id_cliente,)
        )
        cliente = cursor.fetchone()

        assert cliente is not None
        assert cliente[1] == "Cliente Driver Prueba"
        assert cliente[2] == "3001112233"
        assert cliente[3] == "driver.prueba@example.com"

        print("Cliente consultado:", cliente)
        pausar("Comprueba los datos consultados.")

        cursor.execute(
            """
            UPDATE Cliente
            SET nombre = %s, telefono = %s
            WHERE id_cliente = %s
            """,
            ("Cliente Driver Actualizado", "3009998877", id_cliente)
        )
        conexion.commit()

        cursor.execute(
            """
            SELECT id_cliente, nombre, telefono, correo, direccion
            FROM Cliente WHERE id_cliente = %s
            """,
            (id_cliente,)
        )
        cliente = cursor.fetchone()

        assert cliente is not None
        assert cliente[1] == "Cliente Driver Actualizado"
        assert cliente[2] == "3009998877"

        print("Cliente actualizado:", cliente)
        pausar("Revisa en Workbench los cambios realizados.")

        cursor.execute(
            "DELETE FROM Cliente WHERE id_cliente = %s",
            (id_cliente,)
        )
        conexion.commit()

        cursor.execute(
            "SELECT id_cliente FROM Cliente WHERE id_cliente = %s",
            (id_cliente,)
        )
        assert cursor.fetchone() is None

        print(f"Cliente {id_cliente} eliminado correctamente.")
        id_cliente = None
        pausar("Comprueba que el cliente ya no existe.")

    finally:
        if id_cliente is not None:
            try:
                cursor.execute(
                    "DELETE FROM Cliente WHERE id_cliente = %s",
                    (id_cliente,)
                )
                conexion.commit()
            except Exception:
                conexion.rollback()

        cursor.close()
        conexion.close()