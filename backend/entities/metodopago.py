class MetodoPago:
    def __init__(self, id_metodo_pago=None, efectivo=None, aplicacion=None, tarjeta=None, descripcion=None, estado=None):
        self.id_metodo_pago = id_metodo_pago
        self.efectivo = efectivo
        self.aplicacion = aplicacion
        self.tarjeta = tarjeta
        self.descripcion = descripcion
        self.estado = estado

    def to_dict(self):
        return {
            "id_metodo_pago": self.id_metodo_pago,
            "efectivo": self.efectivo,
            "aplicacion": self.aplicacion,
            "tarjeta": self.tarjeta,
            "descripcion": self.descripcion,
            "estado": self.estado
        }
