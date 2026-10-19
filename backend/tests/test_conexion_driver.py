import os
from pathlib import Path

from dotenv import load_dotenv

from backend.database.connection import get_connection

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def test_conexion_directa_mysql():
    conexion = get_connection()
    cursor = None

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT DATABASE(), 1")
        nombre_bd, resultado = cursor.fetchone()

        assert nombre_bd.lower() == os.getenv("DB_NAME").lower()
        assert resultado == 1

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()