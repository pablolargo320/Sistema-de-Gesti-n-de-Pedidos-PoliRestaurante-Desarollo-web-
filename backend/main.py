from backend import menu_driver
from backend import menu_orm
def mostrarBienvenida():
    print("=" * 50)
    print("  SISTEMA DE GESTION - POLIRESTAURANTE")
    print("  CRUD de Mesa, Administrador y MetodoPago")
    print("=" * 50)


def menuPrincipal():
    mostrarBienvenida()

    while True:
        print("\n==== METODO DE ACCESO A DATOS ====")
        print("1. Driver (mysql.connector)")
        print("2. ORM (SQLAlchemy)")
        print("0. Salir")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            menu_driver.main()
        elif opcion == "2":
            menu_orm.main()
        elif opcion == "0":
            print("Hasta luego")
            break
        else:
            print("Opcion invalida, intente de nuevo")


if __name__ == "__main__":
    menuPrincipal()
