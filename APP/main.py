from fastapi import FastAPI
from APP.routers import usuarios,lenguajes,auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(usuarios.router)
app.include_router(lenguajes.router)
app.include_router(auth.router)
