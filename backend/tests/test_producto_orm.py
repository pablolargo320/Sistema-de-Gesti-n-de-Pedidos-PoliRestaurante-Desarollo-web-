
from backend.database.database import SessionLocal
from backend.entities.producto import Producto


def test_crud_producto_orm():
    db = SessionLocal()
    id_producto = None

    try:
        # CREATE
        producto = Producto(
            nombre="Producto ORM Prueba",
            descripcion="Creado mediante SQLAlchemy",
            precio=10000.00,
            disponible=1,
            id_categoria=1,
            Administrador_id_administrador=1,
        )

        db.add(producto)
        db.commit()
        db.refresh(producto)

        id_producto = producto.id_producto
        print(f"\nProducto ORM creado. ID: {id_producto}")

        input(
            "Consulta el producto creado en Workbench "
            "y pulsa ENTER para continuar..."
        )

        # READ
        producto = db.query(Producto).filter(
            Producto.id_producto == id_producto
        ).first()

        assert producto is not None
        assert producto.nombre == "Producto ORM Prueba"

        # UPDATE
        producto.nombre = "Producto ORM Actualizado"
        producto.precio = 15000.00

        db.commit()

        print("Producto ORM actualizado.")

        input(
            "Consulta el producto actualizado en Workbench "
            "y pulsa ENTER para continuar..."
        )

        # DELETE
        db.delete(producto)
        db.commit()

        id_producto = None

        print("Producto ORM eliminado.")

    finally:
        if id_producto is not None:
            try:
                producto = db.query(Producto).filter(
                    Producto.id_producto == id_producto
                ).first()

                if producto is not None:
                    db.delete(producto)
                    db.commit()
            except Exception:
                db.rollback()

        db.close()