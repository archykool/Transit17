from flask import jsonify
from requests.exceptions import RequestException
from google.protobuf.message import DecodeError

class MTAError(Exception):
    """Base exception for MTA API errors"""
    pass

class MTAConnectionError(MTAError):
    """Raised when there's a connection error with MTA API"""
    pass

class MTADataError(MTAError):
    """Raised when there's an error in the data received from MTA API"""
    pass

def handle_mta_error(error):
    """Handle MTA API related errors"""
    if isinstance(error, MTAConnectionError):
        return jsonify({
            "error": "Connection error with MTA API",
            "details": str(error)
        }), 503
    elif isinstance(error, MTADataError):
        return jsonify({
            "error": "Invalid data received from MTA API",
            "details": str(error)
        }), 422
    elif isinstance(error, MTAError):
        return jsonify({
            "error": "MTA API error",
            "details": str(error)
        }), 500
    else:
        return jsonify({
            "error": "Internal server error",
            "details": str(error)
        }), 500

def validate_vehicle_position(vehicle):
    """Validate vehicle position data and return position status"""
    if not vehicle.position:
        return {
            'is_valid': False,
            'status': 'missing_position',
            'message': 'Position data is missing'
        }
    
    if vehicle.position.latitude == 0 and vehicle.position.longitude == 0:
        return {
            'is_valid': True,
            'status': 'position_unknown',
            'message': 'Position coordinates are not available'
        }
    
    return {
        'is_valid': True,
        'status': 'position_available',
        'message': None
    } 