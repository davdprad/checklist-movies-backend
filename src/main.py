from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

base_url = 'https://api.themoviedb.org/3/search/movie'
base_url_id = 'https://api.themoviedb.org/3/movie'

api_key = '01faa49e3ab1fe3b79aba033317dfb4b'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/movie-data")
async def get_movies(movie: str):
    response = requests.get(f'{base_url}?api_key={api_key}&language=pt-BR&query={movie}')
    data = response.json()

    return data['results']

movie_list = []

class Movie(BaseModel):
    id: int

@app.post("/add-movie")
async def add_movie(movie: Movie):
    if any(m["id"] == movie.id for m in movie_list):
        raise HTTPException(
            status_code=400,
            detail="Filme já está na lista."
        )
    
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie.id}?api_key={api_key}&language=pt-BR')
    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Filme não encontrado."
        )
    
    movie_data = response.json()

    movie_list.append({
        "id": movie_data["id"],
        "title": movie_data["title"],
        "release_date": movie_data.get("release_date", "Data não disponível"),
        "poster_path": movie_data.get("poster_path", ""),
        "description": movie_data.get("overview", "Descrição não disponível")
    })

    return {"message": "Filme adicionado com sucesso!", "movie_list": movie_list}

@app.get("/movies")
async def get_my_movies():
    return {"movies": movie_list}