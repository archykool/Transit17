import schedule
import time
from datetime import datetime
from backend.services.data.cleanup import DataCleanup
from backend.config.settings import StorageConfig

class DataScheduler:
    """Schedule data cleanup tasks"""
    
    @staticmethod
    def schedule_cleanup():
        """Schedule all cleanup tasks"""
        # Schedule trip updates cleanup
        schedule.every(StorageConfig.TRIP_UPDATES.cleanup_interval).minutes.do(
            DataCleanup.cleanup_trip_updates
        )
        
        # Schedule vehicle positions cleanup
        schedule.every(StorageConfig.VEHICLE_POSITIONS.cleanup_interval).minutes.do(
            DataCleanup.cleanup_vehicle_positions
        )
        
        # Schedule service alerts cleanup
        schedule.every(StorageConfig.ALERTS.cleanup_interval).minutes.do(
            DataCleanup.cleanup_service_alerts
        )
        
        print(f"Cleanup tasks scheduled at {datetime.now()}")

    @staticmethod
    def run_scheduler():
        """Run the scheduler"""
        print("Starting data cleanup scheduler...")
        DataScheduler.schedule_cleanup()
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                print(f"Error in scheduler: {str(e)}")
                time.sleep(60)  # Wait a minute before retrying 