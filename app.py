from flask import Flask, json, request, jsonify
from flask_cors.decorator import cross_origin
import requests
from flask_cors import CORS
import pymongo

myclient = pymongo.MongoClient("mongodb+srv://winteriscoming:imready@cluster0.hgwcq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = myclient["weather"]
collection = db["users"]

app = Flask(__name__)
CORS(app)
@app.route('/weather', methods = ["POST"])
def get_weather():
    request_data = request.get_json()
    city = request_data["city"]
    API_KEY = "ad7b0364294be37e13f7431b87811a17"
    url = "http://api.openweathermap.org/data/2.5/weather?q={c}&appid={API}&units=metric".format(c = city, API = API_KEY)
    response_data = requests.get(url).json()
    print(response_data["coord"]["lon"])
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&appid={API}&units=metric".format(lat = response_data["coord"]["lat"], lon = response_data["coord"]["lon"], API = API_KEY)
    response_data = requests.get(url).json()
    return response_data

CORS(app)
@app.route("/login", methods = ["POST"])
def login():
    request_data = request.get_json()
    print(request_data)
    username = request_data["username"]
    password = request_data["password"]
    doc = collection.find_one({"username": username})
    if doc["username"] == username and doc["password"] == password:
        return jsonify({"status": True, "name": doc["name"]})
    else:
        return jsonify({"status": False})

@app.route("/register", methods = ["POST"])
def register():
    request_data = request.get_json()
    data = {"name": request_data["name"], "username": request_data["username"], "password": request_data["password"]}
    id = collection.insert_one(data)
    return jsonify({"status": True})



if __name__ == '__main__':
   app.run(debug=False)