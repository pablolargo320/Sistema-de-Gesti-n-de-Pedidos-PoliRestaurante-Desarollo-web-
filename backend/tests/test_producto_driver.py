
import os
import mysql.connector
import pytest
from decimal import Decimal


def obtener_conexion():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "Camilo"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "PoliRestaurante1"),
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
            ("Producto Driver Actualizado", Decimal("15000.00"), id_producto),
        )
        conexion.commit()

        cursor.execute(
            "SELECT nombre, precio FROM producto WHERE id_producto = %s",
            (id_producto,),
        )
        producto = cursor.fetchone()

        assert producto[0] == "Producto Driver Actualizado"
        assert producto[1] == Decimal("15000.00")

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

    finally:
        if id_producto is not None:
            try:
                conexion.rollback()
                cursor.execute(
                    "DELETE FROM producto WHERE id_producto = %s",
                    (id_producto,),
                )
                conexion.commit()
            except mysql.connector.Error:
                conexion.rollback()

        cursor.close()
        conexion.close()