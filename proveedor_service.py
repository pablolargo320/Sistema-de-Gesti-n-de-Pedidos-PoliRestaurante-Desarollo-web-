class ProveedorService:

    def _init_(self, proveedor_dao):

        self.proveedor_dao = proveedor_dao

    def crear_proveedor(self, proveedor):

        return self.proveedor_dao.crear(proveedor)

    def obtener_proveedores(self):

        return self.proveedor_dao.obtener_todos()

    def obtener_proveedor(self, id_proveedor):

        return self.proveedor_dao.obtener_por_id(
            id_proveedor
        )

    def buscar_por_nombre(self, nombre):

        return self.proveedor_dao.obtener_por_nombre(
            nombre
        )

    def buscar_por_producto(self, id_producto):

        return self.proveedor_dao.obtener_por_producto(
            id_producto
        )

    def actualizar_proveedor(
        self,
        id_proveedor,
        proveedor
    ):

        return self.proveedor_dao.actualizar(
            id_proveedor,
            proveedor
        )

    def eliminar_proveedor(self, id_proveedor):

        return self.proveedor_dao.eliminar(
            id_proveedor
        )