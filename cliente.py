import requests

URL = "http://127.0.0.1:5000"
s = requests.Session()  # mantiene la cookie de sesión


def pedir():
    return input("Usuario: "), input("Contraseña: ")

while True:
    op = input("1) Registro\n2) Login\n3) Ver tareas\n4) Salir\n> ")
    if op in ("1", "2"):
        u, p = pedir()
        r = s.post(f"{URL}/{'registro' if op == '1' else 'login'}",
                   json={"usuario": u, "contraseña": p})
        print(r.status_code, r.json())
    elif op == "3":
        r = s.get(f"{URL}/tareas")
        print(r.status_code, r.text)
    elif op == "4":
        break
