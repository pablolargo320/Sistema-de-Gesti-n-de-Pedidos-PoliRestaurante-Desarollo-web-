import os
from uuid import uuid4

from backend.app import create_app


def pausar(mensaje):
    if os.getenv("PAUSAR_TEST_DB") == "1":
        input(f"\n{mensaje}\nPresiona ENTER para continuar...")


def test_crud_pedido_rest():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    estado_inicial = f"Pendiente REST {uuid4().hex[:6]}"
    estado_actualizado = f"Preparando REST {uuid4().hex[:6]}"
    id_pedido = None

    try:
        # CREATE
        respuesta = client.post(
            "/api/pedidos",
            json={
                "estado": estado_inicial,
                "total": 12000,
                "tipo_pedido": "Prueba REST"
            }
        )

        assert respuesta.status_code == 201

        pedido = respuesta.get_json()
        id_pedido = pedido["id_pedido"]

        assert pedido["estado"] == estado_inicial
        assert float(pedido["total"]) == 12000.00

        print(f"\nPedido creado por REST. ID: {id_pedido}")
        pausar("Revisa en Workbench el pedido creado por REST.")

        # READ por ID
        respuesta = client.get(f"/api/pedidos/{id_pedido}")

        assert respuesta.status_code == 200
        assert respuesta.get_json()["estado"] == estado_inicial

        print("Pedido consultado por REST:", respuesta.get_json())
        pausar("Comprueba los datos consultados por REST.")

        # READ todos
        respuesta = client.get("/api/pedidos")

        assert respuesta.status_code == 200
        assert any(
            p["id_pedido"] == id_pedido
            for p in respuesta.get_json()
        )

        # UPDATE
        respuesta = client.put(
            f"/api/pedidos/{id_pedido}",
            json={
                "estado": estado_actualizado,
                "total": 22000
            }
        )

        assert respuesta.status_code == 200

        pedido = respuesta.get_json()
        assert pedido["estado"] == estado_actualizado
        assert float(pedido["total"]) == 22000.00

        print("Pedido actualizado por REST:", pedido)
        pausar("Revisa en Workbench los datos actualizados por REST.")

        # Confirmar persistencia
        respuesta = client.get(f"/api/pedidos/{id_pedido}")

        assert respuesta.status_code == 200
        assert respuesta.get_json()["estado"] == estado_actualizado

    finally:
        # Eliminar el pedido temporal aunque falle una aserción
        if id_pedido is not None:
            limpieza = client.delete(f"/api/pedidos/{id_pedido}")

            if limpieza.status_code != 200:
                print(
                    "Advertencia: no se pudo limpiar el pedido temporal:",
                    limpieza.get_json()
                )

    # Confirmar que ya no existe
    if id_pedido is not None:
        respuesta = client.get(f"/api/pedidos/{id_pedido}")
        assert respuesta.status_code == 404

        print(f"Pedido {id_pedido} eliminado por REST.")
        pausar("Comprueba que el pedido temporal ya no existe en Workbench.")


def test_validaciones_pedido_rest():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    # Cuerpo vacío
    respuesta = client.post("/api/pedidos", json={})
    assert respuesta.status_code == 201

    # Eliminar inmediatamente el registro creado para probar limpieza
    id_temporal = respuesta.get_json()["id_pedido"]
    client.delete(f"/api/pedidos/{id_temporal}")

    # Total no numérico
    respuesta = client.post(
        "/api/pedidos",
        json={
            "estado": "Pendiente",
            "total": "no es un número",
            "tipo_pedido": "Prueba"
        }
    )
    assert respuesta.status_code == 400

    # Campo desconocido
    respuesta = client.post(
        "/api/pedidos",
        json={"campo_inventado": "valor"}
    )
    assert respuesta.status_code == 400

    # Estado vacío
    respuesta = client.post(
        "/api/pedidos",
        json={"estado": " ", "total": 1000}
    )
    assert respuesta.status_code == 400

    # Pedido inexistente
    respuesta = client.get("/api/pedidos/999999999")
    assert respuesta.status_code == 404

    respuesta = client.put(
        "/api/pedidos/999999999",
        json={"estado": "Preparando"}
    )
    assert respuesta.status_code == 404

    respuesta = client.delete("/api/pedidos/999999999")
    assert respuesta.status_code == 404