import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timedelta
import logging
from pathlib import Path
import socket
import time

# Add the project root directory to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from backend import create_app
from backend.models.static import Route, Stop, Trip, StopTime
from backend.models.realtime import ServiceAlert, VehiclePosition, StopTimeUpdate
from backend.config.settings import StorageConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_available_port(start_port=5000, max_port=5050):
    """Find an available port to run the server on"""
    for port in range(start_port, max_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"No available ports found between {start_port} and {max_port}")

class MTARequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.app = create_app()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        try:
            if self.path == '/api/status':
                with self.app.app_context():
                    # Set request timeout
                    socket.setdefaulttimeout(10)  # 10 seconds timeout
                    
                    data = {
                        'service_status': self.get_service_status(),
                        'subway_lines': self.get_subway_lines_status(),
                        'stations': self.get_major_stations(),
                        'alerts': self.get_service_alerts(),
                        'vehicle_positions': self.get_vehicle_positions(),
                        'arrival_times': self.get_arrival_times()
                    }
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode())
            elif self.path == '/passenger_view.html':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open('passenger_view.html', 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
        except socket.timeout:
            logger.error("Request timed out")
            self.send_response(504)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Request timed out'}).encode())
        except Exception as e:
            logger.error(f"Error handling request: {str(e)}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def get_service_status(self):
        try:
            with self.app.app_context():
                # Check for active service alerts
                active_alerts = ServiceAlert.query.filter(
                    (ServiceAlert.active_period_start <= datetime.now()) &
                    ((ServiceAlert.active_period_end >= datetime.now()) | (ServiceAlert.active_period_end.is_(None)))
                ).limit(10).all()  # Limit query results

                status = {
                    'subway': 'Good Service',
                    'lirr': 'Good Service',
                    'mnr': 'Good Service'
                }

                for alert in active_alerts:
                    if 'subway' in alert.header_text.lower():
                        status['subway'] = 'Service Alert'
                    elif 'lirr' in alert.header_text.lower():
                        status['lirr'] = 'Service Alert'
                    elif 'mnr' in alert.header_text.lower():
                        status['mnr'] = 'Service Alert'

                return status
        except Exception as e:
            logger.error(f"Error getting service status: {str(e)}")
            return {
                'subway': 'Unknown',
                'lirr': 'Unknown',
                'mnr': 'Unknown'
            }

    def get_subway_lines_status(self):
        try:
            with self.app.app_context():
                subway_routes = Route.query.filter(Route.agency_id == 'MTA NYCT').limit(20).all()  # Limit query results
                status = {}
                
                for route in subway_routes:
                    status[route.route_short_name] = {
                        'status': 'Good Service',
                        'vehicles': []
                    }
                    
                    # Get vehicle positions for this route
                    vehicles = VehiclePosition.query.filter(
                        VehiclePosition.trip_id.in_(
                            Trip.query.filter_by(route_id=route.route_id).with_entities(Trip.trip_id)
                        ),
                        VehiclePosition.feed_timestamp >= datetime.now() - timedelta(minutes=5)
                    ).limit(10).all()  # Limit query results
                    
                    for vehicle in vehicles:
                        status[route.route_short_name]['vehicles'].append({
                            'id': vehicle.vehicle_id,
                            'current_stop': vehicle.current_stop_sequence,
                            'status': vehicle.current_status,
                            'timestamp': vehicle.feed_timestamp.isoformat()
                        })
                    
                    # Check for alerts affecting this route
                    active_alerts = ServiceAlert.query.filter(
                        (ServiceAlert.active_period_start <= datetime.now()) &
                        ((ServiceAlert.active_period_end >= datetime.now()) | (ServiceAlert.active_period_end.is_(None))) &
                        (ServiceAlert.header_text.like(f'%{route.route_short_name}%'))
                    ).first()
                    
                    if active_alerts:
                        status[route.route_short_name]['status'] = 'Service Alert'
                
                return status
        except Exception as e:
            logger.error(f"Error getting subway lines status: {str(e)}")
            return {}

    def get_major_stations(self):
        try:
            with self.app.app_context():
                stations = {}
                stops = Stop.query.limit(50).all()  # Limit query results
                
                for stop in stops:
                    if stop.stop_name not in stations:
                        stations[stop.stop_name] = {
                            'name': stop.stop_name,
                            'lines': set(),
                            'status': 'Good Service',
                            'arrivals': []
                        }
                    
                    # Get all routes passing through this station
                    routes = Route.query.join(Trip).join(StopTime).filter(
                        StopTime.stop_id == stop.stop_id
                    ).limit(10).all()  # Limit query results
                    
                    for route in routes:
                        if route.route_short_name:  # Ensure route_short_name is not None
                            stations[stop.stop_name]['lines'].add(route.route_short_name)
                        
                        # Get real-time arrival information for this station
                        arrivals = StopTimeUpdate.query.filter(
                            StopTimeUpdate.stop_id == stop.stop_id,
                            StopTimeUpdate.arrival_time >= datetime.now(),
                            StopTimeUpdate.arrival_time <= datetime.now() + timedelta(minutes=30)
                        ).order_by(StopTimeUpdate.arrival_time).limit(5).all()
                        
                        for arrival in arrivals:
                            stations[stop.stop_name]['arrivals'].append({
                                'route': route.route_short_name or 'Unknown',
                                'arrival_time': arrival.arrival_time.isoformat() if arrival.arrival_time else None,
                                'status': arrival.schedule_relationship or 'Unknown'
                            })
                
                # Convert to list and sort (by number of lines)
                station_list = []
                for station in stations.values():
                    station['lines'] = ', '.join(sorted(station['lines']))
                    station_list.append(station)
                
                # Sort by number of lines and return top 10
                return sorted(station_list, key=lambda x: len(x['lines']), reverse=True)[:10]
        except Exception as e:
            logger.error(f"Error getting major stations: {str(e)}")
            return []

    def get_service_alerts(self):
        try:
            with self.app.app_context():
                alerts = ServiceAlert.query.filter(
                    (ServiceAlert.active_period_start <= datetime.now()) &
                    ((ServiceAlert.active_period_end >= datetime.now()) | (ServiceAlert.active_period_end.is_(None)))
                ).limit(10).all()  # Limit query results
                
                return [{
                    'header': alert.header_text,
                    'description': alert.description_text,
                    'start_time': alert.active_period_start.isoformat() if alert.active_period_start else None,
                    'end_time': alert.active_period_end.isoformat() if alert.active_period_end else None
                } for alert in alerts]
        except Exception as e:
            logger.error(f"Error getting service alerts: {str(e)}")
            return []

    def get_vehicle_positions(self):
        try:
            with self.app.app_context():
                vehicles = VehiclePosition.query.filter(
                    VehiclePosition.feed_timestamp >= datetime.now() - timedelta(minutes=5)
                ).limit(50).all()  # Limit query results
                
                return [{
                    'trip_id': vehicle.trip_id,
                    'vehicle_id': vehicle.vehicle_id,
                    'current_stop': vehicle.current_stop_sequence,
                    'status': vehicle.current_status,
                    'timestamp': vehicle.feed_timestamp.isoformat()
                } for vehicle in vehicles]
        except Exception as e:
            logger.error(f"Error getting vehicle positions: {str(e)}")
            return []

    def get_arrival_times(self):
        try:
            with self.app.app_context():
                arrivals = StopTimeUpdate.query.filter(
                    StopTimeUpdate.arrival_time >= datetime.now(),
                    StopTimeUpdate.arrival_time <= datetime.now() + timedelta(minutes=30)
                ).order_by(StopTimeUpdate.arrival_time).limit(50).all()  # Limit query results
                
                return [{
                    'stop_id': arrival.stop_id,
                    'trip_update_id': arrival.trip_update_id,  # Use trip_update_id instead of trip_id
                    'arrival_time': arrival.arrival_time.isoformat() if arrival.arrival_time else None,
                    'status': arrival.schedule_relationship or 'Unknown'
                } for arrival in arrivals]
        except Exception as e:
            logger.error(f"Error getting arrival times: {str(e)}")
            return []

def run_server(port=None):
    if port is None:
        port = find_available_port()
    server_address = ('', port)
    httpd = HTTPServer(server_address, MTARequestHandler)
    logger.info(f'Server running on http://localhost:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server() 