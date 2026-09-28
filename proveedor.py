class Proveedor:

    def _init_(
        self,
        nombre,
        telefono,
        correo,
        direccion,
        producto_id_producto,
        id_proveedor=None
    ):

        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.producto_id_producto = producto_id_producto

    def _repr_(self):

        return (
            f"Proveedor("
            f"id_proveedor={self.id_proveedor}, "
            f"nombre='{self.nombre}', "
            f"telefono='{self.telefono}', "
            f"correo='{self.correo}', "
            f"direccion='{self.direccion}', "
            f"producto_id_producto={self.producto_id_producto}"
            f")"
        )