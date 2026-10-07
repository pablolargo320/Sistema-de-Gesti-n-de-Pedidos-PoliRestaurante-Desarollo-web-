from sqlalchemy import Column, Integer, String
from backend.database.database import Base


class Administrador(Base):
    __tablename__ = "Administrador"

    id_administrador = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre = Column(String(45))
    correo = Column(String(45))
    usuario = Column(String(45))
    contraseña = Column(String(45))
    telefono = Column(String(20))