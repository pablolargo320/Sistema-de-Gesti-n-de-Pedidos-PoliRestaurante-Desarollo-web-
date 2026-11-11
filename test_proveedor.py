from proveedor import Proveedor
from proveedor_dao import ProveedorDAO


dao = ProveedorDAO()


def mostrar_proveedor(proveedor):

    print("\n----------------------------------------")
    print("        INFORMACIÓN DEL PROVEEDOR")
    print("----------------------------------------")

    print("ID:", proveedor["id_proveedor"])
    print("Nombre:", proveedor["nombre"])
    print("Teléfono:", proveedor["telefono"])
    print("Correo:", proveedor["correo"])
    print("Dirección:", proveedor["direccion"])
    print("ID producto:", proveedor["producto_id_producto"])

    print("----------------------------------------")


def crear_proveedor():

    print("\n=== CREAR PROVEEDOR ===")

    nombre = input("Nombre: ")
    telefono = input("Teléfono: ")
    correo = input("Correo: ")
    direccion = input("Dirección: ")

    try:
        producto_id = int(
            input("ID del producto relacionado: ")
        )

    except ValueError:

        print("\nEl ID del producto debe ser un número.")
        return

    proveedor = Proveedor(
        nombre=nombre,
        telefono=telefono,
        correo=correo,
        direccion=direccion,
        producto_id_producto=producto_id
    )

    try:

        proveedor_creado = dao.crear(proveedor)

        print("\nProveedor creado correctamente.")

        print("ID asignado:", proveedor_creado.id_proveedor)
        print("Nombre:", proveedor_creado.nombre)
        print("Producto:", proveedor_creado.producto_id_producto)

    except Exception as e:

        print("\nNo se pudo crear el proveedor.")
        print("Error:", e)


def obtener_todos():

    print("\n=== TODOS LOS PROVEEDORES ===")

    try:

        proveedores = dao.obtener_todos()

        if not proveedores:

            print("\nNo hay proveedores registrados.")
            return

        for proveedor in proveedores:

            mostrar_proveedor(proveedor)

        print("\nTotal de proveedores:", len(proveedores))

    except Exception as e:

        print("\nError al obtener proveedores.")
        print("Error:", e)


def buscar_por_id():

    print("\n=== BUSCAR PROVEEDOR POR ID ===")

    try:

        id_proveedor = int(
            input("Ingrese el ID del proveedor: ")
        )

    except ValueError:

        print("\nEl ID debe ser un número.")
        return

    try:

        proveedor = dao.obtener_por_id(id_proveedor)

        if proveedor:

            mostrar_proveedor(proveedor)

        else:

            print(
                "\nNo existe un proveedor con ese ID."
            )

    except Exception as e:

        print("\nError al buscar proveedor.")
        print("Error:", e)


def buscar_por_nombre():

    print("\n=== BUSCAR PROVEEDOR POR NOMBRE ===")

    nombre = input(
        "Ingrese el nombre o parte del nombre: "
    )

    try:

        proveedores = dao.obtener_por_nombre(nombre)

        if not proveedores:

            print(
                "\nNo se encontraron proveedores."
            )

            return

        for proveedor in proveedores:

            mostrar_proveedor(proveedor)

        print(
            "\nProveedores encontrados:",
            len(proveedores)
        )

    except Exception as e:

        print("\nError al buscar proveedores.")
        print("Error:", e)


def buscar_por_producto():

    print("\n=== BUSCAR PROVEEDORES POR PRODUCTO ===")

    try:

        id_producto = int(
            input("Ingrese el ID del producto: ")
        )

    except ValueError:

        print("\nEl ID debe ser un número.")
        return

    try:

        proveedores = dao.obtener_por_producto(
            id_producto
        )

        if not proveedores:

            print(
                "\nNo hay proveedores relacionados "
                "con ese producto."
            )

            return

        for proveedor in proveedores:

            mostrar_proveedor(proveedor)

        print(
            "\nProveedores encontrados:",
            len(proveedores)
        )

    except Exception as e:

        print("\nError al buscar proveedores.")
        print("Error:", e)


def actualizar_proveedor():

    print("\n=== ACTUALIZAR PROVEEDOR ===")

    try:

        id_proveedor = int(
            input("Ingrese el ID del proveedor: ")
        )

    except ValueError:

        print("\nEl ID debe ser un número.")
        return

    try:

        proveedor_actual = dao.obtener_por_id(
            id_proveedor
        )

        if not proveedor_actual:

            print(
                "\nNo existe un proveedor con ese ID."
            )

            return

        print("\nProveedor actual:")

        mostrar_proveedor(proveedor_actual)

        print("\nIngrese los nuevos datos.")

        nombre = input("Nuevo nombre: ")
        telefono = input("Nuevo teléfono: ")
        correo = input("Nuevo correo: ")
        direccion = input("Nueva dirección: ")

        try:

            producto_id = int(
                input(
                    "Nuevo ID del producto relacionado: "
                )
            )

        except ValueError:

            print(
                "\nEl ID del producto debe ser un número."
            )

            return

        proveedor = Proveedor(
            nombre=nombre,
            telefono=telefono,
            correo=correo,
            direccion=direccion,
            producto_id_producto=producto_id
        )

        filas_actualizadas = dao.actualizar(
            id_proveedor,
            proveedor
        )

        if filas_actualizadas > 0:

            print(
                "\nProveedor actualizado correctamente."
            )

        else:

            print(
                "\nNo se realizaron cambios."
            )

    except Exception as e:

        print("\nError al actualizar proveedor.")
        print("Error:", e)


def eliminar_proveedor():

    print("\n=== ELIMINAR PROVEEDOR ===")

    try:

        id_proveedor = int(
            input("Ingrese el ID del proveedor: ")
        )

    except ValueError:

        print("\nEl ID debe ser un número.")
        return

    try:

        proveedor = dao.obtener_por_id(
            id_proveedor
        )

        if not proveedor:

            print(
                "\nNo existe un proveedor con ese ID."
            )

            return

        print("\nProveedor que se va a eliminar:")

        mostrar_proveedor(proveedor)

        confirmacion = input(
            "\n¿Está seguro de eliminarlo? (s/n): "
        ).strip().lower()

        if confirmacion != "s":

            print("\nOperación cancelada.")
            return

        filas_eliminadas = dao.eliminar(
            id_proveedor
        )

        if filas_eliminadas > 0:

            print(
                "\nProveedor eliminado correctamente."
            )

        else:

            print(
                "\nNo se pudo eliminar el proveedor."
            )

    except Exception as e:

        print("\nNo se pudo eliminar el proveedor.")
        print("Error:", e)


def mostrar_menu():

    while True:

        print("\n")
        print("================================")
        print("       CRUD DE PROVEEDORES")
        print("================================")

        print("1. Crear proveedor")
        print("2. Ver todos los proveedores")
        print("3. Buscar proveedor por ID")
        print("4. Buscar por nombre")
        print("5. Buscar por producto")
        print("6. Actualizar proveedor")
        print("7. Eliminar proveedor")
        print("0. Salir")

        print("================================")

        opcion = input(
            "Seleccione una opción: "
        ).strip()

        if opcion == "1":

            crear_proveedor()

        elif opcion == "2":

            obtener_todos()

        elif opcion == "3":

            buscar_por_id()

        elif opcion == "4":

            buscar_por_nombre()

        elif opcion == "5":

            buscar_por_producto()

        elif opcion == "6":

            actualizar_proveedor()

        elif opcion == "7":

            eliminar_proveedor()

        elif opcion == "0":

            print("\nPrograma finalizado.")
            break

        else:

            print("\nOpción no válida.")


mostrar_menu()