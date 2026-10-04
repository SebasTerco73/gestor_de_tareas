# PFO 2: Sistema de Gestión de Tareas con API y Base de Datos

API REST en Flask con registro, login y persistencia en SQLite. Las contraseñas se guardan hasheadas con `werkzeug.security`.

## Estructura

```
├── servidor.py     # API Flask + SQLite
├── cliente.py      # Cliente de consola 
└── README.md
```

## Cómo ejecutar

```bash
git clone 
cd 
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install flask requests
python servidor.py  # Con thunder client o postman
python cliente.py   # Por consola
```

El servidor queda en `http://127.0.0.1:5000` y crea `users.db` automáticamente.

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/registro` | Crea un usuario. Body: `{"username": "sebas", "password": "1234"}` |
| POST | `/login` | Verifica credenciales e inicia sesión (cookie) |
| GET | `/tareas` | HTML de bienvenida (requiere haber iniciado sesión) |

## Pruebas con curl

```bash
# Registro  -> 201
curl -X POST http://127.0.0.1:5000/registro \
  -H "Content-Type: application/json" \
  -d '{"username":"sebas","password":"1234"}'

# Login (guarda la cookie)  -> 200
curl -X POST http://127.0.0.1:5000/login -c cookies.txt \
  -H "Content-Type: application/json" \
  -d '{"username":"sebas","password":"1234"}'

# Tareas (usa la cookie)  -> 200 + HTML
curl http://127.0.0.1:5000/tareas -b cookies.txt

# Tareas sin login  -> 401
curl http://127.0.0.1:5000/tareas
```

También puede probarse con `python cliente.py`.

## Capturas de pantalla



## Respuestas conceptuales

**¿Por qué hashear contraseñas?**
Si la base de datos se filtra o alguien con acceso (un administrador, un backup expuesto) la lee, las contraseñas en texto plano quedan comprometidas al instante, y como mucha gente las reutiliza, el daño se extiende a otros servicios. Un hash es una función de un solo sentido: el servidor nunca necesita conocer la contraseña real, solo comparar el hash de lo que se ingresa con el almacenado. Con salt aleatoria, que `generate_password_hash` agrega automáticamente, dos usuarios con la misma contraseña tienen hashes distintos y se dificultan los ataques con tablas precalculadas (rainbow tables).

**Ventajas de usar SQLite en este proyecto**
- No requiere instalar ni configurar un servidor de base de datos: es un único archivo (`users.db`).
- Viene incluido en Python (`sqlite3`), sin dependencias extra.
- Es ideal para proyectos pequeños, prototipos y entornos de aprendizaje: fácil de entregar, copiar y reiniciar.
- Ofrece persistencia real y soporta SQL estándar, restricciones (`UNIQUE`) y transacciones.
- Su limitación es la concurrencia de escrituras y la escalabilidad, por lo que en producción con mucho tráfico convendría migrar a PostgreSQL o MySQL.

