from flask import Blueprint, jsonify
from backend.services.mta import MTAServiceFactory

bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')

@bp.route('/subway')
def get_subway_alerts():
    """get subway line alerts"""
    try:
        service = MTAServiceFactory.get_service('subway')
        alerts = service.get_alerts()
        return jsonify(alerts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/lirr')
def get_lirr_alerts():
    """get LIRR alerts"""
    try:
        service = MTAServiceFactory.get_service('lirr')
        alerts = service.get_alerts()
        return jsonify(alerts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/mnr')
def get_mnr_alerts():
    """get MNR alerts"""
    try:
        service = MTAServiceFactory.get_service('mnr')
        alerts = service.get_alerts()
        return jsonify(alerts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/all')
def get_all_alerts():
    """get all traffic system alerts"""
    try:
        alerts = {}
        for service_type in ['subway', 'lirr', 'mnr']:
            service = MTAServiceFactory.get_service(service_type)
            alerts[service_type] = service.get_alerts()
        return jsonify(alerts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 