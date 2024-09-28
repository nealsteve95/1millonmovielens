from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymssql
import os
import math 

app = FastAPI()

SQL_SERVER_HOST = os.getenv("SQL_SERVER_HOST", "192.168.0.6")
DATABASE_NAME = os.getenv("DATABASE_NAME", "MovieLens")
USERNAME = os.getenv("USERNAME", "SA")
PASSWORD = os.getenv("PASSWORD", "YourStrong@Passw0rd")

@app.get("/")
def read_root():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
        tables = cursor.fetchall()
        conn.close()
        return {"tables": [table[0] for table in tables]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tables: {e}")

def get_db_connection():
    try:
        conn = pymssql.connect(
            server=SQL_SERVER_HOST,
            user=USERNAME,
            password=PASSWORD,
            database=DATABASE_NAME,
            port=1433
        )
        return conn
    except pymssql.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

class Rating(BaseModel):
    user_id: int
    movie_id: int
    rating: float
    
@app.post("/recommendations/")
def get_recommendations(ratings: list[Rating]):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener ratings de la base de datos
        cursor.execute("SELECT UserID, MovieID, Rating FROM Ratings")
        db_ratings = cursor.fetchall()
        
        # Obtener títulos y géneros de las películas
        cursor.execute("SELECT MovieID, Title, Genres FROM Movies")  # Modificado a Genres
        movies = cursor.fetchall()
        
        conn.close()
        
        # Crear diccionarios para ratings y movies
        db_ratings_dict = {}
        for user_id, movie_id, rating in db_ratings:
            if user_id not in db_ratings_dict:
                db_ratings_dict[user_id] = {}
            db_ratings_dict[user_id][movie_id] = rating
        
        movies_dict = {movie_id: {"title": title, "genres": genres} for movie_id, title, genres in movies}

        # Calcular similitudes utilizando solo la distancia Euclidiana
        recommendations = []
        for user_id, user_ratings in db_ratings_dict.items():
            euclidean_distance, similar_ratings = calculate_euclidean_distance(ratings, user_ratings)
            for movie_id, rating in similar_ratings:
                if movie_id in movies_dict:  # Verificar si la película existe
                    recommendations.append({
                        "user_id": user_id,
                        "movie_id": movie_id,
                        "title": movies_dict[movie_id]["title"],
                        "genres": movies_dict[movie_id]["genres"]  # Cambiado a genres
                    })
        
        # Retornar las 10 mejores recomendaciones basadas en similitud
        recommendations = sorted(recommendations, key=lambda x: x['user_id'])[:10]  # Por simplicidad, aquí solo se está limitando por UserID
        return {"recommendations": recommendations}  # Top 10 recomendaciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recommendations: {e}")

def calculate_euclidean_distance(ratings, user_ratings):
    distance = 0
    similar_ratings = []
    for rating in ratings:
        if rating.movie_id in user_ratings:
            distance += (rating.rating - user_ratings[rating.movie_id]) ** 2
            similar_ratings.append((rating.movie_id, user_ratings[rating.movie_id]))  # Guardamos el MovieID y Rating
    return math.sqrt(distance), similar_ratings






