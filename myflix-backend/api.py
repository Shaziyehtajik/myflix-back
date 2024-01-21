from flask import Blueprint, request, jsonify, make_response, current_app
from flask_cors import cross_origin
from .sqlbd import register_user, authenticate_user, update_user_profile
from .mongodb import (
    create_movie,
    update_movie,
    delete_movie,
    get_movie_by_id,
    get_all_movies,
    get_movie,
    get_genres,
)
from .sqldb import verify, create
from .stream import initiate_stream

api_page = Blueprint('api', __name__)

# User Management

@api_page.route('/register', methods=['POST'])
@cross_origin()
def register():
    data = request.json
    result = register_user(data['username'], data['password'])
    return jsonify({"success": result}), 201 if result else 400

@api_page.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json
    token = authenticate_user(data['username'], data['password'])
    return jsonify({"token": token}) if token else jsonify({"error": "Invalid credentials"}), 200

@api_page.route('/profile', methods=['PUT'])
@cross_origin()
def update_profile():
    data = request.json
    success = update_user_profile(data['username'], data['new_password'])
    return jsonify({"success": success}), 200 if success else 400

# Movie Management

@api_page.route('/movies', methods=['GET', 'POST'])
@cross_origin()
def manage_movies():
    if request.method == 'GET':
        response = get_all_movies()
    elif request.method == 'POST':
        data = request.json
        response = create_movie(data)
    return jsonify(response)

@api_page.route('/movies/<movie_id>', methods=['PUT', 'DELETE'])
@cross_origin()
def update_delete_movie(movie_id):
    if request.method == 'PUT':
        data = request.json
        response = update_movie(movie_id, data)
    elif request.method == 'DELETE':
        response = delete_movie(movie_id)
    return jsonify(response)

# Additional Routes

@api_page.route('/genres', methods=['GET'])
@cross_origin()
def api_get_genres():
    response = get_genres()
    return jsonify(response)

@api_page.route('/verify', methods=['POST'])
@cross_origin()
def verification():
    username = request.json['username']
    password = request.json['password']
    if verify(username, password):
        return {"token": username}, 200
    else:
        return {"token": "error"}, 200

@api_page.route('/create', methods=['POST'])
@cross_origin()
def api_create_account():
    username = request.json['username']
    password = request.json['password']
    if create(username, password):
        return {"result": True}, 200
    else:
        return {"result": False}, 200

@api_page.route('/stream', methods=['POST'])
@cross_origin()
def start_stream():
    filename = request.json['filename']
    response = initiate_stream(filename)
    if response == "success":
        return '', 200
    if response == "error":
        return '', 404

@api_page.route('/health')
def health():
    return '', 200

@api_page.route('/ready')
def ready():
    return '', 200
