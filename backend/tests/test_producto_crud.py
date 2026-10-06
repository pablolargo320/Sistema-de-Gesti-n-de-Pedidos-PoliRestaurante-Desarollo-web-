from backend.database.database import SessionLocal
from backend.entities.producto import Producto


def test_crud_producto():

    db = SessionLocal()

    try:


        producto = Producto(
            nombre="Producto de prueba",
            descripcion="Producto creado desde SQLAlchemy",
            precio=10000.00,
            disponible=True,
            id_categoria=1,
            Administrador_id_administrador=1
        )

        db.add(producto)
        db.commit()
        db.refresh(producto)

        assert producto.id_producto is not None

        id_producto = producto.id_producto

        print(
            f"\nProducto creado con ID: {id_producto}"
        )

        
        producto_consultado = db.query(
            Producto
        ).filter(
            Producto.id_producto == id_producto
        ).first()

        assert producto_consultado is not None
        assert producto_consultado.nombre == "Producto de prueba"

        print("Producto consultado correctamente")

        
        producto_consultado.nombre = "Producto actualizado"
        producto_consultado.precio = 15000.00

        db.commit()
        db.refresh(producto_consultado)

        assert producto_consultado.nombre == "Producto actualizado"
        assert float(producto_consultado.precio) == 15000.00

        print("Producto actualizado correctamente")



        db.delete(producto_consultado)
        db.commit()

        producto_eliminado = db.query(
            Producto
        ).filter(
            Producto.id_producto == id_producto
        ).first()

        assert producto_eliminado is None

        print("Producto eliminado correctamente")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()