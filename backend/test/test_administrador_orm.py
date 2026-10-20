import unittest
from backend.dao import administrador_dao_orm


class TestAdministradorOrm(unittest.TestCase):

    def test_crud_administrador(self):
        nuevoId = administrador_dao_orm.crearAdministrador(
            "Test ORM", "testorm@polirestaurante.com", "testorm", "12345", "3000000002"
        )
        self.assertIsNotNone(nuevoId)

        admin = administrador_dao_orm.buscarAdministradorPorId(nuevoId)
        self.assertIsNotNone(admin)
        self.assertEqual(admin["nombre"], "Test ORM")

        filas = administrador_dao_orm.editarAdministrador(
            nuevoId, "Test ORM Editado", "testorm@polirestaurante.com",
            "testorm", "54321", "3000000002"
        )
        self.assertEqual(filas, 1)

        admin = administrador_dao_orm.buscarAdministradorPorId(nuevoId)
        self.assertEqual(admin["nombre"], "Test ORM Editado")

        todos = administrador_dao_orm.findAll()
        self.assertTrue(any(a["id_administrador"] == nuevoId for a in todos))

        filas = administrador_dao_orm.eliminarAdministrador(nuevoId)
        self.assertEqual(filas, 1)

        admin = administrador_dao_orm.buscarAdministradorPorId(nuevoId)
        self.assertIsNone(admin)


if __name__ == "__main__":
    unittest.main()
