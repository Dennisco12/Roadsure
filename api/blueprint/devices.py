#!/usr/bin/python3

from flask import jsonify, request
from api.blueprint import app_views
from models.device import Device
from models.vehicle import Vehicle
from models import storage


@app_views.route('/signal/status', strict_slashes=False, methods=['POST'])
def send_status():
    if not request.json:
        return jsonify('Not a valid json'), 400
    
    data = request.get_json()
    if "device_id" not in data:
        return jsonify("Please include a valid device_id"), 400
    
    device: Device = storage.get("Device", data['device_id'])
    if not device:
        return jsonify("Device not found"), 404
    
    vehicle: Vehicle = storage.get("Vehicle", device.vehicle_id)
    if not vehicle:
        return jsonify("Vehicle not found"), 404
    
    # Action!!!
    
    return jsonify("status sent!"), 200

@app_views.route('/signal/location' ,strict_slashes=False, methods=['POST'])
def send_location():
    if not request.json:
        return jsonify("Not a valid json"), 400
    
    data = request.get_json()
    if "device_id" not in data:
        return jsonify("Please include a valid device_id"), 404
    
    device: Device = storage.get("Device", data['device_id'])
    if not device:
        return jsonify("Device not found"), 404
    
    vehicle: Vehicle = storage.get("Vehicle", device.vehicle_id)
    if not vehicle:
        return jsonify("Vehicle not found"), 404
    
    location = data.get('location')
    if not location or not location.get('long') or not location.get('lat'):
        return jsonify("Please include location in proper format"), 400
    
    loc_info = {
        'longitude': location['longitude'], 
        'latitude': location['latitude']
        }
    
    setattr(vehicle, location, loc_info)
    return jsonify("Location recieved"), 200

