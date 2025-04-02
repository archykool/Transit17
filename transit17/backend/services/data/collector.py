import logging
from datetime import datetime
from typing import Dict, Any
from backend.services.mta.manager import APIManager
from backend.services.data.importer import RealtimeImporter
from backend.services.data.cleanup import DataCleanup
from backend.config.settings import StorageConfig
import time

class DataCollector:
    """Collect and store data from MTA API"""
    
    def __init__(self):
        self.api_manager = APIManager()
        self.logger = logging.getLogger(__name__)
        self.last_collection_time: Dict[str, datetime] = {}

    def collect_data(self) -> None:
        """Collect data from all services"""
        try:
            # Get data from all services
            data = self.api_manager.get_all_data()
            
            # Process and store data
            for service_type, service_data in data.items():
                if not service_data:
                    continue
                    
                # Import trip updates
                if 'trip_updates' in service_data:
                    for trip_update in service_data['trip_updates']:
                        RealtimeImporter.import_trip_update(trip_update, service_type)
                
                # Import vehicle positions
                if 'vehicle_positions' in service_data:
                    for vehicle_position in service_data['vehicle_positions']:
                        RealtimeImporter.import_vehicle_position(vehicle_position, service_type)
                
                self.last_collection_time[service_type] = datetime.utcnow()
                self.logger.info(f"Data collected for {service_type}")
                
        except Exception as e:
            self.logger.error(f"Error collecting data: {str(e)}")

    def run_collection(self) -> None:
        """Run continuous data collection"""
        self.logger.info("Starting data collection service...")
        
        while True:
            try:
                self.collect_data()
                
                # Check if cleanup is needed
                for service_type, last_time in self.last_collection_time.items():
                    time_since_last_cleanup = (
                        datetime.utcnow() - last_time
                    ).total_seconds() / 60
                    
                    if time_since_last_cleanup >= StorageConfig.CLEANUP_INTERVAL:
                        DataCleanup.cleanup_all()
                        self.logger.info("Data cleanup completed")
                
                # Wait for next collection interval
                time.sleep(StorageConfig.API_POLL_INTERVAL)
                
            except Exception as e:
                self.logger.error(f"Error in data collection: {str(e)}")
                # Wait before retrying
                time.sleep(60) 