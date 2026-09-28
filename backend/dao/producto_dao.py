from database.connection import get_connection


class ProductoDAO:

    def crear(self, producto):
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO producto
            (nombre, descripcion, precio, disponible, id_categoria)
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            producto.nombre,
            producto.descripcion,
            producto.precio,
            producto.disponible,
            producto.id_categoria
        )

        cursor.execute(sql, valores)
        conexion.commit()

        producto.id_producto = cursor.lastrowid

        cursor.close()
        conexion.close()

        return producto

    def obtener_todos(self):
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        sql = """
            SELECT
                id_producto,
                nombre,
                descripcion,
                precio,
                disponible,
                id_categoria
            FROM producto
        """

        cursor.execute(sql)

        productos = cursor.fetchall()

        cursor.close()
        conexion.close()

        return productos

    def obtener_por_id(self, id_producto):
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        sql = """
            SELECT
                id_producto,
                nombre,
                descripcion,
                precio,
                disponible,
                id_categoria
            FROM producto
            WHERE id_producto = %s
        """

        cursor.execute(sql, (id_producto,))

        producto = cursor.fetchone()

        cursor.close()
        conexion.close()

        return producto

    def actualizar(self, id_producto, producto):
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE producto
            SET
                nombre = %s,
                descripcion = %s,
                precio = %s,
                disponible = %s,
                id_categoria = %s
            WHERE id_producto = %s
        """

        valores = (
            producto.nombre,
            producto.descripcion,
            producto.precio,
            producto.disponible,
            producto.id_categoria,
            id_producto
        )

        cursor.execute(sql, valores)
        conexion.commit()

        filas_afectadas = cursor.rowcount

        cursor.close()
        conexion.close()

        return filas_afectadas

    def eliminar(self, id_producto):
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            DELETE FROM producto
            WHERE id_producto = %s
        """

        cursor.execute(sql, (id_producto,))
        conexion.commit()

        filas_afectadas = cursor.rowcount

        cursor.close()
        conexion.close()

        return filas_afectadas