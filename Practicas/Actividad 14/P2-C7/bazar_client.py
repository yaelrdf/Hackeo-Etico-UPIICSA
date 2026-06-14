from flask import Flask, render_template_string
import jwt
import requests
import time

app = Flask(__name__)

APP_NAME = "Bazar"
APP_PASSWORD = "123"
JWT_SECRET = "secret_server_keys"
API_KEY = "1234567890"
API_BASE_URL = "http://127.0.0.1:5001"

def generar_token():
    payload = {
        "aplicacion": APP_NAME,
        "contrasena": APP_PASSWORD,
        "caducidad": int(time.time()) + 3600,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token if isinstance(token, str) else token.decode("utf-8")

@app.route("/")
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Bazar de ciudades</title>
    </head>
    <body>
      <h1>Elija un servicio</h1>
      <p><a href="/get-ciudades">Paquetes de ciudades</a></p>
      <p><a href="/reservar/1">Reservar habitación #1</a></p>
    </body>
    </html>
    """)

@app.route("/get-ciudades")
def get_ciudades():
    token = generar_token()
    payload = {"apiClave": API_KEY, "aplicacion": APP_NAME, "contrasena": APP_PASSWORD}
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    respuesta = requests.post(f"{API_BASE_URL}/api/get-ciudades", json=payload, headers=headers, timeout=10)
    try:
        datos = respuesta.json()
    except ValueError:
        datos = {
            "mensaje": "Respuesta no JSON",
            "codigo_http": str(respuesta.status_code),
            "contenido": respuesta.text
        }
    plantilla = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Resultado del servicio</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 2rem; }
        table { border-collapse: collapse; width: 100%; margin-top: 1rem; }
        th, td { border: 1px solid #999; padding: 0.5rem; text-align: left; }
        th { background: #efefef; }
      </style>
    </head>
    <body>
      <h1>Resultado del microservicio</h1>
      <p><strong>Mensaje:</strong> {{ datos.get('mensaje', '') }}</p>
      <p><strong>Código HTTP:</strong> {{ datos.get('codigo_http', '') }}</p>
      <p><strong>Token:</strong> {{ datos.get('token_del_portador', '') }}</p>
      {% if datos.get('habitaciones') %}
      <h2>Habitaciones disponibles</h2>
      <table>
        <tr>
          <th>ID</th><th>Ciudad</th><th>Hotel</th><th>Tipo</th><th>Precio por noche</th><th>Disponibles</th>
        </tr>
        {% for h in datos.get('habitaciones', []) %}
        <tr>
          <td>{{ h['id'] }}</td>
          <td>{{ h['ciudad'] }}</td>
          <td>{{ h['hotel'] }}</td>
          <td>{{ h['tipo'] }}</td>
          <td>{{ h['precio_noche'] }}</td>
          <td>{{ h['disponibles'] }}</td>
        </tr>
        {% endfor %}
      </table>
      {% endif %}
      <p><strong>Depuración:</strong> status_code={{ respuesta.status_code }}, content_type={{ respuesta.headers.get('Content-Type', '') }}</p>
      <p><a href="/">Regresar al inicio</a></p>
    </body>
    </html>
    """
    return render_template_string(plantilla, datos=datos, respuesta=respuesta)

@app.route("/reservar/<int:id_habitacion>")
def reservar(id_habitacion):
    token = generar_token()
    payload = {
        "apiClave": API_KEY,
        "aplicacion": APP_NAME,
        "contrasena": APP_PASSWORD,
        "idHabitacion": id_habitacion,
        "cantidad": 1,
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    respuesta = requests.put(f"{API_BASE_URL}/api/reservar-habitacion", json=payload, headers=headers, timeout=10)
    try:
        datos = respuesta.json()
    except ValueError:
        datos = {"mensaje": "Respuesta no JSON", "codigo_http": str(respuesta.status_code), "contenido": respuesta.text}
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"><title>Reserva</title></head>
    <body>
      <h1>Resultado de la reserva</h1>
      <pre>{{ datos | tojson(indent=2) }}</pre>
      <p><a href="/">Regresar</a></p>
    </body>
    </html>
    """, datos=datos)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
