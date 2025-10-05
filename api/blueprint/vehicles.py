#!/usr/bin/python3

from flask import jsonify, request
from api.blueprint import app_views
from models.vehicle import Vehicle
from models import storage

@app_views.route('/vehicles', strict_slashes=False)
def get_vehicles():
    return jsonify([veh.to_dict() for _, veh in storage.all("Vehicle").items()])

@app_views.route('/vehicle', strict_slashes=False, methods=['POST'])
def create_vehicle():
    if not request.json:
        return jsonify("Not a valid json"), 400
    
    data = request.get_json()
    try:
        model = Vehicle(**data)
        model.save()
    except Exception as e:
        return jsonify(e), 400
    
    return jsonify(model.to_dict())

@app_views.route('/vehicle/<vehicle_id>', strict_slashes=False, methods=["DELETE", "PUT", "GET"])
def get_update_delete_vehicle(vehicle_id):
    if not request.json:
        return jsonify("Not a valid json"), 400
    veh: Vehicle = storage.get("Vehicle", vehicle_id)
    if not veh:
        return jsonify("Vehicle not found"), 404
    
    if request.method == "PUT":
        data = request.get_json()
        try:
            for key, val in data.items():
                setattr(veh, key, val)
        except Exception as e:
            return jsonify(e), 400
        veh.save()
        return jsonify(veh.to_dict()), 200
    elif request.method == "GET":
        return jsonify(veh.to_dict()), 200
    else:
        storage.delete(veh)
        return jsonify({}), 201
    
    
