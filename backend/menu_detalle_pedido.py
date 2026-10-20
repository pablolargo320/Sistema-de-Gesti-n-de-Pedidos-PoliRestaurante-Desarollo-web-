
from backend.dao.detalle_pedido_dao import DetallePedidoDAO
from backend.entities.detalle_pedido import DetallePedido


def menu_detalle_pedido():
    dao = DetallePedidoDAO()

    while True:
        print("\n===================================")
        print("       MENU DETALLE DE PEDIDO")
        print("===================================")
        print("1. Listar todos los detalles")
        print("2. Consultar detalle por ID")
        print("3. Crear detalle")
        print("4. Actualizar detalle")
        print("5. Eliminar detalle")
        print("0. Salir del menu")
        print("===================================")

        opcion = input("Seleccione una opcion: ").strip()

        try:
            if opcion == "1":
                detalles = dao.obtener_todos()

                if not detalles:
                    print("No hay detalles registrados.")
                else:
                    for detalle in detalles:
                        print(
                            f"ID: {detalle.id_detalle} | "
                            f"Cantidad: {detalle.cantidad} | "
                            f"Notas: {detalle.notas} | "
                            f"Subtotal: {detalle.subtotal} | "
                            f"Pedido: {detalle.id_pedido} | "
                            f"Producto: {detalle.id_producto}"
                        )

            elif opcion == "2":
                id_detalle = int(input("ID del detalle: "))
                detalle = dao.obtener_por_id(id_detalle)

                if detalle:
                    print(f"ID: {detalle.id_detalle}")
                    print(f"Cantidad: {detalle.cantidad}")
                    print(f"Notas: {detalle.notas}")
                    print(f"Subtotal: {detalle.subtotal}")
                    print(f"ID del pedido: {detalle.id_pedido}")
                    print(f"ID del producto: {detalle.id_producto}")
                else:
                    print("Detalle no encontrado.")

            elif opcion == "3":
                cantidad = int(input("Cantidad: "))
                notas = input("Notas: ").strip()
                subtotal = float(input("Subtotal: "))
                id_pedido = int(input("ID del pedido existente: "))
                id_producto = int(input("ID del producto existente: "))

                detalle = DetallePedido(
                    cantidad=cantidad,
                    notas=notas,
                    subtotal=subtotal,
                    id_pedido=id_pedido,
                    id_producto=id_producto
                )

                resultado = dao.crear(detalle)

                print(
                    "Detalle creado correctamente. "
                    f"ID asignado: {resultado.id_detalle}"
                )

            elif opcion == "4":
                id_detalle = int(
                    input("ID del detalle que desea actualizar: ")
                )

                existente = dao.obtener_por_id(id_detalle)

                if existente is None:
                    print("Detalle no encontrado.")
                    continue

                cantidad = int(input("Nueva cantidad: "))
                notas = input("Nuevas notas: ").strip()
                subtotal = float(input("Nuevo subtotal: "))
                id_pedido = int(input("Nuevo ID del pedido existente: "))
                id_producto = int(
                    input("Nuevo ID del producto existente: ")
                )

                actualizado = DetallePedido(
                    cantidad=cantidad,
                    notas=notas,
                    subtotal=subtotal,
                    id_pedido=id_pedido,
                    id_producto=id_producto
                )

                resultado = dao.actualizar(id_detalle, actualizado)

                if resultado:
                    print("Detalle actualizado correctamente.")
                else:
                    print("No se pudo actualizar el detalle.")

            elif opcion == "5":
                id_detalle = int(
                    input("ID del detalle que desea eliminar: ")
                )

                resultado = dao.eliminar(id_detalle)

                if resultado:
                    print("Detalle eliminado correctamente.")
                else:
                    print("Detalle no encontrado.")

            elif opcion == "0":
                print("Saliendo del menu de detalle de pedido...")
                break

            else:
                print("Opcion no valida. Intente nuevamente.")

        except ValueError:
            print("Error: ingrese un numero valido.")

        except Exception as error:
            print(f"Error al ejecutar la operacion: {error}")


if __name__ == "__main__":
    menu_detalle_pedido()