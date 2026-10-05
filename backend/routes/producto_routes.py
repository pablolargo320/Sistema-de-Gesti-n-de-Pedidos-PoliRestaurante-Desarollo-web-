from flask import Blueprint, request, jsonify

from backend.dao.producto_dao import ProductoDAO
from backend.entities.producto import Producto


producto_routes = Blueprint(
    "producto_routes",
    __name__
)

producto_dao = ProductoDAO()


@producto_routes.route("/api/productos", methods=["GET"])
def obtener_productos():
    productos = producto_dao.obtener_todos()

    resultado = []

    for producto in productos:
        resultado.append({
            "id_producto": producto.id_producto,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": (
                float(producto.precio)
                if producto.precio is not None
                else None
            ),
            "disponible": producto.disponible,
            "id_categoria": producto.id_categoria,
            "Administrador_id_administrador": (
                producto.Administrador_id_administrador
            )
        })

    return jsonify(resultado), 200


@producto_routes.route(
    "/api/productos/<int:id_producto>",
    methods=["GET"]
)
def obtener_producto(id_producto):
    producto = producto_dao.obtener_por_id(id_producto)

    if producto is None:
        return jsonify({
            "mensaje": "Producto no encontrado"
        }), 404

    resultado = {
        "id_producto": producto.id_producto,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "precio": (
            float(producto.precio)
            if producto.precio is not None
            else None
        ),
        "disponible": producto.disponible,
        "id_categoria": producto.id_categoria,
        "Administrador_id_administrador": (
            producto.Administrador_id_administrador
        )
    }

    return jsonify(resultado), 200


@producto_routes.route("/api/productos", methods=["POST"])
def crear_producto():
    datos = request.get_json()

    if not datos:
        return jsonify({
            "mensaje": "Debe enviar información del producto"
        }), 400

    campos_obligatorios = [
        "nombre",
        "precio",
        "disponible",
        "id_categoria"
    ]

    for campo in campos_obligatorios:
        if campo not in datos:
            return jsonify({
                "mensaje": f"Falta el campo: {campo}"
            }), 400

    producto = Producto(
        nombre=datos["nombre"],
        descripcion=datos.get("descripcion"),
        precio=datos["precio"],
        disponible=datos["disponible"],
        id_categoria=datos["id_categoria"],
        Administrador_id_administrador=(
            datos.get("Administrador_id_administrador")
        )
    )

    try:
        producto_creado = producto_dao.crear(producto)

        return jsonify({
            "id_producto": producto_creado.id_producto,
            "nombre": producto_creado.nombre,
            "descripcion": producto_creado.descripcion,
            "precio": float(producto_creado.precio),
            "disponible": producto_creado.disponible,
            "id_categoria": producto_creado.id_categoria,
            "Administrador_id_administrador": (
                producto_creado.Administrador_id_administrador
            )
        }), 201

    except Exception:
        return jsonify({
            "mensaje": "No fue posible crear el producto"
        }), 500


@producto_routes.route(
    "/api/productos/<int:id_producto>",
    methods=["PUT"]
)
def actualizar_producto(id_producto):
    datos = request.get_json()

    if not datos:
        return jsonify({
            "mensaje": "Debe enviar información"
        }), 400

    campos_obligatorios = [
        "nombre",
        "precio",
        "disponible",
        "id_categoria"
    ]

    for campo in campos_obligatorios:
        if campo not in datos:
            return jsonify({
                "mensaje": f"Falta el campo: {campo}"
            }), 400

    try:
        producto = producto_dao.actualizar(
            id_producto,
            datos
        )

        if producto is None:
            return jsonify({
                "mensaje": "Producto no encontrado"
            }), 404

        return jsonify({
            "mensaje": "Producto actualizado correctamente",
            "producto": {
                "id_producto": producto.id_producto,
                "nombre": producto.nombre,
                "descripcion": producto.descripcion,
                "precio": float(producto.precio),
                "disponible": producto.disponible,
                "id_categoria": producto.id_categoria,
                "Administrador_id_administrador": (
                    producto.Administrador_id_administrador
                )
            }
        }), 200

    except Exception:
        return jsonify({
            "mensaje": "No fue posible actualizar el producto"
        }), 500


@producto_routes.route(
    "/api/productos/<int:id_producto>",
    methods=["DELETE"]
)
def eliminar_producto(id_producto):
    try:
        eliminado = producto_dao.eliminar(id_producto)

        if not eliminado:
            return jsonify({
                "mensaje": "Producto no encontrado"
            }), 404

        return jsonify({
            "mensaje": "Producto eliminado correctamente"
        }), 200

    except Exception:
        return jsonify({
            "mensaje": "No fue posible eliminar el producto"
        }), 500
