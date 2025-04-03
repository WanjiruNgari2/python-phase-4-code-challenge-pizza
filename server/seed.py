#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():
    # Clear existing data
    print("Deleting data...")
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()
    db.session.commit()

    # Create restaurants
    print("Creating restaurants...")
    dominos = Restaurant(name="Domino's")
    pizza_hut = Restaurant(name="Pizza Hut")
    db.session.add_all([dominos, pizza_hut])
    db.session.commit()  # Commit to generate IDs for restaurants

    # Create pizzas
    print("Creating pizzas...")
    pepperoni = Pizza(name="Pepperoni")
    margherita = Pizza(name="Margherita")
    db.session.add_all([pepperoni, margherita])
    db.session.commit()  # Commit to generate IDs for pizzas

    # Link restaurants and pizzas
    print("Creating restaurant-pizza links...")
    rp1 = RestaurantPizza(restaurant_id=dominos.id, pizza_id=pepperoni.id, price=15)
    rp2 = RestaurantPizza(restaurant_id=pizza_hut.id, pizza_id=margherita.id, price=20)
    db.session.add_all([rp1, rp2])
    db.session.commit()

    print("Database seeded successfully!")
