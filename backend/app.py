from flask import Flask

from routes.mesa_routes import mesa_bp
from routes.administrador_routes import administrador_bp
from routes.metodopago_routes import metodopago_bp

app = Flask(__name__)

app.register_blueprint(mesa_bp)
app.register_blueprint(administrador_bp)
app.register_blueprint(metodopago_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
