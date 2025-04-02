from flask import Blueprint, jsonify
from backend.services.mta import MTAServiceFactory

bp = Blueprint('subway', __name__, url_prefix='/api/subway')

@bp.route('/status')
def get_status():
    """get all subway line statuses"""
    try:
        service = MTAServiceFactory.get_service('subway')
        statuses = service.get_all_line_statuses()
        return jsonify(statuses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/status/<line>')
def get_line_status(line):
    """get specified subway line status"""
    try:
        service = MTAServiceFactory.get_service('subway')
        status = service.get_line_status(line)
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/feed/<line>')
def get_line_feed(line):
    """get specified subway line real-time data"""
    try:
        service = MTAServiceFactory.get_service('subway')
        feed = service.get_line_feed(line)
        return jsonify(feed)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/feed/all')
def get_all_feeds():
    """get all subway line real-time data"""
    try:
        service = MTAServiceFactory.get_service('subway')
        feeds = service.get_all_feeds()
        return jsonify(feeds)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 