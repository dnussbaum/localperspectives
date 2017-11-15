from flask import Flask
from flask import jsonify
from flask import request
from extract import *
app = Flask(__name__)

@app.route("/")
def get_articles():
    url = request.args.get('url')
    response = jsonify(get_json(url))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

app.run()
