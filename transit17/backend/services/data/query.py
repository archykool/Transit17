from datetime import datetime, timedelta
from sqlalchemy import desc
from backend import db
from backend.models import (
    Route, Stop, Trip, StopTime,
    TripUpdate, StopTimeUpdate, VehiclePosition, ServiceAlert
)

class DataQuery:
    """Query data from database"""
    
    @staticmethod
    def get_route(route_id):
        """Get route by ID"""
        return Route.query.get(route_id)

    @staticmethod
    def get_stop(stop_id):
        """Get stop by ID"""
        return Stop.query.get(stop_id)

    @staticmethod
    def get_trip(trip_id):
        """Get trip by ID"""
        return Trip.query.get(trip_id)

    @staticmethod
    def get_stop_times(trip_id):
        """Get stop times for a trip"""
        return StopTime.query.filter_by(trip_id=trip_id).order_by(StopTime.stop_sequence).all()

    @staticmethod
    def get_latest_trip_updates(route_id=None, limit=10):
        """Get latest trip updates"""
        query = TripUpdate.query.order_by(desc(TripUpdate.feed_timestamp))
        if route_id:
            query = query.filter_by(route_id=route_id)
        return query.limit(limit).all()

    @staticmethod
    def get_latest_vehicle_positions(route_id=None, limit=10):
        """Get latest vehicle positions"""
        query = VehiclePosition.query.order_by(desc(VehiclePosition.feed_timestamp))
        if route_id:
            query = query.filter_by(route_id=route_id)
        return query.limit(limit).all()

    @staticmethod
    def get_active_alerts(route_id=None):
        """Get active service alerts"""
        now = datetime.utcnow()
        query = ServiceAlert.query.filter(
            (ServiceAlert.active_period_start <= now) &
            ((ServiceAlert.active_period_end >= now) | (ServiceAlert.active_period_end.is_(None)))
        )
        if route_id:
            query = query.filter_by(informed_entity_id=route_id)
        return query.all()

    @staticmethod
    def get_route_status(route_id):
        """Get current status of a route"""
        # Get latest trip updates
        trip_updates = DataQuery.get_latest_trip_updates(route_id, limit=1)
        
        # Get latest vehicle positions
        vehicle_positions = DataQuery.get_latest_vehicle_positions(route_id, limit=1)
        
        # Get active alerts
        alerts = DataQuery.get_active_alerts(route_id)
        
        return {
            'trip_updates': [update.to_dict() for update in trip_updates],
            'vehicle_positions': [position.to_dict() for position in vehicle_positions],
            'alerts': [alert.to_dict() for alert in alerts]
        }

    @staticmethod
    def get_stop_info(stop_id):
        """Get information about a stop"""
        stop = DataQuery.get_stop(stop_id)
        if not stop:
            return None
            
        # Get upcoming trips
        now = datetime.utcnow()
        upcoming_stop_times = StopTime.query.join(Trip).filter(
            StopTime.stop_id == stop_id,
            StopTime.departure_time > now.strftime('%H:%M:%S')
        ).order_by(StopTime.departure_time).limit(5).all()
        
        # Get active alerts
        alerts = DataQuery.get_active_alerts()
        
        return {
            'stop': stop.to_dict(),
            'upcoming_trips': [stop_time.to_dict() for stop_time in upcoming_stop_times],
            'alerts': [alert.to_dict() for alert in alerts]
        } 