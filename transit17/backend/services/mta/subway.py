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