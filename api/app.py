from json import dumps
from marshmallow import fields, Schema
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from json import loads
import datetime

tank = []
id = 0
global data_object 
data_object = {}
global tanklevel_obj
tanklevel_obj = {}

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://iamonfire11:justine123@cluster0.cunrk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)

class Tank_Schema(Schema):
    location = fields.String(required=True)
    full = fields.Integer(required=True)
    lat = fields.Float(required=True)
    long = fields.Float(required=True)

#CREATE TANK
@app.route("/data", methods=["POST"])
def post_d():
    new_tank = Tank_Schema().load(request.json)  #request dictionary
    tank_document = mongo.db.tankscollection.insert_one(new_tank)
    tank_id = tank_document.inserted_id
    findtank = mongo.db.tankscollection.find_one({"_id": tank_id})
    return loads(dumps(findtank))
   

#READ TANK
@app.route("/data",methods = ["GET"])
def get_data():
    tankscollection = mongo.db.tankscollection.find()
    tanks_list = loads(dumps(tankscollection))
    return jsonify(tanks_list)

#UPDATE TANK
@app.route("/data/<ObjectId:id>", methods = ["PATCH"])
def update_tanks(id):
    mongo.db.tankscollection.update_one({"_id": id}, {"$set": request.json})
    findtank = mongo.db.tankscollection.find_one(id)
    tank_json = loads(dumps(findtank))
    return jsonify(tank_json)


#DELETE TANK
@app.route("/data/<ObjectId:id>", methods=["DELETE"])
def delete_tank(id):
  result = mongo.db.tankscollection.delete_one({"_id": id})
  if result.deleted_count == 1:
    return {
      "success": True
    }
  else:
    return {
      "success": False
    }, 400

class tank_level(Schema):
	tank_id = fields.String(required=True)
	water_level=fields.Integer(required=True)

@app.route("/tank",methods=["POST"])
def stat():
    ledstatus = False

    new_tank = tank_level().load(request.json)  #request dictionary
    tank_document = mongo.db.tank_level.insert_one(new_tank)
    tank_id = tank_document.inserted_id
    tank = mongo.db.tank_level.find_one({"_id": tank_id})
    tank_json = loads(dumps(tank))
    if tank_json["water_level"] in range(80,101):
        ledstatus=True
    tanklevel_obj={
	"led": ledstatus,
	"msg": "data saved in database successfully",
	"date": str(datetime.now()),
    }
    return jsonify(tanklevel_obj)


if __name__ == "__main__":
    app.run(debug = True, port = 3000, host = "0.0.0.0")