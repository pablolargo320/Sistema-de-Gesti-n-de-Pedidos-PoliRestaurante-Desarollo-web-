from sqlalchemy import Column, Integer, String
from backend.database.database import Base


class Cliente(Base):
    __tablename__ = "Cliente"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(45))
    telefono = Column(String(20))
    correo = Column(String(45))
    direccion = Column(String(45))