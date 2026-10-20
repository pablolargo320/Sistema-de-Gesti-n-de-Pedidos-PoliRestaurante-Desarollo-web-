from backend.database.connection import getSession
from backend.entities.mesa import Mesa
from backend.entities.administrador import Administrador
from backend.entities.metodopago import MetodoPago


def menuMesa():
    while True:
        print("\n--- MESA (ORM) ---")
        print("1. Listar")
        print("2. Buscar por id")
        print("3. Crear")
        print("4. Editar")
        print("5. Eliminar")
        print("0. Volver")
        opcion = input("Seleccione una opcion: ")

        session = getSession()

        if opcion == "1":
            for m in session.query(Mesa).all():
                print(m.to_dict())

        elif opcion == "2":
            id_mesa = int(input("id_mesa: "))
            mesa = session.query(Mesa).filter(Mesa.id_mesa == id_mesa).first()
            print(mesa.to_dict() if mesa else None)

        elif opcion == "3":
            numero = int(input("numero: "))
            estado = input("estado: ")
            mesa = Mesa(numero=numero, estado=estado)
            session.add(mesa)
            session.commit()
            print("Mesa creada con id", mesa.id_mesa)

        elif opcion == "4":
            id_mesa = int(input("id_mesa: "))
            mesa = session.query(Mesa).filter(Mesa.id_mesa == id_mesa).first()
            if mesa:
                mesa.numero = int(input("numero: "))
                mesa.estado = input("estado: ")
                session.commit()
                print("Mesa actualizada")
            else:
                print("Mesa no encontrada")

        elif opcion == "5":
            id_mesa = int(input("id_mesa: "))
            mesa = session.query(Mesa).filter(Mesa.id_mesa == id_mesa).first()
            if mesa:
                session.delete(mesa)
                session.commit()
                print("Mesa eliminada")
            else:
                print("Mesa no encontrada")

        elif opcion == "0":
            session.close()
            break

        else:
            print("Opcion invalida")

        session.close()


def menuAdministrador():
    while True:
        print("\n--- ADMINISTRADOR (ORM) ---")
        print("1. Listar")
        print("2. Buscar por id")
        print("3. Crear")
        print("4. Editar")
        print("5. Eliminar")
        print("0. Volver")
        opcion = input("Seleccione una opcion: ")

        session = getSession()

        if opcion == "1":
            for a in session.query(Administrador).all():
                print(a.to_dict())

        elif opcion == "2":
            id_administrador = int(input("id_administrador: "))
            admin = session.query(Administrador).filter(Administrador.id_administrador == id_administrador).first()
            print(admin.to_dict() if admin else None)

        elif opcion == "3":
            nombre = input("nombre: ")
            correo = input("correo: ")
            usuario = input("usuario: ")
            contrasena = input("contrasena: ")
            telefono = input("telefono: ")
            admin = Administrador(nombre=nombre, correo=correo, usuario=usuario, contrasena=contrasena, telefono=telefono)
            session.add(admin)
            session.commit()
            print("Administrador creado con id", admin.id_administrador)

        elif opcion == "4":
            id_administrador = int(input("id_administrador: "))
            admin = session.query(Administrador).filter(Administrador.id_administrador == id_administrador).first()
            if admin:
                admin.nombre = input("nombre: ")
                admin.correo = input("correo: ")
                admin.usuario = input("usuario: ")
                admin.contrasena = input("contrasena: ")
                admin.telefono = input("telefono: ")
                session.commit()
                print("Administrador actualizado")
            else:
                print("Administrador no encontrado")

        elif opcion == "5":
            id_administrador = int(input("id_administrador: "))
            admin = session.query(Administrador).filter(Administrador.id_administrador == id_administrador).first()
            if admin:
                session.delete(admin)
                session.commit()
                print("Administrador eliminado")
            else:
                print("Administrador no encontrado")

        elif opcion == "0":
            session.close()
            break

        else:
            print("Opcion invalida")

        session.close()


def menuMetodoPago():
    while True:
        print("\n--- METODO DE PAGO (ORM) ---")
        print("1. Listar")
        print("2. Buscar por id")
        print("3. Crear")
        print("4. Editar")
        print("5. Eliminar")
        print("0. Volver")
        opcion = input("Seleccione una opcion: ")

        session = getSession()

        if opcion == "1":
            for m in session.query(MetodoPago).all():
                print(m.to_dict())

        elif opcion == "2":
            id_metodo_pago = int(input("id_metodo_pago: "))
            metodo = session.query(MetodoPago).filter(MetodoPago.id_metodo_pago == id_metodo_pago).first()
            print(metodo.to_dict() if metodo else None)

        elif opcion == "3":
            efectivo = int(input("efectivo (1 o 0): "))
            aplicacion = input("aplicacion (enter para dejar vacio): ") or None
            tarjeta = input("tarjeta (enter para dejar vacio): ") or None
            descripcion = input("descripcion: ")
            estado = int(input("estado (1 o 0): "))
            metodo = MetodoPago(efectivo=efectivo, aplicacion=aplicacion, tarjeta=tarjeta, descripcion=descripcion, estado=estado)
            session.add(metodo)
            session.commit()
            print("Metodo de pago creado con id", metodo.id_metodo_pago)

        elif opcion == "4":
            id_metodo_pago = int(input("id_metodo_pago: "))
            metodo = session.query(MetodoPago).filter(MetodoPago.id_metodo_pago == id_metodo_pago).first()
            if metodo:
                metodo.efectivo = int(input("efectivo (1 o 0): "))
                metodo.aplicacion = input("aplicacion (enter para dejar vacio): ") or None
                metodo.tarjeta = input("tarjeta (enter para dejar vacio): ") or None
                metodo.descripcion = input("descripcion: ")
                metodo.estado = int(input("estado (1 o 0): "))
                session.commit()
                print("Metodo de pago actualizado")
            else:
                print("Metodo de pago no encontrado")

        elif opcion == "5":
            id_metodo_pago = int(input("id_metodo_pago: "))
            metodo = session.query(MetodoPago).filter(MetodoPago.id_metodo_pago == id_metodo_pago).first()
            if metodo:
                session.delete(metodo)
                session.commit()
                print("Metodo de pago eliminado")
            else:
                print("Metodo de pago no encontrado")

        elif opcion == "0":
            session.close()
            break

        else:
            print("Opcion invalida")

        session.close()


def main():
    while True:
        print("\n==== MENU CRUD - ORM (SQLAlchemy) ====")
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