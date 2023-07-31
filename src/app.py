"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ----- ENDPOINTS ------ 

@app.route('/users', methods=['GET','POST'])
def get_post_users():
    if request.method == "GET":
        users_query = User.query.all()
        users = list(map(lambda user:user.serialize(),users_query))
        response_body = {
            "msg": "ok",
            "results": users
        }
        return jsonify(response_body), 200
    elif request.method == "POST":
        request_body = request.get_json(force=True)
        user = User(email=request_body["email"],password=request_body["password"],is_active=request_body["is_active"])
        if user is None:
            return jsonify({"msg":"User no puede ser null"}),400
        if "email" not in request_body:
            return jsonify({"msg":"email no puede estar vacio"}),400
        if "password" not in request_body:
            return jsonify({"msg":"password no puede estar vacio"}),400
        db.session.add(user)
        db.session.commit()
        response_body = {
            "msg" : "ok - User created"
        }
        return jsonify(response_body), 200

@app.route('/users/<int:user_id>', methods=['GET','DELETE'])
def get_delete_one_user(user_id):
    user_query = User.query.filter_by(id=user_id).first()

    if user_query is None:
        return jsonify({"msg" : "User not found"}),404

    elif request.method == "GET":
        response_body = {
            "msg": "ok",
            "result" : user_query.serialize()
        }
        return jsonify(response_body), 200
    
    elif request.method == "DELETE":
        response_body = {
            "msg": "ok - User deleted"
        }
        db.session.delete(user_query)
        db.session.commit()
        return jsonify(response_body), 200

@app.route('/characters', methods=['GET','POST'])
def get_post_characters():
    if request.method == "GET":
        characters_query = Character.query.all()
        characters = list(map(lambda character:character.serialize(),characters_query))
        response_body = {
            "msg": "ok",
            "results": characters
        }
        return jsonify(response_body), 200
    
    elif request.method == "POST":
        request_body = request.get_json(force=True)
        character = Character(name=request_body["name"],height=request_body["height"],mass=request_body["mass"],hair_color=request_body["hair_color"],skin_color=request_body["skin_color"],eye_color=request_body["eye_color"],birth_year=request_body["birth_year"],gender=request_body["gender"])
        if character is None:
            return jsonify({"msg":"Character no puede ser null"}),400
        if "name" not in request_body:
            return jsonify({"msg":"name no puede ser null"}),400
        db.session.add(character)
        db.session.commit()
        response_body = {
            "msg" : "ok - Character created"
        }
        return jsonify(response_body), 200

@app.route('/characters/<int:character_id>', methods=['GET','DELETE'])
def get_delete_one_character(character_id):
    character_query = Character.query.filter_by(id=character_id).first()

    if character_query is None:
        return jsonify({"msg" : "Character not found"}),404

    elif request.method == "GET":
        response_body = {
            "msg": "ok",
            "result" : character_query.serialize()
        }
        return jsonify(response_body), 200
    
    elif request.method == "DELETE":
        response_body = {
            "msg": "ok - Character deleted"
        }
        db.session.delete(character_query)
        db.session.commit()
        return jsonify(response_body), 200

@app.route('/planets', methods=['GET','POST'])
def get_post_planets():
    if request.method == "GET":
        planets_query = Planet.query.all()
        planets = list(map(lambda planet:planet.serialize(),planets_query))
        response_body = {
            "msg": "ok",
            "results": planets
        }
        return jsonify(response_body), 200

    elif request.method == "POST":
        request_body = request.get_json(force=True)
        planet = Planet(name=request_body["name"],rotation_period=request_body["rotation_period"],orbital_period=request_body["orbital_period"],diameter=request_body["diameter"],climate=request_body["climate"],gravity=request_body["gravity"],terrain=request_body["terrain"],surface_water=request_body["surface_water"],population=request_body["population"])
        if planet is None:
            return jsonify({"msg":"Planet cannot be null"})
        if "name" not in request_body:
            return jsonify({"msg":"name cannot be null"}),404
        db.session.add(planet)
        db.session.commit()
        response_body = {
            "msg" : "ok - Planet created"
        }
        return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET','DELETE'])
def get_delete_one_planet(planet_id):
    planet_query = Planet.query.filter_by(id=planet_id).first()

    if planet_query is None:
        return jsonify({"msg" : "Planet not found"}),404

    elif request.method == "GET":
        response_body = {
            "msg": "ok",
            "result" : planet_query.serialize()
        }
        return jsonify(response_body), 200
    
    elif request.method == "DELETE":
        response_body = {
            "msg": "ok - Planet deleted"
        }
        favorites_query = Favorite
        db.session.delete(planet_query)
        db.session.commit()
        return jsonify(response_body), 200

@app.route('/favorites', methods=['GET','POST'])
def get_post_favorites():
    if request.method == "GET":
        favorites_query = Favorite.query.all()
        favorites = list(map(lambda favorite:favorite.serialize(),favorites_query))
        response_body = {
            "msg": "ok",
            "results": favorites
        }
        return jsonify(response_body), 200
    
    elif request.method == "POST":
        request_body = request.get_json(force=True)
        exists = Favorite.query.filter_by(user_id=request_body["user_id"],character_id=request_body["character_id"],planet_id=request_body["planet_id"]).first()
        if exists != None:
            return jsonify({"msg":"Already exists"}),400
        favorite = Favorite(user_id=request_body["user_id"],character_id=request_body["character_id"],planet_id=request_body["planet_id"])
        if favorite.user_id is None:
            return jsonify({"msg":"No user was selected"}),400
        if favorite.character_id is None and favorite.planet_id is None:
            return jsonify({"msg":"No character or planet was selected"}),400
        if favorite.character_id is not None and favorite.planet_id is not None:
            return jsonify({"msg":"Multiple items selected"}),400
        db.session.add(favorite)
        db.session.commit()
        response_body = {
            "msg" : "ok - Favorite created"
        }
        return jsonify(response_body), 200

@app.route('/favorites/<int:favorite_id>', methods=['GET','DELETE'])
def get_delete_one_favorite(favorite_id):
    favorite_query = Favorite.query.filter_by(id=favorite_id).first()

    if favorite_query is None:
        return jsonify({"msg" : "Favorite not found"}),404

    elif request.method == "GET":
        response_body = {
            "msg": "ok",
            "result" : favorite_query.serialize()
        }
        return jsonify(response_body), 200

    elif request.method == "DELETE":
        response_body = {
            "msg": "ok - Favorite deleted"
        }
        db.session.delete(favorite_query)
        db.session.commit()
        return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
