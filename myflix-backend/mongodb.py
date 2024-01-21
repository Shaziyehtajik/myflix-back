import json
from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from bson.json_util import dumps

def get_mongodb():
    if 'mongodb' not in g:
        g.mongodb = PyMongo(current_app).db
    return g.mongodb

# Use LocalProxy to read the global db instance with just `db`
mongodb = LocalProxy(get_mongodb)

# Movie Management

def create_movie(movie_data):
    result = mongodb.movies.insert_one(movie_data)
    return {'success': bool(result.inserted_id)}

def update_movie(movie_id, updated_data):
    result = mongodb.movies.update_one({'_id': movie_id}, {'$set': updated_data})
    return {'success': bool(result.modified_count)}

def delete_movie(movie_id):
    result = mongodb.movies.delete_one({'_id': movie_id})
    return {'success': bool(result.deleted_count)}

# Retrieve a specific movie by its ID
def get_movie_by_id(movie_id):
    movie = mongodb.movies.find_one({'_id': movie_id})
    return movie

# Retrieve all movies
def get_all_movies():
    movies = list(mongodb.movies.find())
    return movies

# Additional movie functions (if needed)

# Genre Management

def get_movie_by_genre(genre):
    movies = list(mongodb.movies.find({'genre': genre}))
    return json_response(movies)

def get_all_genres():
    genres = list(mongodb.genres.find())
    return json_response(genres)

# Helper function for JSON response
def json_response(payload, status=200):
    return (dumps(payload), status, {'content-type': 'application/json'})
