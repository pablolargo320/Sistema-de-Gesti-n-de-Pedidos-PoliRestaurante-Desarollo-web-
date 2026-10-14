from database.connection import getConnection, closeConnection
from entities.mesa import Mesa


def findAll():
    conn = getConnection()
    c = conn.cursor()

    c.execute("SELECT id_mesa, numero, estado FROM mesa")
    rows = c.fetchall()

    closeConnection(conn)
    return [Mesa(*row).to_dict() for row in rows]


def buscarMesaPorId(id_mesa):
    conn = getConnection()
    c = conn.cursor()

    c.execute("SELECT id_mesa, numero, estado FROM mesa WHERE id_mesa = %s", (id_mesa,))
    row = c.fetchone()

    closeConnection(conn)
    return Mesa(*row).to_dict() if row else None


def crearMesa(numero, estado):
    conn = getConnection()
    c = conn.cursor()

    mesaInsert = """INSERT INTO mesa (numero, estado) VALUES (%s, %s)"""
    val = (numero, estado)

    c.execute(mesaInsert, val)
    conn.commit()
    nuevoId = c.lastrowid
    print(c.rowcount, "record inserted.")

    closeConnection(conn)
    return nuevoId


def editarMesa(id_mesa, numero, estado):
    conn = getConnection()
    c = conn.cursor()

    mesaUpdate = """UPDATE mesa SET numero = %s,
    estado = %s
    WHERE id_mesa = %s"""
    val = (numero, estado, id_mesa)

    c.execute(mesaUpdate, val)
    conn.commit()
    filas = c.rowcount
    print(filas, "record updated.")

    closeConnection(conn)
    return filas


def eliminarMesa(id_mesa):
    conn = getConnection()
    c = conn.cursor()

    mesaDelete = """DELETE FROM mesa WHERE id_mesa = %s"""
    val = (id_mesa,)

    c.execute(mesaDelete, val)
    conn.commit()
    filas = c.rowcount
    print(filas, "record deleted.")

    closeConnection(conn)
    return filas
