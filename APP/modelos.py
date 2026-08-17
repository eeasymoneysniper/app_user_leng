from sqlalchemy import Integer,Column,String,ForeignKey,DateTime,func
from APP.basededatos import Base


class users(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer,nullable=False,primary_key=True,index=True,unique=True)
    nombre = Column(String(100))
    dni = Column(Integer,nullable=False,unique=True)
    password = Column(String(100),nullable=False)
    created_at = Column(DateTime,server_default=func.now())
    
class lenguajes(Base):
    __tablename__ = "lenguajes"
    
    leng_id = Column(Integer,primary_key=True,nullable=False,index=True)
    usuario_id = Column(Integer,ForeignKey("users.user_id"),nullable=False)
    lenguajes = Column(String(100))