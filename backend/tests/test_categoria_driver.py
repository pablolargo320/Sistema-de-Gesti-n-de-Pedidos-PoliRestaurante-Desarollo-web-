
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

        print(f"\nCategoria creada. ID: {id_categoria}")
        pausar("Revisa en Workbench el registro recién creado.")

        cursor.execute(
            "SELECT id_categoria, nombre FROM categoria "
            "WHERE id_categoria = %s",
            (id_categoria,)
        )
        categoria = cursor.fetchone()

        assert categoria is not None
        assert categoria[1] == "Categoria Driver Prueba"
        print("Categoria consultada:", categoria)
        pausar("Comprueba los datos consultados.")

        cursor.execute(
            "UPDATE categoria SET nombre = %s "
            "WHERE id_categoria = %s",
            ("Categoria Driver Actualizada", id_categoria)
        )
        conexion.commit()

        cursor.execute(
            "SELECT id_categoria, nombre FROM categoria "
            "WHERE id_categoria = %s",
            (id_categoria,)
        )
        categoria = cursor.fetchone()

        assert categoria is not None
        assert categoria[1] == "Categoria Driver Actualizada"
        print("Categoria actualizada:", categoria)
        pausar("Revisa en Workbench el nombre actualizado.")

        cursor.execute(
            "DELETE FROM categoria WHERE id_categoria = %s",
            (id_categoria,)
        )
        conexion.commit()

        cursor.execute(
            "SELECT id_categoria FROM categoria WHERE id_categoria = %s",
            (id_categoria,)
        )
        assert cursor.fetchone() is None

        print(f"Categoria {id_categoria} eliminada correctamente.")
        id_categoria = None
        pausar("Comprueba que el registro ya no existe.")

    finally:
        if id_categoria is not None:
            try:
                cursor.execute(
                    "DELETE FROM categoria WHERE id_categoria = %s",
                    (id_categoria,)
                )
                conexion.commit()
            except mysql.connector.Error:
                conexion.rollback()

        cursor.close()
        conexion.close()