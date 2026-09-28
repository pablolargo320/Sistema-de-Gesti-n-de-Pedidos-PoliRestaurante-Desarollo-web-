from dao.producto_dao import ProductoDAO
from entities.producto import Producto


dao = ProductoDAO()


def crear_producto():
    print("\n=== CREAR PRODUCTO ===")

    nombre = input("Nombre: ")
    descripcion = input("Descripción: ")
    precio = float(input("Precio: "))
    disponible = int(input("¿Está disponible? (1 = Sí, 0 = No): "))
    id_categoria = int(input("ID de categoría: "))

    producto = Producto(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        disponible=disponible,
        id_categoria=id_categoria
    )

    producto_creado = dao.crear(producto)

    print("\nProducto creado correctamente.")
    print(producto_creado.__dict__)


def buscar_producto():
    print("\n=== BUSCAR PRODUCTO ===")

    id_producto = int(input("Ingrese el ID del producto: "))

    producto = dao.obtener_por_id(id_producto)

    if producto:
        print("\nProducto encontrado:")
        print(producto)
    else:
        print("\nNo se encontró un producto con ese ID.")


def actualizar_producto():
    print("\n=== ACTUALIZAR PRODUCTO ===")

    id_producto = int(input("Ingrese el ID del producto que desea actualizar: "))

    producto_actual = dao.obtener_por_id(id_producto)

    if not producto_actual:
        print("\nNo se encontró un producto con ese ID.")
        return

    print("\nProducto actual:")
    print(producto_actual)

    print("\nIngrese los nuevos datos:")

    nombre = input("Nuevo nombre: ")
    descripcion = input("Nueva descripción: ")
    precio = float(input("Nuevo precio: "))
    disponible = int(input("¿Está disponible? (1 = Sí, 0 = No): "))
    id_categoria = int(input("Nuevo ID de categoría: "))

    producto = Producto(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        disponible=disponible,
        id_categoria=id_categoria
    )

    filas_actualizadas = dao.actualizar(
        id_producto,
        producto
    )

    if filas_actualizadas > 0:
        print("\nProducto actualizado correctamente.")
    else:
        print("\nNo se pudo actualizar el producto.")


def eliminar_producto():
    print("\n=== ELIMINAR PRODUCTO ===")

    id_producto = int(input("Ingrese el ID del producto que desea eliminar: "))

    producto = dao.obtener_por_id(id_producto)

    if not producto:
        print("\nNo se encontró un producto con ese ID.")
        return

    print("\nProducto que se va a eliminar:")
    print(producto)

    confirmacion = input(
        "\n¿Está seguro de eliminarlo? (s/n): "
    )

    if confirmacion.lower() == "s":

        filas_eliminadas = dao.eliminar(id_producto)

        if filas_eliminadas > 0:
            print("\nProducto eliminado correctamente.")
        else:
            print("\nNo se pudo eliminar el producto.")

    else:
        print("\nOperación cancelada.")


def obtener_todos():
    print("\n=== TODOS LOS PRODUCTOS ===")

    productos = dao.obtener_todos()

    if not productos:
        print("No hay productos registrados.")
        return

    for producto in productos:
        print(producto)


def mostrar_menu():

    while True:

        print("\n")
        print("================================")
        print("       CRUD DE PRODUCTOS")
        print("================================")
        print("1. Crear producto")
        print("2. Buscar producto por ID")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Ver todos los productos")
        print("0. Salir")
        print("================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_producto()

        elif opcion == "2":
            buscar_producto()

        elif opcion == "3":
            actualizar_producto()

        elif opcion == "4":
            eliminar_producto()

        elif opcion == "5":
            obtener_todos()

        elif opcion == "0":
            print("\nPrograma finalizado.")
            break

        else:
            print("\nOpción no válida. Intente nuevamente.")


mostrar_menu()