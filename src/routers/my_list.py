from fastapi import HTTPException, APIRouter
from typing import List
import requests
from models import MovieDetailed, Platform

# Configurações gerais
base_url = 'https://api.themoviedb.org/3/search/movie'
base_url_id = 'https://api.themoviedb.org/3/movie'
api_key = '01faa49e3ab1fe3b79aba033317dfb4b'

movie_list = []

my_list_router = APIRouter()

@my_list_router.get("/movies", response_model=List[MovieDetailed])
async def get_my_movies():
    return movie_list

@my_list_router.post("/add-movie", response_model=MovieDetailed)
async def add_movie(movie: int):
    if any(m.id == movie for m in movie_list):
        raise HTTPException(status_code=409, detail="Movie is already on the pending list.")

    details_response = requests.get(f'{base_url_id}/{movie}?api_key={api_key}&language=pt-BR&append_to_response=watch/providers')
    if details_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Movie not found.")

    details_data = details_response.json()

    providers = details_data.get("watch/providers", {}).get("results", {}).get("BR", {}).get("flatrate", [])
    platforms = [
        Platform(name=provider["provider_name"], logo_path=provider.get("logo_path", ""))
        for provider in providers
    ] if providers else [Platform(name="Not available.", logo_path="")]

    movie_detailed = MovieDetailed(
        id=details_data["id"],
        title=details_data["title"],
        release_date=details_data.get("release_date", "Data not available."),
        runtime=details_data.get("runtime", 0),
        genres=[genre["name"] for genre in details_data.get("genres", [])],
        description=details_data.get("overview", "Description not available."),
        poster_path=details_data.get("poster_path") or "",
        platforms=platforms
    )

    movie_list.append(movie_detailed)
    return movie_detailed

@my_list_router.post("/delete-movies")
async def delete_movies(movies: List[int]):
    if not movie_list:
        raise HTTPException(status_code=404, detail="Empty to-do list.")
    
    for movie in movies:
        movie_to_delete = next((m for m in movie_list if m.id == movie), None)
        if not movie_to_delete:
            raise HTTPException(status_code=404, detail=f"Movie with id {movie} not found in the pending list.")
        movie_list.remove(movie_to_delete)

    return {"message": "Successfully deleted movie."}
