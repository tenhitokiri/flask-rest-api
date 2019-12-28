from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# seguir en

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

# Init db
db = SQLAlchemy(app)

# init Marshmallow
ma = Marshmallow(app)

# Product Class/Model


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# Product Schema


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')


# Init Schema
product_schema = ProductSchema()
#product_schema = ProductSchema(strict=True)
#products_schema = ProductSchema(many=True, strict=True)
products_schema = ProductSchema(many=True)

# ------------- End points ------------------------

# Create a Product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Get all Products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Get ONE Product
@app.route('/product/<int:id>', methods=['GET'])
def get_one_product(id):
    one_product = Product.query.get(id)
    return product_schema.jsonify(one_product)

# Update a Product
@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    one_product = Product.query.get(id)
    one_product.name = request.json['name']
    one_product.description = request.json['description']
    one_product.price = request.json['price']
    one_product.qty = request.json['qty']
    db.session.commit()

    return product_schema.jsonify(one_product)

# Delete ONE Product
@app.route('/product/<int:id>', methods=['DELETE'])
def delete_one_product(id):
    one_product = Product.query.get(id)
    db.session.delete(one_product)
    db.session.commit()
    return product_schema.jsonify(one_product)


# run server
if __name__ == '__main__':
    app.run(debug=True)
