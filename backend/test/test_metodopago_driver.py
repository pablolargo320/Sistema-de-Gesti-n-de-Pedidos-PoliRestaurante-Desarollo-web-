import unittest
from dao import metodopago_dao


class TestMetodoPagoDriver(unittest.TestCase):

    def test_crud_metodopago(self):
        nuevoId = metodopago_dao.crearMetodoPago(0, "Daviplata", None, "Pago por Daviplata", 1)
        self.assertIsNotNone(nuevoId)

        metodo = metodopago_dao.buscarMetodoPagoPorId(nuevoId)
        self.assertIsNotNone(metodo)
        self.assertEqual(metodo["aplicacion"], "Daviplata")

        filas = metodopago_dao.editarMetodoPago(nuevoId, 0, "Daviplata", None, "Daviplata editado", 0)
        self.assertEqual(filas, 1)

        metodo = metodopago_dao.buscarMetodoPagoPorId(nuevoId)
        self.assertEqual(metodo["descripcion"], "Daviplata editado")

        todos = metodopago_dao.findAll()
        self.assertTrue(any(m["id_metodo_pago"] == nuevoId for m in todos))

        filas = metodopago_dao.eliminarMetodoPago(nuevoId)
        self.assertEqual(filas, 1)

        metodo = metodopago_dao.buscarMetodoPagoPorId(nuevoId)
        self.assertIsNone(metodo)


if __name__ == "__main__":
    unittest.main()
