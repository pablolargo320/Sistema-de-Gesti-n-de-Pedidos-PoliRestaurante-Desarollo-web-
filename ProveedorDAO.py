import mysql.connector
def getConnection():
    conn = None
    try:
        conn = mysql.connector.connect(user="root", password="psswrd", host="localhost", database="agenda", port="3306")
    except:
        print("no se puede conectar a la base de datos")
        return 0
    print("conectado")
    return conn


def unconnection(conn):
    conn.close()

def findAll():
    conn = getConnection()
    c = conn.cursor()

    proveedores = """SELECT * FROM agenda.proveedor"""

    c.execute(proveedores)

    proveedoresData = c.fetchall()

    for p in proveedoresData:
        print(p)

    unconnection(conn)

def buscarProveedorPorNombre(nombre):
    conn = getConnection()
    c = conn.cursor()

    proveedores = """SELECT * FROM agenda.proveedor as p WHERE p.nombre LIKE %s"""
    val = ("%{}%".format(nombre),)

    c.execute(proveedores, val)

    proveedoresData = c.fetchall()

    for p in proveedoresData:
        print(p)

    unconnection(conn)

def buscarProveedorPorId(id):
    conn = getConnection()
    c = conn.cursor()

    proveedores = """SELECT * FROM agenda.proveedor as p WHERE p.id_proveedor = %s"""
    val = (id,)

    c.execute(proveedores, val)

    proveedoresData = c.fetchall()

    for p in proveedoresData:
        print(p)

    unconnection(conn)


def buscarProveedoresPorProducto(idProducto):
    conn = getConnection()
    c = conn.cursor()

    proveedores = """SELECT * FROM agenda.proveedor as p WHERE p.producto_id_producto = %s"""
    val = (idProducto,)

    c.execute(proveedores, val)

    proveedoresData = c.fetchall()

    for p in proveedoresData:
        print(p)

    unconnection(conn)


def crearProveedor(nombre, telefono, correo, direccion, productoIdProducto):
    conn = getConnection()
    c = conn.cursor()
    proveedorInsert = """INSERT into proveedor (nombre, telefono, correo, direccion, producto_id_producto) VALUES (%s, %s, 
    %s, %s, %s)"""
    val = (nombre, telefono, correo, direccion, productoIdProducto)
    #print(proveedorInsert)
    c.execute(proveedorInsert, val)
    conn.commit()
    print(c.rowcount, "record inserted.")
    unconnection(conn)

def editarProveedor(nombre, telefono, correo, direccion, productoIdProducto, id):
    conn = getConnection()
    c = conn.cursor()
    proveedorUpdate = """UPDATE proveedor SET nombre = %s, 
    telefono = %s, 
    correo = %s, 
    direccion = %s, 
    producto_id_producto = %s 
    WHERE id_proveedor = %s"""
    val = (nombre, telefono, correo, direccion, productoIdProducto, id)
    #print(proveedorUpdate)
    c.execute(proveedorUpdate, val)
    conn.commit()
    print(c.rowcount, "record updated.")
    unconnection(conn)

def eliminarProveedor(id):
    conn = getConnection()
    c = conn.cursor()
    proveedorDelete = """DELETE FROM proveedor WHERE id_proveedor = %s"""
    val = (id,)
    #print(proveedorDelete)
    c.execute(proveedorDelete, val)
    conn.commit()
    print(c.rowcount, "record deleted.")
    unconnection(conn)
