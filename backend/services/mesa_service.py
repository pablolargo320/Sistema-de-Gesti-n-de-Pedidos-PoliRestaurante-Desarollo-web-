class MesaService:

    def __init__(self, mesa_dao):
        self.mesa_dao = mesa_dao

    def crear_mesa(self, mesa):

        return self.mesa_dao.crear(mesa)

    def obtener_mesas(self):

        return self.mesa_dao.obtener_todos()

    def obtener_mesa(self, id_mesa):

        return self.mesa_dao.obtener_por_id(id_mesa)

    def obtener_mesa_por_numero(self, numero):

        return self.mesa_dao.obtener_por_numero(numero)

    def actualizar_mesa(self, id_mesa, mesa):

        return self.mesa_dao.actualizar(
            id_mesa,
            mesa
        )

    def cambiar_estado(self, id_mesa, estado):

        return self.mesa_dao.cambiar_estado(
            id_mesa,
            estado
        )

    def eliminar_mesa(self, id_mesa):

        return self.mesa_dao.eliminar(id_mesa)

    def obtener_mesas_por_estado(self, estado):

        return self.mesa_dao.obtener_por_estado(estado)
