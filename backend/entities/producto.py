from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from backend.database.database import Base


class Producto(Base):

    __tablename__ = "producto"

    id_producto = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre = Column(
        String(45),
        nullable=False
    )

    descripcion = Column(
        String(100),
        nullable=True
    )

    precio = Column(
        Numeric(10, 2),
        nullable=False
    )

    disponible = Column(
        Boolean,
        nullable=False
    )

    id_categoria = Column(
        Integer,
        ForeignKey("categoria.id_categoria"),
        nullable=False
    )

    Administrador_id_administrador = Column(
        Integer,
        ForeignKey("Administrador.id_administrador"),
        nullable=True
    )