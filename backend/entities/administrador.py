class Administrador:
    def __init__(self, id_administrador=None, nombre=None, correo=None, usuario=None, contrasena=None, telefono=None):
        self.id_administrador = id_administrador
        self.nombre = nombre
        self.correo = correo
        self.usuario = usuario
        self.contrasena = contrasena
        self.telefono = telefono

    def to_dict(self):
        # No se incluye la contraseña en la respuesta por seguridad
        return {
            "id_administrador": self.id_administrador,
            "nombre": self.nombre,
            "correo": self.correo,
            "usuario": self.usuario,
            "telefono": self.telefono
        }
