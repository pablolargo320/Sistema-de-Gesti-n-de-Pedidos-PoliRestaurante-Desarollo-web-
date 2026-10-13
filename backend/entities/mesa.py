from sqlalchemy import Column, Integer, String
from backend.database.database import Base


class Mesa(Base):
    __tablename__ = "mesa"

    id_mesa = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer)
    estado = Column(String(45))