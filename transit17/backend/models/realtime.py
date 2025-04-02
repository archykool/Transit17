from datetime import datetime
from backend.models.base import BaseModel
from backend import db

class TripUpdate(BaseModel):
    """Model for GTFS trip updates"""
    __tablename__ = 'trip_updates'

    trip_id = db.Column(db.String(50), nullable=False, index=True)
    route_id = db.Column(db.String(10), nullable=False, index=True)
    direction_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.String(8))  # HH:MM:SS format
    start_date = db.Column(db.String(8))  # YYYYMMDD format
    schedule_relationship = db.Column(db.String(20))
    feed_timestamp = db.Column(db.DateTime, nullable=False, index=True)
    agency_id = db.Column(db.String(10), nullable=False)  # subway, lirr, mnr

    # Relationship with stop time updates
    stop_time_updates = db.relationship('StopTimeUpdate', backref='trip', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<TripUpdate {self.trip_id}>'

class StopTimeUpdate(BaseModel):
    """Model for GTFS stop time updates"""
    __tablename__ = 'stop_time_updates'

    trip_update_id = db.Column(db.Integer, db.ForeignKey('trip_updates.id'), nullable=False)
    stop_id = db.Column(db.String(50), nullable=False, index=True)
    stop_sequence = db.Column(db.Integer)
    arrival_time = db.Column(db.DateTime)
    departure_time = db.Column(db.DateTime)
    schedule_relationship = db.Column(db.String(20))

    def __repr__(self):
        return f'<StopTimeUpdate {self.stop_id}>'

class VehiclePosition(BaseModel):
    """Model for GTFS vehicle positions"""
    __tablename__ = 'vehicle_positions'

    vehicle_id = db.Column(db.String(50), nullable=False, index=True)
    trip_id = db.Column(db.String(50), nullable=True, index=True)
    label = db.Column(db.String(50))
    license_plate = db.Column(db.String(20))
    current_stop_sequence = db.Column(db.Integer)
    current_status = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, nullable=False)
    congestion_level = db.Column(db.String(20))
    occupancy_status = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    speed = db.Column(db.Float)
    bearing = db.Column(db.Float)
    odometer = db.Column(db.Float)
    feed_timestamp = db.Column(db.DateTime, nullable=False, index=True)
    agency_id = db.Column(db.String(10), nullable=False)  # subway, lirr, mnr

    def __repr__(self):
        return f'<VehiclePosition {self.vehicle_id}>'

class ServiceAlert(BaseModel):
    """Model for GTFS service alerts"""
    __tablename__ = 'service_alerts'

    active_period_start = db.Column(db.DateTime)
    active_period_end = db.Column(db.DateTime)
    informed_entity_type = db.Column(db.String(20))
    informed_entity_id = db.Column(db.String(50), index=True)
    cause = db.Column(db.String(20))
    effect = db.Column(db.String(20))
    url = db.Column(db.String(500))
    header_text = db.Column(db.Text)
    description_text = db.Column(db.Text)
    tts_header_text = db.Column(db.Text)
    tts_description_text = db.Column(db.Text)
    severity_level = db.Column(db.String(20))
    feed_timestamp = db.Column(db.DateTime, nullable=False, index=True)
    agency_id = db.Column(db.String(10), nullable=False)  # subway, lirr, mnr

    def __repr__(self):
        return f'<ServiceAlert {self.id}>' 