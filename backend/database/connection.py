import os
from pathlib import Path
import mysql.connector
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker, registry

from backend.entities.mesa import Mesa
from backend.entities.administrador import Administrador
from backend.entities.metodopago import MetodoPago

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "polirestaurante1")

if DB_PASSWORD is None:
    raise RuntimeError("DB_PASSWORD no está definida. Crea un archivo .env con las credenciales de la base de datos.")


# ---------- Conexion de tus compañeros (driver) ----------
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


# ---------- Conexion del CRUD Mesa / Administrador / MetodoPago (driver) ----------
def getConnection():
    conn = None
    try:
        conn = get_connection()
    except Exception:
        print("no se puede conectar a la base de datos")
        return None
    print("conectado")
    return conn


def closeConnection(conn):
    if conn:
        conn.close()


# ---------- ORM (SQLAlchemy) ----------
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def getSession():
    return SessionLocal()


metadata = MetaData()
mapper_registry = registry()

mesa_table = Table(
    "mesa", metadata,
    Column("id_mesa", Integer, primary_key=True, autoincrement=True),
    Column("numero", Integer),
    Column("estado", String(45)),
)

administrador_table = Table(
    "Administrador", metadata,
    Column("id_administrador", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(45)),
    Column("correo", String(45)),
    Column("usuario", String(45)),
    Column("contraseña", String(45), key="contrasena"),
    Column("telefono", String(20)),
)

metodopago_table = Table(
    "metodo_pago", metadata,
    Column("id_metodo_pago", Integer, primary_key=True, autoincrement=True),
    Column("efectivo", Integer),
    Column("aplicacion", String(45)),
    Column("tarjeta", String(45)),
    Column("descripcion", String(45)),
    Column("estado", Integer),
)

mapper_registry.map_imperatively(Mesa, mesa_table)
mapper_registry.map_imperatively(Administrador, administrador_table)
mapper_registry.map_imperatively(MetodoPago, metodopago_table)