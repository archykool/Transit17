from datetime import datetime
from backend.services.mta.base import BaseMTAService
from backend.config.mta_endpoints import MNR_FEEDS

class MNRService(BaseMTAService):
    def __init__(self):
        super().__init__()
        self.feeds = MNR_FEEDS
        
    def get_feed(self):
        """get MNR GTFS real-time data"""
        return self.get_feed('mnr')
        
    def get_realtime_data(self):
        """get real-time data for MNR"""
        feed = self.get_feed()
        if not feed:
            return None
            
        trip_updates = self.process_trip_updates(feed)
        vehicle_positions = self.process_vehicle_positions(feed)
        
        return {
            'trip_updates': trip_updates,
            'vehicle_positions': vehicle_positions,
            'timestamp': self.get_timestamp()
        } 