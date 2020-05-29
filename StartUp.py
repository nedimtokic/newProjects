from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir,"db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init database
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Users model


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    fullname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self,username,fullname,lastname,email):
        self.username = username
        self.fullname = fullname
        self.lastname = lastname
        self.email = email

# Users Schema


class UserSchema(ma.Schema):
    class Meta:
        fields= ("Id,","username","fullname","lastname","email")


# Init schema

user_schema = UserSchema()

users_schema = UserSchema(many=True)

# Create user


@app.route("/user", methods=["POST"])
def add_User():
    username = request.json["username"]
    fullname = request.json["fullname"]
    lastname = request.json["lastname"]
    email = request.json["email"]

    new_user = Users(username,fullname,lastname,email)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route("/allusers", methods=["GET"])
def get_all():
    all_users = Users.query.all()
    result=users_schema.dump(all_users)
    return jsonify(result)


@app.route("/", methods =["GET"])
def home():
   return jsonify({"testmsg":"Hello world!"})

#Run Server
if __name__ == "__main__":
    app.run(debug=True)