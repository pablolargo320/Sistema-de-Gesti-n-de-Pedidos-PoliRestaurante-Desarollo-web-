from sqlalchemy import (
    Column, Integer, String, Date, DateTime,
    ForeignKey, func
)

from backend.database.database import Base


class SolicitudAbastecimiento(Base):

    __tablename__ = "solicitud_abastecimiento"

    id_solicitud = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    proveedor_id_proveedor = Column(
        Integer,
        ForeignKey("proveedor.id_proveedor"),
        nullable=False
    )

    producto_id_producto = Column(
        Integer,
        ForeignKey("producto.id_producto"),
        nullable=False
    )

    cantidad_solicitada = Column(
        Integer,
        nullable=False
    )

    fecha_solicitud = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp()
    )

    fecha_requerida = Column(
        Date,
        nullable=True
    )

    estado = Column(
        String(20),
        nullable=False,
        default="pendiente"
    )

    observaciones = Column(
        String(255),
        nullable=True
    )

    motivo_rechazo = Column(
        String(255),
        nullable=True
    )

    fecha_respuesta = Column(
        DateTime,
        nullable=True
    )