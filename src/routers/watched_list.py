from fastapi import HTTPException, APIRouter
from typing import List
import requests
from models import MovieDetailed, MovieBase

# Configurações gerais
base_url = 'https://api.themoviedb.org/3/search/movie'
base_url_id = 'https://api.themoviedb.org/3/movie'
api_key = '01faa49e3ab1fe3b79aba033317dfb4b'

watched_list = []

watched_list_router = APIRouter()

@watched_list_router.get("/watched", response_model=List[MovieDetailed])
async def get_watched_movies():
    return watched_list

@watched_list_router.post("/add-watched", response_model=MovieDetailed)
async def add_watched_movie(movie: MovieBase):
    if any(m.id == movie.id for m in watched_list):
        raise HTTPException(status_code=400, detail="Filme já está na lista de assistidos.")

    response = requests.get(f'{base_url_id}/{movie.id}?api_key={api_key}&language=pt-BR&append_to_response=watch/providers')
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Filme não encontrado.")
    
    providers = response.get("watch/providers", {}).get("results", {}).get("BR", {}).get("flatrate", [])
    platforms = [provider["provider_name"] for provider in providers] if providers else ["Não disponível"]

    movie_data = response.json()
    movie_detailed = MovieDetailed(
        id=movie_data["id"],
        title=movie_data["title"],
        release_date=movie_data.get("release_date", "Data não disponível"),
        poster_path=movie_data.get("poster_path", ""),
        description=movie_data.get("overview", "Descrição não disponível"),
        platforms=platforms
    )
    watched_list.append(movie_detailed)
    return movie_detailed

@watched_list_router.post("/delete-watched")
async def delete_watched_movies(movies: List[MovieBase]):
    for movie in movies:
        movie_to_delete = next((m for m in watched_list if m.id == movie.id), None)
        if not movie_to_delete:
            raise HTTPException(status_code=404, detail=f"Filme com id {movie.id} não encontrado na lista de assistidos.")
        watched_list.remove(movie_to_delete)
    return {"message": "Filmes removidos da lista de assistidos com sucesso!"}
