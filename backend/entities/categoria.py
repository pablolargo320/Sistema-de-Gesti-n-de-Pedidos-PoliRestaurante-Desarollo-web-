from sqlalchemy import Column, Integer, String
from backend.database.database import Base


class Categoria(Base):
    __tablename__ = "categoria"

    id_categoria = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre = Column(String(45))