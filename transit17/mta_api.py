import requests
from datetime import datetime

class MTAAPI:
    def __init__(self):
        # MTA GTFS-realtime feed URLs
        self.base_url = "https://api-endpoint.mta.info"
        self.subway_status_url = "https://api-endpoint.mta.info/status/subway"
        
        # Standard headers for MTA API requests
        self.headers = {
            "Accept": "application/json"
        }

    def get_subway_status(self):
        """
        Fetch real-time subway status from MTA API
        Returns a list of subway line statuses
        """
        try:
            response = requests.get(
                self.subway_status_url,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching subway status: {e}")
            return None

    def parse_status_data(self, data):
        """
        Parse the raw API response into a structured format
        """
        if not data:
            return []
        
        parsed_data = []
        try:
            # Parse the MTA status data structure
            for line in data.get('subway_lines', []):
                parsed_data.append({
                    'line': line.get('line_id'),
                    'status': line.get('status'),
                    'timestamp': datetime.now()
                })
        except Exception as e:
            print(f"Error parsing status data: {e}")
        
        return parsed_data 