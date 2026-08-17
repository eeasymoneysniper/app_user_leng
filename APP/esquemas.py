from pydantic import BaseModel


class usuario_response(BaseModel):
    user_id : int
    nombre : str
    dni : int 
    
class usuario_post(BaseModel):
    nombre : str 
    dni : int
    password : str
    
class usuario_update(BaseModel): 
    nombre : str | None = None
    dni : int | None = None
        
    
class leng_post(BaseModel):
    lenguaje : str

class leng_response(BaseModel):
    leng_id : int
    usuario_id : int
    lenguajes : str
    
class leng_put(BaseModel):
    lenguajes : str | None = None
    