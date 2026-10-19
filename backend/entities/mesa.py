from sqlalchemy import Column, Integer, String
from backend.database.database import Base


class Mesa(Base):
    __tablename__ = "mesa"

    id_mesa = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer)
    estado = Column(String(45))
class Mesa:

    def __init__(
        self,
        numero,
        estado,
        id_mesa=None
    ):
        self.id_mesa = id_mesa
        self.numero = numero
        self.estado = estado

    def __repr__(self):
        return (
            f"Mesa("
            f"id_mesa={self.id_mesa}, "
            f"numero={self.numero}, "
            f"estado='{self.estado}'"
            f")"
        )
