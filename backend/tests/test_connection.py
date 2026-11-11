from backend.database.connection import get_connection

def test_conexion_base_datos():
    try:
        conexion = get_connection()
        assert conexion is not None, "La conexión retorno None"
        assert conexion.is_connected(), "El driver de MySQL no está conectado"
        conexion.close()
    except Exception as e:
        assert False, f"Error de conexion con mysql-connector: {e}"
