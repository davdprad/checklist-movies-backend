from fastapi import HTTPException, APIRouter
from typing import List
import requests
from models import Movie, MovieDetailed, Platform

# General settings
base_url = 'https://api.themoviedb.org/3/search/movie'
base_url_id = 'https://api.themoviedb.org/3/movie'
api_key = '01faa49e3ab1fe3b79aba033317dfb4b'

# Router
api_router = APIRouter()

# Route to fetch movie list
@api_router.get("/movie-list", response_model=List[Movie])
async def get_movies(movie: str):
    search_response = requests.get(f'{base_url}?api_key={api_key}&language=pt-BR&query={movie}')
    search_data = search_response.json()
    
    if 'results' not in search_data or not search_data['results']:
        raise HTTPException(status_code=404, detail="Movies not found.")
    
    detailed_movies = []
    for item in search_data["results"]:
        movie_detailed = Movie(
            id=item["id"],
            title=item["title"],
            release_date=item.get("release_date", "Data not available."),
            description=item.get("overview", "Description not available."),
            poster_path=item.get("poster_path") or "",
        )
        detailed_movies.append(movie_detailed)

    return detailed_movies

# Route to fetch detailed movie data
@api_router.get("/movie-data", response_model=MovieDetailed)
async def movie_data(movie_id: int):
    details_response = requests.get(f'{base_url_id}/{movie_id}?api_key={api_key}&language=pt-BR&append_to_response=watch/providers')
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

    return movie_detailed
