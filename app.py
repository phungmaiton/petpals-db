from flask import Flask, make_response, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound
from models import db, Pet, User, Meetup
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from geopy.geocoders import Nominatim

app = Flask(__name__)
CORS(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///petpals.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False  # configures JSON responses to print on indented lines
app.secret_key = (
    b"\xda\xac|D\xb4\xed\t\xffK\xd1\xbe\x1dg\xf4\x16\xc1j\xb3\x95N+\xf8x\x9e"
)

geolocator = Nominatim(user_agent="petpals")

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
# Views go here!


class ClearSession(Resource):
    def delete(self):
        session["page_views"] = None
        session["user_id"] = None

        return {}, 204


api.add_resource(ClearSession, "/clear", endpoint="clear")


class Signup(Resource):
    def post(self):
        request_json = request.get_json()
        username = request_json["username"]
        password = request_json["password"]
        profile_pic = request_json["profile_pic"]
        email = request_json["email"]

        new_user = User(username=username, profile_pic=profile_pic, email=email)
        new_user.password_hash = password
        try:
            db.session.add(new_user)
            db.session.commit()
            session["user_id"] = new_user.id

            return new_user.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            return {"error": "Username already exists"}, 422


api.add_resource(Signup, "/signup", endpoint="signup")


class Login(Resource):
    def post(self):
        request_json = request.get_json()
        username = request_json["username"]
        user = User.query.filter(User.username == username).first()
        password = request_json["password"]

        if user:
            if user.authenticate(password):
                session["user_id"] = user.id
                return user.to_dict(), 200

        return {"error": "Invalid username or password"}, 401


api.add_resource(Login, "/login", endpoint="login")


class Logout(Resource):
    def delete(self):
        if session.get("user_id"):
            session["user_id"] = None

            return {}, 204

        return {"error": "401 Unauthorized"}, 401


api.add_resource(Logout, "/logout", endpoint="logout")


class CheckSession(Resource):
    def get(self):
        if session.get("user_id"):
            user = User.query.filter(User.id == session["user_id"]).first()
            return user.to_dict(), 200

        return {"error": "401 Unauthorized"}, 401


api.add_resource(CheckSession, "/check_session", endpoint="check_session")


class Meetups(Resource):
    def post(self):
        request_json = request.get_json()

        street_address = request_json["street_address"]
        city = request_json["city"]
        state = request_json["state"]
        country = request_json["country"]

        address = f"{street_address}, {city}, {state}, {country}"

        geolocator = Nominatim(user_agent="your_app_name")
        location = geolocator.geocode(address)

        if location is None:
            return {"error": "Invalid address."}, 400

        longitude = location.longitude
        latitude = location.latitude

        meetup = Meetup(
            user_id=session["user_id"],
            pet_id=request_json["pet_id"],
            venue=request_json["venue"],
            street_address=street_address,
            city=city,
            state=state,
            country=country,
            longitude=longitude,
            latitude=latitude,
        )
        db.session.add(meetup)
        db.session.commit()
        return {"message": "Meetup created successfully."}, 201


api.add_resource(Meetups, "/meetups")

class Pets(Resource):
    
    def get(self):
        pets = [pet.to_dict(rules=("-meetups",)) for pet in Pet.query.all()]

        return make_response(pets, 200)
    
    def post(self):
        request_json = request.get_json()

        pet = Pet(
            owner_id=session["owner_id"],
            name=request_json["name"],
            birth_year=request_json["birth_year"],
            species=request_json["species"],
            breed=request_json["breed"],
            profile_pic=request_json["profile_pic"],
            city=request_json["city"],
            state=request_json["state"],
            country=request_json["country"],
            availability=request_json["availability"],
        )
        db.session.add(pet)
        db.session.commit()
        return make_response(
            pet.to_dict(rules=("-meetups",)),
            201
        )
    
api.add_resource(Pets, "/pets")

if __name__ == "__main__":
    app.run(port=5555, debug=True)

#test