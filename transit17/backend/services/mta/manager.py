import time
import logging
from datetime import datetime
from typing import Dict, Any
from backend.config.settings import API_POLL_INTERVAL
from backend.services.mta import MTAServiceFactory

class APIManager:
    """Manage MTA API calls with rate limiting and error handling"""
    
    def __init__(self):
        self.last_request_time = {}  # Track last request time for each service
        self.logger = logging.getLogger(__name__)
        self.min_interval = API_POLL_INTERVAL  # Minimum time between requests
        
    def can_make_request(self, service_type: str) -> bool:
        """Check if enough time has passed since last request"""
        now = time.time()
        if service_type not in self.last_request_time:
            return True
        
        time_since_last_request = now - self.last_request_time[service_type]
        return time_since_last_request >= self.min_interval
    
    def handle_error(self, error: Exception, retry_count: int) -> None:
        """Handle API errors with exponential backoff"""
        wait_time = min(300, 2 ** retry_count)  # Cap at 5 minutes
        self.logger.error(f"API error: {str(error)}. Retrying in {wait_time} seconds.")
        time.sleep(wait_time)
    
    def get_data(self, service_type: str, api_call) -> Dict[str, Any]:
        """Get data from MTA API with rate limiting and error handling"""
        retry_count = 0
        max_retries = 5
        
        while retry_count < max_retries:
            if not self.can_make_request(service_type):
                time.sleep(self.min_interval)
                continue
                
            try:
                data = api_call()
                self.last_request_time[service_type] = time.time()
                return data
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    self.logger.error(f"Max retries reached for {service_type}. Error: {str(e)}")
                    raise
                self.handle_error(e, retry_count)
        
        raise Exception(f"Failed to get data for {service_type} after {max_retries} retries")
    
    def get_all_data(self, services: Dict[str, callable]) -> Dict[str, Any]:
        """Get data from all services"""
        results = {}
        for service_type, api_call in services.items():
            try:
                results[service_type] = self.get_data(service_type, api_call)
            except Exception as e:
                self.logger.error(f"Failed to get data for {service_type}: {str(e)}")
                results[service_type] = None
        return results

    def get_all_data(self) -> Dict[str, Any]:
        """Get data from all services with coordinated timing"""
        results = {}
        for service_type in ['subway', 'lirr', 'mnr']:
            if self.can_make_request(service_type):
                data = self.get_data(service_type, lambda: MTAServiceFactory.get_service(service_type).get_realtime_data())
                if data:
                    results[service_type] = data
        return results 