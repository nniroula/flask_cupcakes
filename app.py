from ctypes import sizeof
from flask import Flask, render_template, jsonify, request
from flask.templating import render_template_string
from models import Cupcake, connect_db, db


app = Flask(__name__)

# call connect_db function here
connect_db(app)

app.config['SECRET_KEY'] = "nokeyherebuddy"  # needs to run debugger, flash and much more
# app.config['DEBUG_TB-INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Flask_Cupcake_db'    # point to your datatbase

app.config['SQLALCHEMY_ECHO'] = True    # prints sql statements to terminal
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False      # suppress sqlalchemy yelling at you

@app.route('/')
def home_page():
    return "<small> Fun Project </small>"

# GET /api/cupcakes
# Get data about all cupcakes.
# Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.
# The values should come from each cupcake instance.
@app.route('/api/cupcakes')
def list_all_cupcakes():
    cc = Cupcake.query.all()  # this gives query object
    # cupcakes = [item.Cupcake.to_dict() for item in cc ]
    cupcakes = [item.to_dict() for item in cc]
    return jsonify(cupcakes = cupcakes)  

# GET /api/cupcakes/[cupcake-id]
# Get data about a single cupcake.
# Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
# This should raise a 404 if the cupcake cannot be found.
@app.route('/api/cupcakes/<int:cupcake_id>')    # Not complete for 404 message(I believe)
def get_data_about_single_cupcake(cupcake_id):
    singleCupCake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(singleCupCake.to_dict()) 

# POST /api/cupcakes
# Create a cupcake with flavor, size, rating and image data from the body of the request.
# Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
@app.route('/api/cupcakes', methods = ["POST"])   # Error in insomnia is TypeError: 'NoneType' object is not callable
def create_cupcake():
    data = request.json()
    # jsonflavor = request.json["flavor"]
    # jsonSize = request.json["size"]
    # jsonRating = request.json["rating"]
    # jsonImage = request.json["image"]
    # new_cupcake = Cupcake(flavor = jsonflavor, size = jsonSize, rating = jsonRating, image = jsonImage or None)
    new_cupcake = Cupcake(flavor = data['flavor'], size = data['size'], rating = data['rating'], image = data['image'] or None)

    db.session.add(new_cupcake)
    db.session.commit()
    json_response = jsonify(new_cupcake.to_dict()) 
    return (json_response, 201)


# Test these routes in Insomnia.
# tests do not work yet.


# PATCH /api/cupcakes/[cupcake-id]
# Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request. You can always assume that the entire cupcake object will be passed to the backend.
# This should raise a 404 if the cupcake cannot be found.
# Respond with JSON of the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating, image}}.

@app.route('/api/cupcakes/<int:cupcake_id>', methods = ["PATCH"])    # PATCH route
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    # up that cupcake
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.size('size', cupcake.size)
    cupcake.rating = request.rating('rating', cupcake.rating)
    cupcake.image = request.image('image', cupcake.image) 
    db.session.commit()
    return jsonify(cupcake= cupcake.to_dict())

# DELETE /api/cupcakes/[cupcake-id]
# This should raise a 404 if the cupcake cannot be found.
# Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}.
@app.route('api/cupcakes/<int:cupcake_id>', methods = ['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message = 'deleted')




