from sqlalchemy import Column, Integer, String
from backend.database.database import Base


class Domiciliario(Base):

    __tablename__ = "domiciliario"

    id_domiciliario = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre = Column(String(45))
    apellido = Column(String(45))
    telefono = Column(String(20))
    correo = Column(String(45))
    direccion = Column(String(45))
    estado = Column(String(45))
    tipo_vehiculo = Column(String(45))
    placa_vehiculo = Column(String(45))