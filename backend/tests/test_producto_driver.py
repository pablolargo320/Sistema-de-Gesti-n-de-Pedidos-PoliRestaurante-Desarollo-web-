import os
from pathlib import Path
from decimal import Decimal

import mysql.connector
from dotenv import load_dotenv


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


def pausar_si_es_necesario():
    if os.getenv("PAUSAR_TEST_DB") == "1":
        input(
            "\nRevisa MySQL Workbench. "
            "Presiona ENTER para continuar con el DELETE..."
        )


def test_crud_producto_driver():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    id_producto = None

    try:
        cursor.execute(
            """
            INSERT INTO producto
                (nombre, descripcion, precio, disponible,
                 id_categoria, Administrador_id_administrador)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                "Producto Driver Prueba",
                "Creado mediante mysql.connector",
                Decimal("10000.00"),
                1,
                1,
                1,
            ),
        )
        conexion.commit()
        id_producto = cursor.lastrowid
        print (f"\nProducto creado. ID: {id_producto}")
        input("Revisa el producto en Workbench y pulsa ENTER para continuar...")

        assert id_producto is not None

        cursor.execute(
            """
            SELECT nombre, precio
            FROM producto
            WHERE id_producto = %s
            """,
            (id_producto,),
        )
        producto = cursor.fetchone()

        assert producto is not None
        assert producto[0] == "Producto Driver Prueba"
        assert producto[1] == Decimal("10000.00")

        cursor.execute(
            """
            UPDATE producto
            SET nombre = %s, precio = %s
            WHERE id_producto = %s
            """,
            (
                "Producto Driver Actualizado",
                Decimal("15000.00"),
                id_producto,
            ),
        )
        conexion.commit()
        print("Producto actualizado correctamente")
        input("Revisa la actualización en Workbench y pulsa ENTER para continuar...")

        cursor.execute(
            """
            SELECT nombre, precio
            FROM producto
            WHERE id_producto = %s
            """,
            (id_producto,),
        )
        producto = cursor.fetchone()

        assert producto is not None
        assert producto[0] == "Producto Driver Actualizado"
        assert producto[1] == Decimal("15000.00")

        pausar_si_es_necesario()

        cursor.execute(
            "DELETE FROM producto WHERE id_producto = %s",
            (id_producto,),
        )
        conexion.commit()

        cursor.execute(
            "SELECT id_producto FROM producto WHERE id_producto = %s",
            (id_producto,),
        )
        assert cursor.fetchone() is None

        id_producto = None

    finally:
        if id_producto is not None:
            try:
                cursor.execute(
                    "DELETE FROM producto WHERE id_producto = %s",
                    (id_producto,),
                )
                conexion.commit()
                print("Producto eliminado correctamente")
            except mysql.connector.Error:
                conexion.rollback()

        cursor.close()
        conexion.close()

