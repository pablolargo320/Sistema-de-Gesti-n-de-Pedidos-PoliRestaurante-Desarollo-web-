from backend.database.connection import getSession
from backend.entities.metodopago import MetodoPago


def findAll():
    session = getSession()
    metodos = session.query(MetodoPago).all()
    resultado = [m.to_dict() for m in metodos]
    session.close()
    return resultado


def buscarMetodoPagoPorId(id_metodo_pago):
    session = getSession()
    metodo = session.query(MetodoPago).filter(MetodoPago.id_metodo_pago == id_metodo_pago).first()
    resultado = metodo.to_dict() if metodo else None
    session.close()
    return resultado


def crearMetodoPago(efectivo, aplicacion, tarjeta, descripcion, estado):
    session = getSession()
    metodo = MetodoPago(
        efectivo=efectivo, aplicacion=aplicacion, tarjeta=tarjeta,
        descripcion=descripcion, estado=estado
    )
    session.add(metodo)
    session.commit()
    nuevoId = metodo.id_metodo_pago
    session.close()
    return nuevoId


def editarMetodoPago(id_metodo_pago, efectivo, aplicacion, tarjeta, descripcion, estado):
    session = getSession()
    metodo = session.query(MetodoPago).filter(MetodoPago.id_metodo_pago == id_metodo_pago).first()
    filas = 0
    if metodo:
        metodo.efectivo = efectivo
        metodo.aplicacion = aplicacion
        metodo.tarjeta = tarjeta
        metodo.descripcion = descripcion
        metodo.estado = estado
        session.commit()
        filas = 1
    session.close()
    return filas


def eliminarMetodoPago(id_metodo_pago):
    session = getSession()
    metodo = session.query(MetodoPago).filter(MetodoPago.id_metodo_pago == id_metodo_pago).first()
    filas = 0
    if metodo:
        session.delete(metodo)
        session.commit()
        filas = 1
    session.close()
    return filas