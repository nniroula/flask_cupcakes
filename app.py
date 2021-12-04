from flask import Flask, render_template, jsonify
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
@app.route('/api/cupcakes/<int:cupcake_id>')
def get_data_about_single_cupcake(cupcake_id):
    singleCupCake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(singleCupCake.to_dict()) 


"""

Part Two: Listing, Getting & Creating Cupcakes
Make routes for the following:




POST /api/cupcakes
Create a cupcake with flavor, size, rating and image data from the body of the request.

Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.

Test that these routes work in Insomnia.

We’ve provided tests for these three routes; these test should pass if the routes work properly.

You can run our tests like:

"""





