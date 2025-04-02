from flask import Blueprint, jsonify
from backend.services.mta import MTAServiceFactory

bp = Blueprint('lirr', __name__, url_prefix='/api/lirr')

@bp.route('/realtime')
def get_realtime_data():
    """get LIRR real-time data"""
    try:
        service = MTAServiceFactory.get_service('lirr')
        data = service.get_realtime_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/feed')
def get_feed():
    """get LIRR GTFS data"""
    try:
        service = MTAServiceFactory.get_service('lirr')
        feed = service.get_feed()
        return jsonify(feed)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 