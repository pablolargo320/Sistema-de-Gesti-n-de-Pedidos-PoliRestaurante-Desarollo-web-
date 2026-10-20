from flask import Blueprint, request, jsonify

from backend.dao.categoria_dao import CategoriaDAO
from backend.entities.categoria import Categoria


categoria_routes = Blueprint(
    "categoria_routes",
    __name__
)

categoria_dao = CategoriaDAO()


@categoria_routes.route(
    "/api/categorias",
    methods=["GET"]
)
def obtener_categorias():

    categorias = categoria_dao.obtener_todas()

    resultado = []

    for categoria in categorias:
        resultado.append({
            "id_categoria": categoria.id_categoria,
            "nombre": categoria.nombre
        })

    return jsonify(resultado), 200


@categoria_routes.route(
    "/api/categorias/<int:id_categoria>",
    methods=["GET"]
)
def obtener_categoria(id_categoria):

    categoria = categoria_dao.obtener_por_id(id_categoria)

    if categoria is None:
        return jsonify({
            "mensaje": "Categoría no encontrada"
        }), 404

    return jsonify({
        "id_categoria": categoria.id_categoria,
        "nombre": categoria.nombre
    }), 200


@categoria_routes.route(
    "/api/categorias",
    methods=["POST"]
)
def crear_categoria():

    datos = request.get_json()

    categoria = Categoria(
        nombre=datos.get("nombre")
    )

    categoria_creada = categoria_dao.crear(categoria)

    return jsonify({
        "id_categoria": categoria_creada.id_categoria,
        "nombre": categoria_creada.nombre
    }), 201


@categoria_routes.route(
    "/api/categorias/<int:id_categoria>",
    methods=["PUT"]
)
def actualizar_categoria(id_categoria):

    datos = request.get_json()

    categoria = Categoria(
        nombre=datos.get("nombre")
    )

    filas_afectadas = categoria_dao.actualizar(
        id_categoria,
        categoria
    )

    if filas_afectadas == 0:
        return jsonify({
            "mensaje": "Categoría no encontrada"
        }), 404

    return jsonify({
        "mensaje": "Categoría actualizada correctamente"
    }), 200


@categoria_routes.route(
    "/api/categorias/<int:id_categoria>",
    methods=["DELETE"]
)
def eliminar_categoria(id_categoria):

    filas_afectadas = categoria_dao.eliminar(
        id_categoria
    )

    if filas_afectadas == 0:
        return jsonify({
            "mensaje": "Categoría no encontrada"
        }), 404

    return jsonify({
        "mensaje": "Categoría eliminada correctamente"
    }), 200