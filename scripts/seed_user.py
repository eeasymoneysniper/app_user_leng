# scripts/seed_user.py
import os
import dotenv
dotenv.load_dotenv()

from APP.basededatos import SessionLocal, engine, Base
from APP.modelos import users
from APP.hash import get_password_hashed

def create_user(nombre: str, dni: int, password: str):
    db = SessionLocal()
    try:
        u = db.query(users).filter(users.dni == dni).first()
        if u:
            print("Usuario ya existe:", u.user_id)
            return
        usuario = users(nombre=nombre, dni=dni, password=get_password_hashed(password))
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        print("Usuario creado id:", usuario.user_id)
    finally:
        db.close()

if __name__ == "__main__":
    # Ajusta valores si quieres
    create_user("Demo", 12345678, "secret")
