
import get_connection


class ProveedorDAO:

    def crear(self, proveedor):

        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO proveedor
            (
                nombre,
                telefono,
                correo,
                direccion,
                producto_id_producto
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            proveedor.nombre,
            proveedor.telefono,
            proveedor.correo,
            proveedor.direccion,
            proveedor.producto_id_producto
        )

        cursor.execute(sql, valores)

        conexion.commit()

        proveedor.id_proveedor = cursor.lastrowid

        cursor.close()
        conexion.close()

        return proveedor

    def obtener_todos(self):

        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        sql = """
            SELECT
                id_proveedor,
                nombre,
                telefono,
                correo,
                direccion,
                producto_id_producto
            FROM proveedor
            ORDER BY id_proveedor
        """

        cursor.execute(sql)

        proveedores = cursor.fetchall()

        cursor.close()
        conexion.close()

        return proveedores

    def obtener_por_id(self, id_proveedor):

        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        sql = """
            SELECT
                id_proveedor,
                nombre,
                telefono,
                correo,
                direccion,
                producto_id_producto
            FROM proveedor
            WHERE id_proveedor = %s
        """

        cursor.execute(sql, (id_proveedor,))

        proveedor = cursor.fetchone()

        cursor.close()
        conexion.close()

        return proveedor

    def obtener_por_nombre(self, nombre):

        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        sql = """
            SELECT
                id_proveedor,
                nombre,
                telefono,
                correo,
                direccion,
                producto_id_producto
            FROM proveedor
            WHERE nombre LIKE %s
            ORDER BY nombre
        """

        valor = (f"%{nombre}%",)

        cursor.execute(sql, valor)

        proveedores = cursor.fetchall()

        cursor.close()
        conexion.close()

        return proveedores

    def obtener_por_producto(self, id_producto):

        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        sql = """
            SELECT
                id_proveedor,
                nombre,
                telefono,
                correo,
                direccion,
                producto_id_producto
            FROM proveedor
            WHERE producto_id_producto = %s
            ORDER BY nombre
        """

        cursor.execute(sql, (id_producto,))

        proveedores = cursor.fetchall()

        cursor.close()
        conexion.close()

        return proveedores

    def actualizar(self, id_proveedor, proveedor):

        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE proveedor
            SET
                nombre = %s,
                telefono = %s,
                correo = %s,
                direccion = %s,
                producto_id_producto = %s
            WHERE id_proveedor = %s
        """

        valores = (
            proveedor.nombre,
            proveedor.telefono,
            proveedor.correo,
            proveedor.direccion,
            proveedor.producto_id_producto,
            id_proveedor
        )

        cursor.execute(sql, valores)

        conexion.commit()

        filas_afectadas = cursor.rowcount

        cursor.close()
        conexion.close()

        return filas_afectadas

    def eliminar(self, id_proveedor):

        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            DELETE FROM proveedor
            WHERE id_proveedor = %s
        """

        cursor.execute(sql, (id_proveedor,))

        conexion.commit()

        filas_afectadas = cursor.rowcount

        cursor.close()
        conexion.close()

        return filas_afectadas