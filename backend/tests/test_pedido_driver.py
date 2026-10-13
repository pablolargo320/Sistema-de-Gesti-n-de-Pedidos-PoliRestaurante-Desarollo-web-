import os
import mysql.connector
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def obtener_conexion():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "PoliRestaurante1"),
    )


def pausar(mensaje):
    if os.getenv("PAUSAR_TEST_DB") == "1":
        input(f"\n{mensaje}\nPresiona ENTER para continuar...")


def test_crud_pedido_driver():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    id_pedido = None

    try:
        # CREATE
        cursor.execute(
            """
            INSERT INTO pedido
                (fecha_creacion, estado, total, tipo_pedido)
            VALUES
                (NOW(), %s, %s, %s)
            """,
            ("Pendiente (Driver)", 15000, "Prueba Driver")
        )
        conexion.commit()
        id_pedido = cursor.lastrowid

        print(f"\nPedido creado. ID: {id_pedido}")
        pausar("Revisa en Workbench el pedido recién creado.")

        # READ
        cursor.execute(
            """
            SELECT id_pedido, estado, total, tipo_pedido
            FROM pedido
            WHERE id_pedido = %s
            """,
            (id_pedido,)
        )
        pedido = cursor.fetchone()

        assert pedido is not None
        assert pedido[1] == "Pendiente (Driver)"
        assert float(pedido[2]) == 15000.00
        assert pedido[3] == "Prueba Driver"

        print("Pedido consultado:", pedido)
        pausar("Comprueba los datos consultados en Workbench.")

        # UPDATE
        cursor.execute(
            """
            UPDATE pedido
            SET estado = %s, total = %s
            WHERE id_pedido = %s
            """,
            ("Preparando (Driver)", 20000, id_pedido)
        )
        conexion.commit()

        cursor.execute(
            """
            SELECT id_pedido, estado, total
            FROM pedido
            WHERE id_pedido = %s
            """,
            (id_pedido,)
        )
        pedido = cursor.fetchone()

        assert pedido is not None
        assert pedido[1] == "Preparando (Driver)"
        assert float(pedido[2]) == 20000.00

        print("Pedido actualizado:", pedido)
        pausar("Revisa en Workbench el estado y total actualizados.")

        # DELETE
        cursor.execute(
            "DELETE FROM pedido WHERE id_pedido = %s",
            (id_pedido,)
        )
        conexion.commit()

        cursor.execute(
            "SELECT id_pedido FROM pedido WHERE id_pedido = %s",
            (id_pedido,)
        )

        assert cursor.fetchone() is None

        print(f"Pedido {id_pedido} eliminado correctamente.")
        id_pedido = None
        pausar("Comprueba en Workbench que el pedido ya no existe.")

    finally:
        # Limpiar el registro si el test falla antes de terminar
        if id_pedido is not None:
            try:
                cursor.execute(
                    "DELETE FROM pedido WHERE id_pedido = %s",
                    (id_pedido,)
                )
                conexion.commit()
            except mysql.connector.Error:
                conexion.rollback()

        cursor.close()
        conexion.close()