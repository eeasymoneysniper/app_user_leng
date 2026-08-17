from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from typing import Annotated
from PRACTICA.modelos import users
from PRACTICA.basededatos import get_db
from PRACTICA.esquemas import usuario_response,usuario_post,usuario_update
from PRACTICA.hash import get_password_hashed,verify
from PRACTICA.routers.auth import crear_token,get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.get("/usuarios",response_model=list[usuario_response],status_code=status.HTTP_200_OK)
async def obtener_usuarios(db : Annotated[Session,Depends(get_db)],skip = 0,limit = 5):
    return db.query(users).offset(skip).limit(limit).all()
    
@router.get("/usuarios/{user_id}",response_model=usuario_response,status_code=status.HTTP_200_OK)
async def obtener_usuario(user_id : int,db : Annotated[Session,Depends(get_db)]):
    usuario = db.query(users).filter(users.user_id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Usuario no encontrado")
    return usuario
    

@router.post('/usuarios',response_model=usuario_response,status_code=status.HTTP_201_CREATED)
async def postear(usuario_nuevo : usuario_post, db : Annotated[Session,Depends(get_db)]):
    db_usuario = db.query(users).filter(users.dni == usuario_nuevo.dni).first()
    if db_usuario:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Ya existe un usuario con dni {usuario_nuevo.dni}.")
    
    usuario = users(nombre = usuario_nuevo.nombre,
                          dni = usuario_nuevo.dni,
                          password = get_password_hashed(usuario_nuevo.password))
    
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/usuarios/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
async def eliminar(user_id : int,db : Annotated[Session,Depends(get_db)],current_user : Annotated[users,Depends(get_current_user)]):
    usuario = db.query(users).filter(users.user_id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Usuario no encontrado")
    if usuario.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permisos para eliminar este usuario")
    db.delete(usuario)  
    db.commit()
        

@router.put("/usuarios/{user_id}",status_code=status.HTTP_200_OK,response_model=usuario_response)
async def actualizar(user_id : int,usuario : usuario_update ,db : Annotated[Session,Depends(get_db)],current_user : Annotated[users,Depends(get_current_user)]):
    user = db.query(users).filter(users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Usuario no encontrado.")
    
    if user.user_id != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permisos para actualizar este usuario.")
    
    if usuario.nombre != None:
       user.nombre = usuario.nombre
    
    if usuario.dni != None:
        usuario_mismo_dni = db.query(users).filter(users.dni == usuario.dni,users.user_id != user_id).first()
        if usuario_mismo_dni:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Ya existe usuario con ese dni.")
        user.dni = usuario.dni
    db.commit()
    db.refresh(user)
    return user


#AUTH y JWT
@router.post("/login")
async def login(form : Annotated[OAuth2PasswordRequestForm, Depends()],db : Annotated[Session,Depends(get_db)]):
    usuario = db.query(users).filter(users.dni == int(form.username)).first()
    if not usuario or not verify(form.password,usuario.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Credenciales inválidas")
    
    return {"access_token" : crear_token(data = {"sub" : str(usuario.user_id)}),"token_type" : "bearer"}
    