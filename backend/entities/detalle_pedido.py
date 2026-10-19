
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from backend.database.database import Base


class DetallePedido(Base):
    __tablename__ = "detalle_pedido"

    id_detalle = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    cantidad = Column(Integer)
    notas = Column(String(100))
    subtotal = Column(Numeric(10, 2))

    id_pedido = Column(
        Integer,
        ForeignKey("pedido.id_pedido")
    )

    id_producto = Column(
        Integer,
        ForeignKey("producto.id_producto")
    )