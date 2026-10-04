import sqlite3
from flask import Flask, request, jsonify, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "pfo2-redes"
DB = "users.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )"""
        )

@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json(silent=True) or {}
    usuario = (datos.get("usuario") or "").strip()
    contrasena = datos.get("contraseña") or ""

    if not usuario or not contrasena:
        return jsonify({"error": "Faltan 'usuario' o 'contraseña'"}), 400

    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (usuario, generate_password_hash(contrasena)),
            )
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409

    return jsonify({"mensaje": f"Usuario '{usuario}' registrado correctamente"}), 201


@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json(silent=True) or {}
    usuario = (datos.get("usuario") or "").strip()
    contrasena = datos.get("contraseña") or ""

    with get_db() as conn:
        fila = conn.execute(
            "SELECT * FROM users WHERE username = ?", (usuario,)
        ).fetchone()

    if fila is None or not check_password_hash(fila["password_hash"], contrasena):
        return jsonify({"error": "Credenciales inválidas"}), 401

    session["user"] = fila["username"]
    return jsonify({"mensaje": f"Bienvenido, {usuario}"}), 200


@app.route("/tareas", methods=["GET"])
def tareas():
        usuario = session.get("user")
        if not usuario:
            return jsonify({"error": "Debes iniciar sesion para acceder a la lista de tareas"}), 401
        return render_template("tareas.html", usuario=usuario)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
