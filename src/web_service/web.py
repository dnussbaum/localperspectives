from flask import Flask
from flask import jsonify
from flask import request
from extract import *
app = Flask(__name__)

@app.route("/locations")
def locations():
    url = request.args.get('url')
    response = jsonify(get_locations(url))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/")
def articles():
    url = request.args.get('url')
    location = request.args.get('location')
    response = jsonify(get_articles(url,location))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


app.run()
