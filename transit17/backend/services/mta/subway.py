from datetime import datetime
from backend.services.mta.base import BaseMTAService
from backend.config.mta_endpoints import SUBWAY_FEEDS, SUBWAY_STATUS_URL

class SubwayService(BaseMTAService):
    def __init__(self):
        super().__init__()
        self.feeds = SUBWAY_FEEDS
        
    def get_line_status(self, line_id):
        """get specified subway line status"""
        response = self._make_request(SUBWAY_STATUS_URL)
        if not response:
            return None
            
        data = self._parse_json_response(response)
        if not data:
            return None
            
        # find specified line status
        for line in data.get('subway_lines', []):
            if line.get('line_id') == line_id:
                return {
                    'line': line_id,
                    'status': line.get('status'),
                    'timestamp': self.get_timestamp()
                }
                
        return None
        
    def get_all_line_statuses(self):
        """get all subway line statuses"""
        response = self._make_request(SUBWAY_STATUS_URL)
        if not response:
            return None
            
        data = self._parse_json_response(response)
        if not data:
            return None
            
        statuses = []
        for line in data.get('subway_lines', []):
            statuses.append({
                'line': line.get('line_id'),
                'status': line.get('status'),
                'timestamp': self.get_timestamp()
            })
            
        return statuses
        
    def get_line_feed(self, line_id):
        """get specified line's GTFS real-time data"""
        if line_id not in self.feeds:
            return None
            
        return self.get_feed('subway', line_id)
        
    def get_all_feeds(self):
        """get all line's GTFS real-time data"""
        feeds = {}
        for line_id in self.feeds:
            feed = self.get_line_feed(line_id)
            if feed:
                feeds[line_id] = feed
                
        return feeds

    def process_trip_updates(self, feed):
        """process trip update data"""
        if not feed:
            return []
            
        trip_updates = []
        for entity in feed.entity:
            if entity.HasField('trip_update'):
                trip = entity.trip_update.trip
                updates = []
                
                # process stop time updates
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
        
    def process_vehicle_positions(self, feed):
        """process vehicle position data"""
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
        
    def get_realtime_data(self):
        """get real-time data for all subway lines"""
        feeds = self.get_all_feeds()
        if not feeds:
            return None
            
        all_trip_updates = []
        all_vehicle_positions = []
        
        for feed in feeds.values():
            trip_updates = self.process_trip_updates(feed)
            vehicle_positions = self.process_vehicle_positions(feed)
            all_trip_updates.extend(trip_updates)
            all_vehicle_positions.extend(vehicle_positions)
            
        return {
            'trip_updates': all_trip_updates,
            'vehicle_positions': all_vehicle_positions,
            'timestamp': self.get_timestamp()
        } 