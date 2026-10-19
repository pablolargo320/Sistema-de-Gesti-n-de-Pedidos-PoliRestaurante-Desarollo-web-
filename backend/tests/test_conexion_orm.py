import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text

from backend.database.database import engine

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def test_conexion_orm_mysql():
    with engine.connect() as conexion:
        fila = conexion.execute(
            text("SELECT DATABASE(), 1")
        ).one()

    nombre_bd, resultado = fila

    assert nombre_bd.lower() == os.getenv("DB_NAME").lower()
    assert resultado == 1