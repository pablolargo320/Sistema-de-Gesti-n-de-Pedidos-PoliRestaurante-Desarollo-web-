from dao import mesa_dao, administrador_dao, metodopago_dao


def menuMesa():
    while True:
        print("\n--- MESA (DRIVER) ---")
        print("1. Listar")
        print("2. Buscar por id")
        print("3. Crear")
        print("4. Editar")
        print("5. Eliminar")
        print("0. Volver")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            for m in mesa_dao.findAll():
                print(m)

        elif opcion == "2":
            id_mesa = int(input("id_mesa: "))
            print(mesa_dao.buscarMesaPorId(id_mesa))

        elif opcion == "3":
            numero = int(input("numero: "))
            estado = input("estado: ")
            nuevoId = mesa_dao.crearMesa(numero, estado)
            print("Mesa creada con id", nuevoId)

        elif opcion == "4":
            id_mesa = int(input("id_mesa: "))
            numero = int(input("numero: "))
            estado = input("estado: ")
            filas = mesa_dao.editarMesa(id_mesa, numero, estado)
            print("Mesa actualizada" if filas else "Mesa no encontrada")

        elif opcion == "5":
            id_mesa = int(input("id_mesa: "))
            filas = mesa_dao.eliminarMesa(id_mesa)
            print("Mesa eliminada" if filas else "Mesa no encontrada")

        elif opcion == "0":
            break

        else:
            print("Opcion invalida")


def menuAdministrador():
    while True:
        print("\n--- ADMINISTRADOR (DRIVER) ---")
        print("1. Listar")
        print("2. Buscar por id")
        print("3. Crear")
        print("4. Editar")
        print("5. Eliminar")
        print("0. Volver")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            for a in administrador_dao.findAll():
                print(a)

        elif opcion == "2":
            id_administrador = int(input("id_administrador: "))
            print(administrador_dao.buscarAdministradorPorId(id_administrador))

        elif opcion == "3":
            nombre = input("nombre: ")
            correo = input("correo: ")
            usuario = input("usuario: ")
            contrasena = input("contrasena: ")
            telefono = input("telefono: ")
            nuevoId = administrador_dao.crearAdministrador(nombre, correo, usuario, contrasena, telefono)
            print("Administrador creado con id", nuevoId)

        elif opcion == "4":
            id_administrador = int(input("id_administrador: "))
            nombre = input("nombre: ")
            correo = input("correo: ")
            usuario = input("usuario: ")
            contrasena = input("contrasena: ")
            telefono = input("telefono: ")
            filas = administrador_dao.editarAdministrador(id_administrador, nombre, correo, usuario, contrasena, telefono)
            print("Administrador actualizado" if filas else "Administrador no encontrado")

        elif opcion == "5":
            id_administrador = int(input("id_administrador: "))
            filas = administrador_dao.eliminarAdministrador(id_administrador)
            print("Administrador eliminado" if filas else "Administrador no encontrado")

        elif opcion == "0":
            break

        else:
            print("Opcion invalida")


def menuMetodoPago():
    while True:
        print("\n--- METODO DE PAGO (DRIVER) ---")
        print("1. Listar")
        print("2. Buscar por id")
        print("3. Crear")
        print("4. Editar")
        print("5. Eliminar")
        print("0. Volver")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            for m in metodopago_dao.findAll():
                print(m)

        elif opcion == "2":
            id_metodo_pago = int(input("id_metodo_pago: "))
            print(metodopago_dao.buscarMetodoPagoPorId(id_metodo_pago))

        elif opcion == "3":
            efectivo = int(input("efectivo (1 o 0): "))
            aplicacion = input("aplicacion (enter para dejar vacio): ") or None
            tarjeta = input("tarjeta (enter para dejar vacio): ") or None
            descripcion = input("descripcion: ")
            estado = int(input("estado (1 o 0): "))
            nuevoId = metodopago_dao.crearMetodoPago(efectivo, aplicacion, tarjeta, descripcion, estado)
            print("Metodo de pago creado con id", nuevoId)

        elif opcion == "4":
            id_metodo_pago = int(input("id_metodo_pago: "))
            efectivo = int(input("efectivo (1 o 0): "))
            aplicacion = input("aplicacion (enter para dejar vacio): ") or None
            tarjeta = input("tarjeta (enter para dejar vacio): ") or None
            descripcion = input("descripcion: ")
            estado = int(input("estado (1 o 0): "))
            filas = metodopago_dao.editarMetodoPago(id_metodo_pago, efectivo, aplicacion, tarjeta, descripcion, estado)
            print("Metodo de pago actualizado" if filas else "Metodo de pago no encontrado")

        elif opcion == "5":
            id_metodo_pago = int(input("id_metodo_pago: "))
            filas = metodopago_dao.eliminarMetodoPago(id_metodo_pago)
            print("Metodo de pago eliminado" if filas else "Metodo de pago no encontrado")

        elif opcion == "0":
            break

        else:
            print("Opcion invalida")


def main():
    while True:
        print("\n==== MENU CRUD - DRIVER (mysql.connector) ====")
        print("1. Mesa")
        print("2. Administrador")
        print("3. MetodoPago")
        print("0. Salir")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            menuMesa()
        elif opcion == "2":
            menuAdministrador()
        elif opcion == "3":
            menuMetodoPago()
        elif opcion == "0":
            print("Hasta luego")
            break
        else:
            print("Opcion invalida")


if __name__ == "__main__":
    main()