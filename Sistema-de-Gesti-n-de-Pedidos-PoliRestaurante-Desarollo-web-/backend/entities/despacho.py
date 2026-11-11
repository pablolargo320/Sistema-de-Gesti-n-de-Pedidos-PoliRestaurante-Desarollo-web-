from sqlalchemy import (
    Column, Integer, String, Date,
    DateTime, ForeignKey, func
)

from backend.database.database import Base


class Despacho(Base):

    __tablename__ = "despacho"

    id_despacho = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    solicitud_id_solicitud = Column(
        Integer,
        ForeignKey("solicitud_abastecimiento.id_solicitud"),
        nullable=False
    )

    cantidad_despachada = Column(
        Integer,
        nullable=False
    )

    fecha_despacho = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp()
    )

    fecha_entrega_estimada = Column(
        Date,
        nullable=True
    )

    fecha_entrega_real = Column(
        DateTime,
        nullable=True
    )

    numero_guia = Column(
        String(60),
        nullable=True
    )

    transportadora = Column(
        String(80),
        nullable=True
    )

    estado = Column(
        String(20),
        nullable=False,
        default="preparando"
    )

    observaciones = Column(
        String(255),
        nullable=True
    )