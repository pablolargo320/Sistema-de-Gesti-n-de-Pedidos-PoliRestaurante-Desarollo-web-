from backend.database.connection import getConnection, closeConnection
from backend.entities.metodopago import MetodoPago


def findAll():
    conn = getConnection()
    c = conn.cursor()

    c.execute("SELECT id_metodo_pago, efectivo, aplicacion, tarjeta, descripcion, estado FROM metodo_pago")
    rows = c.fetchall()

    closeConnection(conn)
    return [MetodoPago(*row).to_dict() for row in rows]


def buscarMetodoPagoPorId(id_metodo_pago):
    conn = getConnection()
    c = conn.cursor()

    c.execute(
        "SELECT id_metodo_pago, efectivo, aplicacion, tarjeta, descripcion, estado FROM metodo_pago WHERE id_metodo_pago = %s",
        (id_metodo_pago,)
    )
    row = c.fetchone()

    closeConnection(conn)
    return MetodoPago(*row).to_dict() if row else None


def crearMetodoPago(efectivo, aplicacion, tarjeta, descripcion, estado):
    conn = getConnection()
    c = conn.cursor()

    metodoPagoInsert = """INSERT INTO metodo_pago (efectivo, aplicacion, tarjeta, descripcion, estado)
    VALUES (%s, %s, %s, %s, %s)"""
    val = (efectivo, aplicacion, tarjeta, descripcion, estado)

    c.execute(metodoPagoInsert, val)
    conn.commit()
    nuevoId = c.lastrowid
    print(c.rowcount, "record inserted.")

    closeConnection(conn)
    return nuevoId


def editarMetodoPago(id_metodo_pago, efectivo, aplicacion, tarjeta, descripcion, estado):
    conn = getConnection()
    c = conn.cursor()

    metodoPagoUpdate = """UPDATE metodo_pago SET efectivo = %s,
    aplicacion = %s,
    tarjeta = %s,
    descripcion = %s,
    estado = %s
    WHERE id_metodo_pago = %s"""
    val = (efectivo, aplicacion, tarjeta, descripcion, estado, id_metodo_pago)

    c.execute(metodoPagoUpdate, val)
    conn.commit()
    filas = c.rowcount
    print(filas, "record updated.")

    closeConnection(conn)
    return filas


def eliminarMetodoPago(id_metodo_pago):
    conn = getConnection()
    c = conn.cursor()

    metodoPagoDelete = """DELETE FROM metodo_pago WHERE id_metodo_pago = %s"""
    val = (id_metodo_pago,)

    c.execute(metodoPagoDelete, val)
    conn.commit()
    filas = c.rowcount
    print(filas, "record deleted.")

    closeConnection(conn)
    return filas
