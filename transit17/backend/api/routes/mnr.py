from flask import Blueprint, jsonify
from backend.services.mta import MTAServiceFactory

bp = Blueprint('mnr', __name__, url_prefix='/api/mnr')

@bp.route('/realtime')
def get_realtime_data():
    """get MNR real-time data"""
    try:
        service = MTAServiceFactory.get_service('mnr')
        data = service.get_realtime_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/feed')
def get_feed():
    """get MNR GTFS data"""
    try:
        service = MTAServiceFactory.get_service('mnr')
        feed = service.get_feed()
        return jsonify(feed)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 