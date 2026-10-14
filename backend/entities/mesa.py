class Mesa:
    def __init__(self, id_mesa=None, numero=None, estado=None):
        self.id_mesa = id_mesa
        self.numero = numero
        self.estado = estado

    def to_dict(self):
        return {
            "id_mesa": self.id_mesa,
            "numero": self.numero,
            "estado": self.estado
        }
