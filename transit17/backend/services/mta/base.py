import requests
from datetime import datetime
from google.transit import gtfs_realtime_pb2
from backend.config.mta_endpoints import get_feed_url

class BaseMTAService:
    def __init__(self):
        self.headers = {
            "Accept": "application/json"
        }
        
    def _make_request(self, url):
        """send HTTP request and handle response"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return None
            
    def _parse_gtfs_feed(self, response):
        """parse GTFS real-time data"""
        try:
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            return feed
        except Exception as e:
            print(f"Error parsing GTFS feed: {e}")
            return None
            
    def _parse_json_response(self, response):
        """parse JSON response"""
        try:
            return response.json()
        except Exception as e:
            print(f"Error parsing JSON response: {e}")
            return None
            
    def get_feed(self, feed_type, feed_id, format='gtfs'):
        """get specified type of feed data"""
        url = get_feed_url(feed_type, feed_id)
        response = self._make_request(url)
        
        if not response:
            return None
            
        if format == 'gtfs':
            return self._parse_gtfs_feed(response)
        else:
            return self._parse_json_response(response)
            
    def get_timestamp(self):
        """get current timestamp"""
        return datetime.now()

    def process_vehicle_positions(self, feed):
        """Process vehicle position data from GTFS feed"""
        if not feed:
            return []
            
        positions = []
        for entity in feed.entity:
            if entity.HasField('vehicle'):
                vehicle = entity.vehicle
                positions.append({
                    'vehicle_id': vehicle.vehicle.id,
                    'trip_id': vehicle.trip.trip_id if vehicle.HasField('trip') else None,
                    'current_stop_sequence': vehicle.current_stop_sequence,
                    'current_status': vehicle.current_status,
                    'timestamp': datetime.fromtimestamp(vehicle.timestamp),
                    'position': {
                        'latitude': vehicle.position.latitude,
                        'longitude': vehicle.position.longitude,
                        'speed': vehicle.position.speed,
                        'bearing': vehicle.position.bearing
                    }
                })
                
        return positions 

    def process_trip_updates(self, feed):
        """Process trip update data from GTFS feed"""
        if not feed:
            return []
            
        trip_updates = []
        for entity in feed.entity:
            if entity.HasField('trip_update'):
                trip = entity.trip_update.trip
                updates = []
                
                # Process stop time updates
                for stop_update in entity.trip_update.stop_time_update:
                    updates.append({
                        'stop_id': stop_update.stop_id,
                        'arrival_time': stop_update.arrival.time if stop_update.HasField('arrival') else None,
                        'departure_time': stop_update.departure.time if stop_update.HasField('departure') else None,
                        'stop_sequence': stop_update.stop_sequence
                    })
                    
                trip_updates.append({
                    'trip_id': trip.trip_id,
                    'route_id': trip.route_id,
                    'direction_id': trip.direction_id,
                    'start_time': trip.start_time,
                    'start_date': trip.start_date,
                    'schedule_relationship': trip.schedule_relationship,
                    'stop_updates': updates,
                    'timestamp': self.get_timestamp()
                })
                
        return trip_updates 