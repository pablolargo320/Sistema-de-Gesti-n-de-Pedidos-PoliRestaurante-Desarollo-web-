import unittest
from backend.dao import administrador_dao


class TestAdministradorDriver(unittest.TestCase):

    def test_crud_administrador(self):
        nuevoId = administrador_dao.crearAdministrador(
            "Test Driver", "testdriver@polirestaurante.com", "testdriver", "12345", "3000000001"
        )
        self.assertIsNotNone(nuevoId)

        admin = administrador_dao.buscarAdministradorPorId(nuevoId)
        self.assertIsNotNone(admin)
        self.assertEqual(admin["nombre"], "Test Driver")

        filas = administrador_dao.editarAdministrador(
            nuevoId, "Test Driver Editado", "testdriver@polirestaurante.com",
            "testdriver", "54321", "3000000001"
        )
        self.assertEqual(filas, 1)

        admin = administrador_dao.buscarAdministradorPorId(nuevoId)
        self.assertEqual(admin["nombre"], "Test Driver Editado")

        todos = administrador_dao.findAll()
        self.assertTrue(any(a["id_administrador"] == nuevoId for a in todos))

        filas = administrador_dao.eliminarAdministrador(nuevoId)
        self.assertEqual(filas, 1)

        admin = administrador_dao.buscarAdministradorPorId(nuevoId)
        self.assertIsNone(admin)


if __name__ == "__main__":
    unittest.main()
