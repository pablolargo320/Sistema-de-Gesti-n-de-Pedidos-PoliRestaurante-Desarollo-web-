from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from backend.database.database import Base


class Pedido(Base):
    __tablename__ = "pedido"

    id_pedido = Column(Integer, primary_key=True, autoincrement=True)

    fecha_creacion = Column(DateTime)
    estado = Column(String(45))
    total = Column(Numeric(10, 2))
    tipo_pedido = Column(String(45))

    id_mesa = Column(
        Integer,
        ForeignKey("mesa.id_mesa"),
        nullable=True
    )

    id_cliente = Column(
        Integer,
        ForeignKey("Cliente.id_cliente"),
        nullable=True
    )

    Administrador_id_administrador = Column(
        Integer,
        ForeignKey("Administrador.id_administrador"),
        nullable=True
    )

    metodo_pago_id_metodo_pago = Column(
        Integer,
        ForeignKey("metodo_pago.id_metodo_pago"),
        nullable=True
    )

    domiciliario_id_domiciliario = Column(
        Integer,
        ForeignKey("domiciliario.id_domiciliario"),
        nullable=True
    )