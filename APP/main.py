from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from APP.routers import usuarios, lenguajes, auth

app = FastAPI()

# Habilitar CORS (ajusta allow_origins en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers existentes
app.include_router(usuarios.router)
app.include_router(lenguajes.router)
app.include_router(auth.router)

# Servir frontend estático desde la carpeta 'frontend'
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
