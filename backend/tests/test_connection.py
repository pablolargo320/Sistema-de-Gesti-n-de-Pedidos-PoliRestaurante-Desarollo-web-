from database.connection import get_connection


try:
    conexion = get_connection()
    print("Conexión exitosa con la base de datos")

    conexion.close()

except Exception as e:
    print("Error de conexión:")
    print(e)