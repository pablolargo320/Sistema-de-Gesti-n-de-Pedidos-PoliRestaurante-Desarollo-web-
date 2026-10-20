from sqlalchemy import text

from backend.database.database import engine
from backend.entities.producto import Producto


def test_conexion_orm():

    with engine.connect() as connection:

        resultado = connection.execute(
            text("SELECT 1")
        )

        assert resultado.scalar() == 1


def test_modelo_producto():

    assert Producto.__tablename__ == "producto"

    assert Producto.id_producto is not None
    assert Producto.nombre is not None
    assert Producto.descripcion is not None
    assert Producto.precio is not None
    assert Producto.disponible is not None