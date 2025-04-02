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