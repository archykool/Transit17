from backend.models.base import BaseModel
from backend import db

class Route(BaseModel):
    """Model for transit routes"""
    __tablename__ = 'routes'

    route_id = db.Column(db.String(10), nullable=False, unique=True, index=True)
    agency_id = db.Column(db.String(10), nullable=False)  # subway, lirr, mnr
    route_short_name = db.Column(db.String(10))
    route_long_name = db.Column(db.String(100))
    route_desc = db.Column(db.Text)
    route_type = db.Column(db.Integer)  # GTFS route type
    route_url = db.Column(db.String(500))
    route_color = db.Column(db.String(6))
    route_text_color = db.Column(db.String(6))

    # Relationships
    trips = db.relationship('Trip', backref='route', lazy=True)
    stops = db.relationship('Stop', secondary='route_stops', backref='routes')

    def __repr__(self):
        return f'<Route {self.route_id}>'

class Stop(BaseModel):
    """Model for transit stops"""
    __tablename__ = 'stops'

    stop_id = db.Column(db.String(50), nullable=False, unique=True, index=True)
    stop_code = db.Column(db.String(50))
    stop_name = db.Column(db.String(100), nullable=False)
    stop_desc = db.Column(db.Text)
    stop_lat = db.Column(db.Float)
    stop_lon = db.Column(db.Float)
    zone_id = db.Column(db.String(50))
    stop_url = db.Column(db.String(500))
    location_type = db.Column(db.Integer)  # GTFS location type
    parent_station = db.Column(db.String(50), db.ForeignKey('stops.stop_id'))
    wheelchair_boarding = db.Column(db.Integer)

    # Relationships
    child_stops = db.relationship('Stop', backref=db.backref('parent', remote_side=[stop_id]))
    stop_times = db.relationship('StopTime', backref='stop', lazy=True)

    def __repr__(self):
        return f'<Stop {self.stop_id}>'

class Trip(BaseModel):
    """Model for transit trips"""
    __tablename__ = 'trips'

    trip_id = db.Column(db.String(50), nullable=False, unique=True, index=True)
    route_id = db.Column(db.String(10), db.ForeignKey('routes.route_id'), nullable=False)
    service_id = db.Column(db.String(50), nullable=False)
    trip_headsign = db.Column(db.String(100))
    trip_short_name = db.Column(db.String(50))
    direction_id = db.Column(db.Integer)
    block_id = db.Column(db.String(50))
    shape_id = db.Column(db.String(50))
    wheelchair_accessible = db.Column(db.Integer)
    bikes_allowed = db.Column(db.Integer)

    # Relationships
    stop_times = db.relationship('StopTime', backref='trip', lazy=True)

    def __repr__(self):
        return f'<Trip {self.trip_id}>'

class StopTime(BaseModel):
    """Model for scheduled stop times"""
    __tablename__ = 'stop_times'

    trip_id = db.Column(db.String(50), db.ForeignKey('trips.trip_id'), nullable=False)
    stop_id = db.Column(db.String(50), db.ForeignKey('stops.stop_id'), nullable=False)
    arrival_time = db.Column(db.String(8))  # HH:MM:SS format
    departure_time = db.Column(db.String(8))  # HH:MM:SS format
    stop_sequence = db.Column(db.Integer, nullable=False)
    stop_headsign = db.Column(db.String(100))
    pickup_type = db.Column(db.Integer)
    drop_off_type = db.Column(db.Integer)
    shape_dist_traveled = db.Column(db.Float)
    timepoint = db.Column(db.Integer)

    def __repr__(self):
        return f'<StopTime {self.trip_id} - {self.stop_id}>'

# Association table for routes and stops
route_stops = db.Table('route_stops',
    db.Column('route_id', db.String(10), db.ForeignKey('routes.route_id'), primary_key=True),
    db.Column('stop_id', db.String(50), db.ForeignKey('stops.stop_id'), primary_key=True)
) 