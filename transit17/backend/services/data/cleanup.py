from datetime import datetime, timedelta
from backend import db
from backend.models import (
    TripUpdate, StopTimeUpdate, VehiclePosition, ServiceAlert
)
from backend.config.settings import StorageConfig

class DataCleanup:
    """Clean up old data from database"""
    
    @staticmethod
    def cleanup_trip_updates():
        """Clean up old trip updates"""
        retention_period = StorageConfig.TRIP_UPDATES.retention_period
        cutoff_time = datetime.utcnow() - timedelta(hours=retention_period)
        
        # Delete old trip updates and their associated stop time updates
        old_trip_updates = TripUpdate.query.filter(
            TripUpdate.feed_timestamp < cutoff_time
        ).all()
        
        for trip_update in old_trip_updates:
            db.session.delete(trip_update)
        
        db.session.commit()

    @staticmethod
    def cleanup_vehicle_positions():
        """Clean up old vehicle positions"""
        retention_period = StorageConfig.VEHICLE_POSITIONS.retention_period
        cutoff_time = datetime.utcnow() - timedelta(hours=retention_period)
        
        VehiclePosition.query.filter(
            VehiclePosition.feed_timestamp < cutoff_time
        ).delete()
        
        db.session.commit()

    @staticmethod
    def cleanup_service_alerts():
        """Clean up old service alerts"""
        retention_period = StorageConfig.ALERTS.retention_period
        cutoff_time = datetime.utcnow() - timedelta(hours=retention_period)
        
        # Delete alerts that have ended and are older than retention period
        ServiceAlert.query.filter(
            (ServiceAlert.active_period_end < cutoff_time) |
            (ServiceAlert.feed_timestamp < cutoff_time)
        ).delete()
        
        db.session.commit()

    @classmethod
    def cleanup_all(cls):
        """Clean up all old data"""
        cls.cleanup_trip_updates()
        cls.cleanup_vehicle_positions()
        cls.cleanup_service_alerts() 