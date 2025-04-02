from datetime import datetime
from backend.services.mta.base import BaseMTAService
from backend.config.mta_endpoints import MNR_FEEDS

class MNRService(BaseMTAService):
    def __init__(self):
        super().__init__()
        self.feeds = MNR_FEEDS
        
    def get_feed(self, feed_type=None, feed_id=None):
        """get MNR's GTFS real-time data"""
        return super().get_feed('mnr', 'mnr')
        
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
        """get real-time data"""
        feed = self.get_feed()
        if not feed:
            return None
            
        return {
            'trip_updates': self.process_trip_updates(feed),
            'vehicle_positions': self.process_vehicle_positions(feed),
            'timestamp': self.get_timestamp()
        } 