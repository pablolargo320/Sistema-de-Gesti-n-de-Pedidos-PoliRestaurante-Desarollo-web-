from sqlalchemy import Column, Integer, String, ForeignKey
from backend.database.database import Base
from backend.entities.producto import Producto


class Proveedor(Base):

    __tablename__ = "proveedor"

    id_proveedor = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre = Column(String(45))
    telefono = Column(String(20))
    correo = Column(String(45))
    direccion = Column(String(45))

    producto_id_producto = Column(
        Integer,
        ForeignKey("producto.id_producto")
    )