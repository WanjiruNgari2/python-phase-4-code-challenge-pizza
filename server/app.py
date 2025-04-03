#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
import os
from sqlalchemy.orm import Session

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)  # Ensure the db object is initialized with the app
migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# filepath: c:\Users\DAMAH\Desktop\moringa\flask phase4\pizza challenge\Phase-4-Code-Challenge-Pizzas-062023\code-challenge\server\app.py

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return [restaurant.to_dict_basic() for restaurant in restaurants], 200

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    with db.session() as session:
        restaurant = session.get(Restaurant, id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        return restaurant.to_dict(), 200

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant_by_id(id):
    with db.session() as session:
        restaurant = session.get(Restaurant, id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        session.delete(restaurant)
        session.commit()
        return '', 204

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return [pizza.to_dict() for pizza in pizzas], 200

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    # Validate required fields
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    if price is None or pizza_id is None or restaurant_id is None:
        return {"errors": ["validation errors"]}, 400

    try:
        # Create a new RestaurantPizza
        restaurant_pizza = RestaurantPizza(
            price=price,
            pizza_id=pizza_id,
            restaurant_id=restaurant_id
        )
        db.session.add(restaurant_pizza)
        db.session.commit()

        return restaurant_pizza.to_dict(), 201
    except ValueError as e:
        return {"errors": ["validation errors"]}, 400
