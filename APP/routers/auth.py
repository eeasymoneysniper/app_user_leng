from fastapi import APIRouter
import jwt
from datetime import datetime,timezone,timedelta
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,status,Depends
from sqlalchemy.orm import Session
from typing import Annotated
from PRACTICA.modelos import users
from PRACTICA.basededatos import get_db
from PRACTICA.hash import verify
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

oauth2=OAuth2PasswordBearer(tokenUrl="/login")
CLAVE = os.getenv("CLAVE")
ALGORITMO = os.getenv("ALGORITMO")
ACCESS_TOKEN_EXPIRE_MINUTES = 15




def crear_token(data:dict):
    datos = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos["exp"] = expire
    encoded_jwt = jwt.encode(datos, CLAVE, algorithm=ALGORITMO)
    return encoded_jwt

def get_current_user(token : Annotated[str,Depends(oauth2)],db : Annotated[Session,Depends(get_db)]):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="No se pudo validar las credenciales",headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token,CLAVE,algorithms=[ALGORITMO])
        user_id : str = payload.get("sub")
        if user_id is None:
            raise exception
    except jwt.PyJWTError:
        raise exception
    usuario = db.query(users).filter(users.user_id == int(user_id)).first()
    if not usuario:
        raise exception
    return usuario
        
        

#AUTH y JWT
@router.post("/login")
async def login(form : Annotated[OAuth2PasswordRequestForm, Depends()],db : Annotated[Session,Depends(get_db)]):
    usuario = db.query(users).filter(users.dni == int(form.username)).first()
    if not usuario or not verify(form.password,usuario.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Credenciales inválidas")
    
    return {"access_token" : crear_token(data = {"sub" : str(usuario.user_id)}),"token_type" : "bearer"}
    