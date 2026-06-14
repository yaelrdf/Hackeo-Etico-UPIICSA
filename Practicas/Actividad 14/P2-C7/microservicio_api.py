from flask import Flask, request, jsonify, make_response
import jwt
import time
import sqlite3
import os
import logging

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "inter.db")
AUDIT_LOG = os.path.join(BASE_DIR, "auditoria.log")
JWT_SECRET = "secret_server_keys"
EXPECTED_API_KEY = "1234567890"

logging.basicConfig(
    filename=AUDIT_LOG,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def conectar():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with conectar() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS habitaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ciudad TEXT NOT NULL,
                hotel TEXT NOT NULL,
                tipo TEXT NOT NULL,
                precio_noche REAL NOT NULL,
                disponibles INTEGER NOT NULL
            )
        """)
        cantidad = conn.execute("SELECT COUNT(*) AS total FROM habitaciones").fetchone()[0]
        if cantidad == 0:
            conn.executemany(
                "INSERT INTO habitaciones (ciudad, hotel, tipo, precio_noche, disponibles) VALUES (?, ?, ?, ?, ?)",
                [
                    ("Ciudad de México", "Inter Reforma", "Sencilla", 1450.00, 8),
                    ("Guadalajara", "Inter Expo", "Doble", 1690.00, 6),
                    ("Monterrey", "Inter Fundidora", "Suite", 2450.00, 3),
                    ("Puebla", "Inter Angelópolis", "Sencilla", 1320.00, 10),
                ],
            )
            conn.commit()

def registrar_evento(mensaje, usuario="desconocido", ip=None):
    ip = ip or request.remote_addr or "0.0.0.0"
    logging.info("usuario=%s | ip=%s | evento=%s", usuario, ip, mensaje)

def aceptar_json():
    accept = request.headers.get("Accept", "*/*")
    return ("application/json" in accept) or ("*/*" in accept)

def validar_content_type():
    content_type = request.headers.get("Content-Type", "")
    return "application/json" in content_type

def extraer_autorizacion():
    authorization = request.headers.get("Authorization", "")
    if not authorization.startswith("Bearer "):
        return None
    return authorization.split(" ", 1)[1].strip()

def verificar_token(token, credenciales):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], options={"verify_exp": False})
    except jwt.InvalidTokenError:
        return False, "Token inválido"
    if decoded.get("aplicacion") != credenciales.get("aplicacion"):
        return False, "Aplicación no coincide"
    if decoded.get("contrasena") != credenciales.get("contrasena"):
        return False, "Contraseña no coincide"
    if int(decoded.get("caducidad", 0)) <= int(time.time()):
        return False, "Token caducado"
    return True, decoded

def respuesta_json(mensaje, codigo_http, token=None, extra=None):
    payload = {"mensaje": mensaje, "codigo_http": str(codigo_http)}
    if token is not None:
        payload["token_del_portador"] = token
    if extra:
        payload.update(extra)
    return make_response(jsonify(payload), codigo_http)

@app.after_request
def aplicar_cabeceras_seguridad(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cache-Control"] = "no-store, max-age=0"
    response.headers["Access-Control-Allow-Origin"] = "*"
    if response.mimetype == "application/json":
        response.headers["Content-Type"] = "application/json; charset=UTF-8"
    return response

@app.route("/api/get-ciudades", methods=["POST"])
def get_ciudades():
    if not aceptar_json():
        registrar_evento("Solicitud con Accept inválido")
        return respuesta_json("Unacceptable Media Type", 406)
    if not validar_content_type():
        registrar_evento("Solicitud con Content-Type inválido")
        return respuesta_json("Unsupported Media Type", 415)

    datos = request.get_json(silent=True) or {}
    api_clave = str(datos.get("apiClave", "")).strip()
    aplicacion = str(datos.get("aplicacion", "")).strip()
    contrasena = str(datos.get("contrasena", "")).strip()

    if api_clave != EXPECTED_API_KEY:
        registrar_evento("API key inválida", aplicacion)
        return respuesta_json("Error: Solicitud no autorizada.", 401, token=extraer_autorizacion())

    token = extraer_autorizacion()
    if token is None:
        registrar_evento("Falta cabecera Authorization", aplicacion)
        return respuesta_json("Error: Solicitud no autorizada.", 401)

    autorizado, detalle = verificar_token(token, {"aplicacion": aplicacion, "contrasena": contrasena})
    if not autorizado:
        registrar_evento(f"Token rechazado: {detalle}", aplicacion)
        return respuesta_json("Error: Solicitud no autorizada.", 401, token=token)

    with conectar() as conn:
        filas = conn.execute("SELECT id, ciudad, hotel, tipo, precio_noche, disponibles FROM habitaciones WHERE disponibles > 0").fetchall()
        habitaciones = [dict(fila) for fila in filas]

    registrar_evento("Solicitud GET autorizada", aplicacion)
    return respuesta_json(
        "API servicio GET ejecutado.",
        200,
        token=token,
        extra={"habitaciones": habitaciones},
    )

@app.route("/api/reservar-habitacion", methods=["PUT"])
def reservar_habitacion():
    if not aceptar_json():
        registrar_evento("Reserva con Accept inválido")
        return respuesta_json("Unacceptable Media Type", 406)
    if not validar_content_type():
        registrar_evento("Reserva con Content-Type inválido")
        return respuesta_json("Unsupported Media Type", 415)

    datos = request.get_json(silent=True) or {}
    api_clave = str(datos.get("apiClave", "")).strip()
    aplicacion = str(datos.get("aplicacion", "")).strip()
    contrasena = str(datos.get("contrasena", "")).strip()
    id_habitacion = int(datos.get("idHabitacion", 0) or 0)
    cantidad = int(datos.get("cantidad", 1) or 1)

    if api_clave != EXPECTED_API_KEY:
        registrar_evento("API key inválida en reserva", aplicacion)
        return respuesta_json("Error: Solicitud no autorizada.", 401)

    token = extraer_autorizacion()
    if token is None:
        registrar_evento("Falta token en reserva", aplicacion)
        return respuesta_json("Error: Solicitud no autorizada.", 401)

    autorizado, detalle = verificar_token(token, {"aplicacion": aplicacion, "contrasena": contrasena})
    if not autorizado:
        registrar_evento(f"Token rechazado en reserva: {detalle}", aplicacion)
        return respuesta_json("Error: Solicitud no autorizada.", 401, token=token)

    if id_habitacion <= 0 or cantidad <= 0:
        registrar_evento("Datos de reserva inválidos", aplicacion)
        return respuesta_json("Datos de entrada inválidos.", 400, token=token)

    with conectar() as conn:
        fila = conn.execute("SELECT id, ciudad, hotel, tipo, precio_noche, disponibles FROM habitaciones WHERE id = ?", (id_habitacion,)).fetchone()
        if fila is None:
            registrar_evento("Habitación no encontrada", aplicacion)
            return respuesta_json("Habitación no encontrada.", 404, token=token)
        if fila["disponibles"] < cantidad:
            registrar_evento("Disponibilidad insuficiente", aplicacion)
            return respuesta_json("No hay suficientes habitaciones disponibles.", 409, token=token)
        conn.execute("UPDATE habitaciones SET disponibles = disponibles - ? WHERE id = ?", (cantidad, id_habitacion))
        conn.commit()

    registrar_evento(f"Reserva confirmada: id={id_habitacion}, cantidad={cantidad}", aplicacion)
    return respuesta_json(
        "Reserva confirmada.",
        200,
        token=token,
        extra={"idHabitacion": id_habitacion, "cantidad": cantidad},
    )

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5001, debug=True)
