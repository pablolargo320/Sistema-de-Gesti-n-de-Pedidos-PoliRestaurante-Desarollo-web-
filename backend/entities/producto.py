
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from backend.database.database import Base


class Producto(Base):
    __tablename__ = "producto"

    id_producto = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre = Column(String(45))
    descripcion = Column(String(100))
    precio = Column(Numeric(10, 2))
    disponible = Column(Integer)

    id_categoria = Column(
        Integer,
        ForeignKey("categoria.id_categoria")
    )

    Administrador_id_administrador = Column(
        Integer,
        ForeignKey("Administrador.id_administrador")
    )
