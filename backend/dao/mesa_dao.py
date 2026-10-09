
from backend.database.connection import get_connection
import mysql.connector


class MesaDAO:

    def crear(self, mesa):

        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO mesa
            (numero, estado)
            VALUES (%s, %s)
        """

        valores = (
            mesa.numero,
            mesa.estado
        )

        cursor.execute(sql, valores)
        conexion.commit()

        mesa.id_mesa = cursor.lastrowid

        cursor.close()
        conexion.close()

        return mesa

    def obtener_todos(self):

        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        sql = """
            SELECT
                id_mesa,
                numero,
                estado
            FROM mesa
            ORDER BY numero
        """

        cursor.execute(sql)

        mesas = cursor.fetchall()

        cursor.close()
        conexion.close()

        return mesas

    def obtener_por_id(self, id_mesa):

        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        sql = """
            SELECT
                id_mesa,
                numero,
                estado
            FROM mesa
            WHERE id_mesa = %s
        """

        cursor.execute(sql, (id_mesa,))

        mesa = cursor.fetchone()

        cursor.close()
        conexion.close()

        return mesa

    def obtener_por_numero(self, numero):

        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        sql = """
            SELECT
                id_mesa,
                numero,
                estado
            FROM mesa
            WHERE numero = %s
        """

        cursor.execute(sql, (numero,))

        mesa = cursor.fetchone()

        cursor.close()
        conexion.close()

        return mesa

    def actualizar(self, id_mesa, mesa):

        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE mesa
            SET
                numero = %s,
                estado = %s
            WHERE id_mesa = %s
        """

        valores = (
            mesa.numero,
            mesa.estado,
            id_mesa
        )

        cursor.execute(sql, valores)
        conexion.commit()

        filas_afectadas = cursor.rowcount

        cursor.close()
        conexion.close()

        return filas_afectadas

    def cambiar_estado(self, id_mesa, estado):

        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE mesa
            SET estado = %s
            WHERE id_mesa = %s
        """

        valores = (
            estado,
            id_mesa
        )

        cursor.execute(sql, valores)
        conexion.commit()

        filas_afectadas = cursor.rowcount

        cursor.close()
        conexion.close()

        return filas_afectadas

    def eliminar(self, id_mesa):

        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
        DELETE FROM mesa
        WHERE id_mesa = %s
        """

        try:

            cursor.execute(sql, (id_mesa,))
            conexion.commit()

            filas_afectadas = cursor.rowcount

            return filas_afectadas

        except mysql.connector.IntegrityError:

            conexion.rollback()

            return -1

        finally:

            cursor.close()
            conexion.close()


    def obtener_por_estado(self, estado):

        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        sql = """
            SELECT
                id_mesa,
                numero,
                estado
            FROM mesa
            WHERE estado = %s
            ORDER BY numero
        """

        cursor.execute(sql, (estado,))

        mesas = cursor.fetchall()

        cursor.close()
        conexion.close()

        return mesas
    
    def actualizar(self, id_mesa, mesa):

        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE mesa
            SET
                numero = %s,
                estado = %s
        WHERE id_mesa = %s
        """
        valores = (
        mesa.numero,
        mesa.estado,
        id_mesa
        )

        cursor.execute(sql, valores)
        conexion.commit()

        filas_afectadas = cursor.rowcount

        cursor.close()
        conexion.close()

        return filas_afectadas

    def eliminar(self, id_mesa):

        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
        DELETE FROM mesa
        WHERE id_mesa = %s
        """

        cursor.execute(sql, (id_mesa,))
        conexion.commit()

        filas_afectadas = cursor.rowcount

        cursor.close()
        conexion.close()

        return filas_afectadas
