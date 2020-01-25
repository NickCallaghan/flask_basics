from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


# Fake Data Generator
from faker import Faker
from faker.providers import internet
fake = Faker()
fake.add_provider(internet)


def make_fake_people(num):
    people = []
    for i in range(num):
        person = {}
        person['name'] = fake.name()
        person['ipv4_address'] = fake.ipv4_public()
        person['email'] = fake.email()
        people.append(person)
    return people


# Init Flask
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initalise marshmallow
ma = Marshmallow(app)


# Person Class/Model
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    ipv4_addr = db.Column(db.String(15))
    age = db.Column(db.Integer)

    def __init__(self, name, email, ipv4_addr, age):
        self.name = name
        self.email = email
        self.ipv4_addr = ipv4_addr
        self.age = age


# Person Schema
class PersonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'ipv4_addr', 'age')


# Init Schema
person_schema = PersonSchema()
persons_schema = PersonSchema(many=True)


# Run Server
@app.route("/")
def index():
    people = make_fake_people(10)
    return jsonify(people)


if __name__ == "__main__":
    app.run(debug=True)
