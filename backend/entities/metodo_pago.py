from sqlalchemy import Column, Integer, String
from backend.database.database import Base


class MetodoPago(Base):
    __tablename__ = "metodo_pago"

    id_metodo_pago = Column(Integer, primary_key=True, autoincrement=True)
    efectivo = Column(Integer)
    aplicacion = Column(String(45))
    tarjeta = Column(String(45))
    descripcion = Column(String(45))
    estado = Column(Integer)