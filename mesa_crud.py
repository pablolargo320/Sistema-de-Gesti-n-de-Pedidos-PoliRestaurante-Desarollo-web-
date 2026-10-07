from backend.dao.mesa_dao import MesaDAO
from backend.entities.mesa import Mesa


dao = MesaDAO()


def crear_mesa():

    print("\n=== CREAR MESA ===")

    numero = int(input("Número de mesa: "))

    print("\nEstados disponibles:")
    print("Disponible(D)")
    print("Ocupada(O)")
    print("Reservada(R)")

    opcion = input("Seleccione el estado: ")

    estados = {
        "D": "Disponible",
        "O": "Ocupada",
        "R": "Reservada"
    }

    if opcion not in estados:
        print("Estado inválido.")
        return

    estado = estados[opcion]

    mesa = Mesa(
        numero=numero,
        estado=estado
    )

    mesa_creada = dao.crear(mesa)

    print("\nMesa creada correctamente.")
    print(mesa_creada)


def listar_mesas():

    print("\n=== TODAS LAS MESAS ===")

    mesas = dao.obtener_todos()

    if not mesas:
        print("No hay mesas registradas.")
        return

    for mesa in mesas:
        print(
            f"ID: {mesa['id_mesa']} | "
            f"Número: {mesa['numero']} | "
            f"Estado: {mesa['estado']}"
        )


def buscar_mesa():

    print("\n=== BUSCAR MESA ===")

    id_mesa = int(
        input("ID de la mesa: ")
    )

    mesa = dao.obtener_por_id(id_mesa)

    if mesa:
        print("\nMesa encontrada:")
        print(mesa)
    else:
        print("\nNo existe esa mesa.")


def mostrar_menu():

    while True:

        print("\n================================")
        print("          CRUD DE MESAS")
        print("================================")
        print("1. Crear mesa")
        print("2. Ver todas las mesas")
        print("3. Buscar mesa por ID")
        print("4. Actualizar mesa")
        print("5. Eliminar mesa")
        print("0. Salir")
        print("================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":

            crear_mesa()

        elif opcion == "2":

            listar_mesas()

        elif opcion == "3":

            buscar_mesa()

        elif opcion == "4":

            actualizar_mesa()

        elif opcion == "5":

            eliminar_mesa()

        elif opcion == "0":

            print("\nPrograma finalizado.")
            break

        else:

            print("\nOpción inválida.")


def actualizar_mesa():

    print("\n=== ACTUALIZAR MESA ===")

    id_mesa = int(
        input("Ingrese el ID de la mesa que desea actualizar: ")
    )

    mesa_actual = dao.obtener_por_id(id_mesa)

    if not mesa_actual:
        print("\nNo existe una mesa con ese ID.")
        return

    print("\nMesa actual:")
    print(
        f"ID: {mesa_actual['id_mesa']}\n"
        f"Número: {mesa_actual['numero']}\n"
        f"Estado: {mesa_actual['estado']}"
    )

    print("\nIngrese los nuevos datos:")

    nuevo_numero = int(
        input("Nuevo número de mesa: ")
    )

    print("\nEstados disponibles:")
    print("1. Disponible")
    print("2. Ocupada")
    print("3. Reservada")

    opcion = input("Seleccione el nuevo estado: ")

    estados = {
        "1": "Disponible",
        "2": "Ocupada",
        "3": "Reservada"
    }

    if opcion not in estados:
        print("\nEstado inválido.")
        return

    nuevo_estado = estados[opcion]

    mesa = Mesa(
        numero=nuevo_numero,
        estado=nuevo_estado,
        id_mesa=id_mesa
    )

    filas_actualizadas = dao.actualizar(
        id_mesa,
        mesa
    )

    if filas_actualizadas > 0:
        print("\nMesa actualizada correctamente.")
    else:
        print("\nNo se pudo actualizar la mesa.")


def eliminar_mesa():

    print("\n=== ELIMINAR MESA ===")

    id_mesa = int(
        input("Ingrese el ID de la mesa que desea eliminar: ")
    )

    mesa = dao.obtener_por_id(id_mesa)

    if not mesa:

        print("\nNo existe una mesa con ese ID.")
        return

    print("\nMesa que se va a eliminar:")

    print(
        f"ID: {mesa['id_mesa']}\n"
        f"Número: {mesa['numero']}\n"
        f"Estado: {mesa['estado']}"
    )

    confirmacion = input(
        "\n¿Está seguro de eliminar esta mesa? (s/n): "
    )

    if confirmacion.lower() != "s":

        print("\nOperación cancelada.")
        return

    filas_eliminadas = dao.eliminar(id_mesa)

    if filas_eliminadas > 0:

        print("\nMesa eliminada correctamente.")

    elif filas_eliminadas == -1:

        print(
            "\nNo se puede eliminar esta mesa "
            "porque tiene pedidos asociados."
        )

    else:

        print("\nNo se pudo eliminar la mesa.")


if __name__ == "__main__":
    mostrar_menu()
