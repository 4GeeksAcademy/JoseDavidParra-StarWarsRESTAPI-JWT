from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorite',backref='user',lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(250),unique = True,nullable=False)
    rotation_period = db.Column(db.Integer,nullable=True)
    orbital_period = db.Column(db.Integer,nullable=True)
    diameter = db.Column(db.Integer,nullable=True)
    climate = db.Column(db.String(250),nullable=True)
    gravity = db.Column(db.String(250),nullable=True)
    terrain = db.Column(db.String(250),nullable=True)
    surface_water = db.Column(db.String(250),nullable=True)
    population = db.Column(db.BigInteger,nullable=True)
    favorite_of = db.relationship('Favorite',backref='planet',lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(250),unique = True,nullable=False)
    height = db.Column(db.Integer,nullable=True)
    mass = db.Column(db.Integer,nullable=True)
    hair_color = db.Column(db.String(250),nullable=True)
    skin_color = db.Column(db.String(250),nullable=True)
    eye_color = db.Column(db.String(250),nullable=True)
    birth_year = db.Column(db.String(250),nullable=True)
    gender = db.Column(db.String(250),nullable=True)
    favorite_of = db.relationship('Favorite',backref='character',lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            # do not serialize the password, its a security breach
        }

class Favorite(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)
    character_id = db.Column(db.Integer,db.ForeignKey('character.id'),nullable = True)
    planet_id = db.Column(db.Integer,db.ForeignKey('planet.id'),nullable = True)

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "user_id": self.user_id
            # do not serialize the password, its a security breach
        }