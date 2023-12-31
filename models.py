# Import SQLAlchemy from flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt
import os
from werkzeug.utils import secure_filename


# Initialize our db
db = SQLAlchemy()

bcrypt = Bcrypt()


class Pet(db.Model, SerializerMixin):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ("-meetups.user", "-_password_hash")

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    email = db.Column(db.String)
    profile_pic = db.Column(db.String)

    meetups = db.relationship("Meetup", backref="user")

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))

    def __repr__(self):
        return f"<User {self.username}>"


class Meetup(db.Model, SerializerMixin):
    __tablename__ = "meetups"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

# small change
