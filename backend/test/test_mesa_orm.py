import unittest
from database.connection import getSession
from entities.mesa import Mesa


class TestMesaOrm(unittest.TestCase):

    def test_crud_mesa(self):
        session = getSession()

        # Crear
        mesa = Mesa(numero=98, estado="Disponible")
        session.add(mesa)
        session.commit()
        nuevoId = mesa.id_mesa
        self.assertIsNotNone(nuevoId)

        # Leer
        mesaConsultada = session.query(Mesa).filter(Mesa.id_mesa == nuevoId).first()
        self.assertIsNotNone(mesaConsultada)
        self.assertEqual(mesaConsultada.numero, 98)
        self.assertEqual(mesaConsultada.estado, "Disponible")

        # Actualizar
        mesaConsultada.estado = "Ocupada"
        session.commit()

        mesaActualizada = session.query(Mesa).filter(Mesa.id_mesa == nuevoId).first()
        self.assertEqual(mesaActualizada.estado, "Ocupada")

        # Listar
        todas = session.query(Mesa).all()
        self.assertTrue(any(m.id_mesa == nuevoId for m in todas))

        # Eliminar
        session.delete(mesaActualizada)
        session.commit()

        mesaEliminada = session.query(Mesa).filter(Mesa.id_mesa == nuevoId).first()
        self.assertIsNone(mesaEliminada)

        session.close()


if __name__ == "__main__":
    unittest.main()