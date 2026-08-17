from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from typing import Annotated
from PRACTICA.modelos import lenguajes,users
from PRACTICA.basededatos import get_db
from PRACTICA.esquemas import leng_post,leng_response,leng_put
from PRACTICA.routers.auth import get_current_user


router = APIRouter()   


#LENGUAJES

@router.get("/usuarios/{user_id}/lenguajes",status_code=status.HTTP_200_OK,response_model=list[leng_response])
async def obtener_lenguajes_de_usuario(user_id:int,db:Annotated[Session,Depends(get_db)],skip = 0,limit = 5):
    usuario = db.query(users).filter(users.user_id == user_id).first()
    
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Usuario no encontrado.")
    
    lenguajes_usuario = db.query(lenguajes).filter(lenguajes.usuario_id == user_id).offset(skip).limit(limit).all()
    
    
    return lenguajes_usuario




@router.post("/usuarios/{user_id}/lenguajes",status_code=status.HTTP_201_CREATED,response_model=leng_response)
async def agregar_lenguajes(user_id : int,lenguaje_nuevo : leng_post,db : Annotated[Session,Depends(get_db)],current_user : Annotated[users,Depends(get_current_user)]):
    usuario = db.query(users).filter(users.user_id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Usuario no encontrado.")
    
    if usuario.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permisos para agregar lenguajes a este usuario.")
    
    
    nombre_lenguaje = lenguaje_nuevo.lenguaje.strip().lower()
    
    lenguaje_existente = db.query(lenguajes).filter(lenguajes.usuario_id == user_id,lenguajes.lenguajes == nombre_lenguaje).first()
    if lenguaje_existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"El usuario con ID {user_id} ya conoce el lenguaje {lenguaje_nuevo.lenguaje}.")
    
  
    
    lenguajes_nuevo = lenguajes(usuario_id = user_id,lenguajes = nombre_lenguaje)
        
    db.add(lenguajes_nuevo)
    db.commit()
    db.refresh(lenguajes_nuevo)
    return lenguajes_nuevo


@router.put("/lenguajes/{leng_id}",status_code=status.HTTP_200_OK,response_model=leng_response)
async def actualizar_lenguaje(leng_id : int,lenguaje : leng_put,db : Annotated[Session,Depends(get_db)],current_user : Annotated[users,Depends(get_current_user)]):
    lenguaje_existente = db.query(lenguajes).filter(lenguajes.leng_id == leng_id).first()
    if not lenguaje_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Lenguaje no encontrado.")
    
    if lenguaje_existente.usuario_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permisos para actualizar este lenguaje.")
    
    if lenguaje.lenguajes != None:
        lenguaje_existente.lenguajes = lenguaje.lenguajes
    
    db.commit()
    db.refresh(lenguaje_existente)
    return lenguaje_existente


@router.delete("/lenguajes/{leng_id}",status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_lenguaje(leng_id : int , db : Annotated[Session,Depends(get_db)],current_user : Annotated[users,Depends(get_current_user)]):
    lenguaje_existente = db.query(lenguajes).filter(lenguajes.leng_id == leng_id).first()
    if not lenguaje_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Lenguaje no encontrado.")
    
    if lenguaje_existente.usuario_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permisos para eliminar este lenguaje.")
    
    db.delete(lenguaje_existente)
    db.commit()



    
    

