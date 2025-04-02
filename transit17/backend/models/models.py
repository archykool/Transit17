from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TripUpdate(db.Model):
    """store trip update information"""
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.String(50), nullable=False)
    route_id = db.Column(db.String(10), nullable=False)
    direction_id = db.Column(db.Integer)
    start_time = db.Column(db.String(10))
    start_date = db.Column(db.String(10))
    schedule_relationship = db.Column(db.Integer)
    feed_timestamp = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # related stop updates
    stop_updates = db.relationship('StopTimeUpdate', backref='trip_update', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'route_id': self.route_id,
            'direction_id': self.direction_id,
            'start_time': self.start_time,
            'start_date': self.start_date,
            'schedule_relationship': self.schedule_relationship,
            'feed_timestamp': self.feed_timestamp.isoformat(),
            'created_at': self.created_at.isoformat(),
            'stop_updates': [stop.to_dict() for stop in self.stop_updates]
        }

class StopTimeUpdate(db.Model):
    """store stop time update information"""
    id = db.Column(db.Integer, primary_key=True)
    trip_update_id = db.Column(db.Integer, db.ForeignKey('trip_update.id'), nullable=False)
    stop_id = db.Column(db.String(10), nullable=False)
    stop_sequence = db.Column(db.Integer)
    arrival_time = db.Column(db.DateTime)
    departure_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'stop_id': self.stop_id,
            'stop_sequence': self.stop_sequence,
            'arrival_time': self.arrival_time.isoformat() if self.arrival_time else None,
            'departure_time': self.departure_time.isoformat() if self.departure_time else None,
            'created_at': self.created_at.isoformat()
        }

class VehiclePosition(db.Model):
    """store vehicle position information"""
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(50))
    label = db.Column(db.String(50))
    license_plate = db.Column(db.String(20))
    current_stop_sequence = db.Column(db.Integer)
    current_status = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, nullable=False)
    congestion_level = db.Column(db.Integer)
    occupancy_status = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    speed = db.Column(db.Float)
    bearing = db.Column(db.Float)
    odometer = db.Column(db.Float)
    feed_timestamp = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'label': self.label,
            'license_plate': self.license_plate,
            'current_stop_sequence': self.current_stop_sequence,
            'current_status': self.current_status,
            'timestamp': self.timestamp.isoformat(),
            'congestion_level': self.congestion_level,
            'occupancy_status': self.occupancy_status,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'speed': self.speed,
            'bearing': self.bearing,
            'odometer': self.odometer,
            'feed_timestamp': self.feed_timestamp.isoformat(),
            'created_at': self.created_at.isoformat()
        }

class Alert(db.Model):
    """store service alert information"""
    id = db.Column(db.Integer, primary_key=True)
    active_period_start = db.Column(db.DateTime)
    active_period_end = db.Column(db.DateTime)
    informed_entity_type = db.Column(db.String(20))
    informed_entity_id = db.Column(db.String(50))
    cause = db.Column(db.Integer)
    effect = db.Column(db.Integer)
    url = db.Column(db.String(500))
    header_text = db.Column(db.Text)
    description_text = db.Column(db.Text)
    tts_header_text = db.Column(db.Text)
    tts_description_text = db.Column(db.Text)
    severity_level = db.Column(db.Integer)
    feed_timestamp = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'active_period_start': self.active_period_start.isoformat() if self.active_period_start else None,
            'active_period_end': self.active_period_end.isoformat() if self.active_period_end else None,
            'informed_entity_type': self.informed_entity_type,
            'informed_entity_id': self.informed_entity_id,
            'cause': self.cause,
            'effect': self.effect,
            'url': self.url,
            'header_text': self.header_text,
            'description_text': self.description_text,
            'tts_header_text': self.tts_header_text,
            'tts_description_text': self.tts_description_text,
            'severity_level': self.severity_level,
            'feed_timestamp': self.feed_timestamp.isoformat(),
            'created_at': self.created_at.isoformat()
        } 