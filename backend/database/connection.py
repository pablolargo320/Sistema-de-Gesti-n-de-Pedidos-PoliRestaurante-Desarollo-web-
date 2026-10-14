import mysql.connector
from urllib.parse import quote_plus
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker, registry

from entities.mesa import Mesa
from entities.administrador import Administrador
from entities.metodopago import MetodoPago

DB_USER = "root"
DB_PASSWORD = "Woxfan#2026"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "polirestaurante1"


# ---------- Conexion estilo driver (mysql.connector), igual a PersonaDAO ----------
def getConnection():
    conn = None
    try:
        conn = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_NAME,
            port=DB_PORT
        )
    except Exception:
        print("no se puede conectar a la base de datos")
        return None
    print("conectado")
    return conn


def closeConnection(conn):
    if conn:
        conn.close()


# ---------- Misma base de datos, expuesta como ORM (SQLAlchemy) ----------
# La contraseña se codifica porque puede traer caracteres especiales (p.ej. '#')
# que romperían la URL de conexión si van tal cual.
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def getSession():
    return SessionLocal()


# Las entidades de entities/ se mapean directamente a sus tablas,
# sin crear clases de modelo separadas.
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
