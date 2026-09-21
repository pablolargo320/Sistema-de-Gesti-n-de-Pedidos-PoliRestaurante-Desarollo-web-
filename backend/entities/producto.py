class Producto:

    def __init__(
        self,
        id_producto=None,
        nombre=None,
        descripcion=None,
        precio=None,
        disponible=None,
        id_categoria=None
    ):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.disponible = disponible
        self.id_categoria = id_categoria