# Arquivo: main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.api_movie import api_router
from routers.my_list import my_list_router
from routers.watched_list import watched_list_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://nossacinemateca.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de roteadores
app.include_router(api_router, prefix="/api", tags=["Filmes da API"])
app.include_router(my_list_router, prefix="/my-list", tags=["Lista de Pendentes"])
app.include_router(watched_list_router, prefix="/watched-list", tags=["Lista de Assistidos"])
