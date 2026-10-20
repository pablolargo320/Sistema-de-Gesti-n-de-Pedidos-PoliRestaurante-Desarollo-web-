from backend.database.connection import getConnection, closeConnection
from backend.entities.administrador import Administrador


def findAll():
    conn = getConnection()
    c = conn.cursor()

    c.execute("SELECT id_administrador, nombre, correo, usuario, contraseña, telefono FROM Administrador")
    rows = c.fetchall()

    closeConnection(conn)
    return [Administrador(*row).to_dict() for row in rows]


def buscarAdministradorPorId(id_administrador):
    conn = getConnection()
    c = conn.cursor()

    c.execute(
        "SELECT id_administrador, nombre, correo, usuario, contraseña, telefono FROM Administrador WHERE id_administrador = %s",
        (id_administrador,)
    )
    row = c.fetchone()

    closeConnection(conn)
    return Administrador(*row).to_dict() if row else None


def crearAdministrador(nombre, correo, usuario, contrasena, telefono):
    conn = getConnection()
    c = conn.cursor()

    administradorInsert = """INSERT INTO Administrador (nombre, correo, usuario, contraseña, telefono)
    VALUES (%s, %s, %s, %s, %s)"""
    val = (nombre, correo, usuario, contrasena, telefono)

    c.execute(administradorInsert, val)
    conn.commit()
    nuevoId = c.lastrowid
    print(c.rowcount, "record inserted.")

    closeConnection(conn)
    return nuevoId


def editarAdministrador(id_administrador, nombre, correo, usuario, contrasena, telefono):
    conn = getConnection()
    c = conn.cursor()

    administradorUpdate = """UPDATE Administrador SET nombre = %s,
    correo = %s,
    usuario = %s,
    contraseña = %s,
    telefono = %s
    WHERE id_administrador = %s"""
    val = (nombre, correo, usuario, contrasena, telefono, id_administrador)

    c.execute(administradorUpdate, val)
    conn.commit()
    filas = c.rowcount
    print(filas, "record updated.")

    closeConnection(conn)
    return filas


def eliminarAdministrador(id_administrador):
    conn = getConnection()
    c = conn.cursor()

    administradorDelete = """DELETE FROM Administrador WHERE id_administrador = %s"""
    val = (id_administrador,)

    c.execute(administradorDelete, val)
    conn.commit()
    filas = c.rowcount
    print(filas, "record deleted.")

    closeConnection(conn)
    return filas
