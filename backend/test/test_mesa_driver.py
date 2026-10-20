import unittest
from backend.dao import mesa_dao


class TestMesaDriver(unittest.TestCase):

    def test_crud_mesa(self):
        nuevoId = mesa_dao.crearMesa(99, "Disponible")
        self.assertIsNotNone(nuevoId)

        mesa = mesa_dao.buscarMesaPorId(nuevoId)
        self.assertIsNotNone(mesa)
        self.assertEqual(mesa["numero"], 99)
        self.assertEqual(mesa["estado"], "Disponible")

        filas = mesa_dao.editarMesa(nuevoId, 99, "Ocupada")
        self.assertEqual(filas, 1)

        mesa = mesa_dao.buscarMesaPorId(nuevoId)
        self.assertEqual(mesa["estado"], "Ocupada")

        todas = mesa_dao.findAll()
        self.assertTrue(any(m["id_mesa"] == nuevoId for m in todas))

        filas = mesa_dao.eliminarMesa(nuevoId)
        self.assertEqual(filas, 1)

        mesa = mesa_dao.buscarMesaPorId(nuevoId)
        self.assertIsNone(mesa)


if __name__ == "__main__":
    unittest.main()
