
import os
import mysql.connector


def obtener_conexion():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "Camilo"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "PoliRestaurante1"),
    )


def test_crud_categoria_driver():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    id_categoria = None

    try:
        cursor.execute(
            "INSERT INTO categoria (nombre) VALUES (%s)",
            ("Categoria Driver Prueba",)
        )
        conexion.commit()
        id_categoria = cursor.lastrowid

        assert id_categoria is not None

        cursor.execute(
            """
            SELECT nombre
            FROM categoria
            WHERE id_categoria = %s
            """,
            (id_categoria,)
        )
        categoria = cursor.fetchone()

        assert categoria is not None
        assert categoria[0] == "Categoria Driver Prueba"

        cursor.execute(
            """
            UPDATE categoria
            SET nombre = %s
            WHERE id_categoria = %s
            """,
            ("Categoria Driver Actualizada", id_categoria)
        )
        conexion.commit()

        cursor.execute(
            """
            SELECT nombre
            FROM categoria
            WHERE id_categoria = %s
            """,
            (id_categoria,)
        )
        categoria = cursor.fetchone()

        assert categoria is not None
        assert categoria[0] == "Categoria Driver Actualizada"

        cursor.execute(
            "DELETE FROM categoria WHERE id_categoria = %s",
            (id_categoria,)
        )
        conexion.commit()
        id_categoria = None

    finally:
        if id_categoria is not None:
            try:
                conexion.rollback()
                cursor.execute(
                    "DELETE FROM categoria WHERE id_categoria = %s",
                    (id_categoria,)
                )
                conexion.commit()
            except mysql.connector.Error:
                conexion.rollback()

        cursor.close()
        conexion.close()