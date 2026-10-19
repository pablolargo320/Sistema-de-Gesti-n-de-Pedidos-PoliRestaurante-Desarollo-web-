
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "PoliRestaurante1")

DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


def registrar_modelos():
    from backend.entities.administrador import Administrador
    from backend.entities.cliente import Cliente
    from backend.entities.domiciliario import Domiciliario
    from backend.entities.mesa import Mesa
    from backend.entities.metodo_pago import MetodoPago
    from backend.entities.pedido import Pedido
    from backend.entities.producto import Producto
    from backend.entities.detalle_pedido import DetallePedido
    from backend.entities.categoria import Categoria
