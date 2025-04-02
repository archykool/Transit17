import csv
import requests
import tempfile
import zipfile
from datetime import datetime
from backend import db
from backend.models import (
    Route, Stop, Trip, StopTime,
    TripUpdate, StopTimeUpdate, VehiclePosition, ServiceAlert
)

class GTFSImporter:
    """Import GTFS static data into database"""
    
    def import_gtfs(self, url, agency_id):
        """Import GTFS data from URL"""
        # Download GTFS zip file
        response = requests.get(url)
        response.raise_for_status()
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save zip file
            zip_path = f"{temp_dir}/gtfs.zip"
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            # Extract zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Import each file
            try:
                self.import_routes(f"{temp_dir}/routes.txt")
                self.import_stops(f"{temp_dir}/stops.txt")
                self.import_trips(f"{temp_dir}/trips.txt")
                self.import_stop_times(f"{temp_dir}/stop_times.txt")
            except Exception as e:
                print(f"Error importing GTFS data: {str(e)}")
                raise

    @staticmethod
    def import_routes(file_path):
        """Import routes from GTFS routes.txt"""
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Check if route already exists
                    existing_route = Route.query.filter_by(route_id=row['route_id']).first()
                    if existing_route:
                        continue
                    
                    # Handle empty values
                    route_type = row.get('route_type', '')
                    if not route_type:
                        route_type = 1  # Default to subway/metro type
                    
                    route = Route(
                        route_id=row['route_id'],
                        agency_id=row.get('agency_id', 'subway'),
                        route_short_name=row.get('route_short_name'),
                        route_long_name=row.get('route_long_name'),
                        route_desc=row.get('route_desc'),
                        route_type=int(route_type),
                        route_url=row.get('route_url'),
                        route_color=row.get('route_color'),
                        route_text_color=row.get('route_text_color')
                    )
                    db.session.add(route)
                    db.session.commit()
                except Exception as e:
                    print(f"Error importing route {row.get('route_id')}: {str(e)}")
                    db.session.rollback()

    @staticmethod
    def import_stops(file_path):
        """Import stops from GTFS stops.txt"""
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Check if stop already exists
                    existing_stop = Stop.query.filter_by(stop_id=row['stop_id']).first()
                    if existing_stop:
                        continue
                    
                    # Handle empty values
                    stop_lat = row.get('stop_lat', '0')
                    stop_lon = row.get('stop_lon', '0')
                    location_type = row.get('location_type', '0')
                    wheelchair_boarding = row.get('wheelchair_boarding', '0')
                    
                    if not stop_lat:
                        stop_lat = '0'
                    if not stop_lon:
                        stop_lon = '0'
                    if not location_type:
                        location_type = '0'
                    if not wheelchair_boarding:
                        wheelchair_boarding = '0'
                    
                    stop = Stop(
                        stop_id=row['stop_id'],
                        stop_code=row.get('stop_code'),
                        stop_name=row['stop_name'],
                        stop_desc=row.get('stop_desc'),
                        stop_lat=float(stop_lat),
                        stop_lon=float(stop_lon),
                        zone_id=row.get('zone_id'),
                        stop_url=row.get('stop_url'),
                        location_type=int(location_type),
                        parent_station=row.get('parent_station'),
                        wheelchair_boarding=int(wheelchair_boarding)
                    )
                    db.session.add(stop)
                    db.session.commit()
                except Exception as e:
                    print(f"Error importing stop {row.get('stop_id')}: {str(e)}")
                    db.session.rollback()

    @staticmethod
    def import_trips(file_path):
        """Import trips from GTFS trips.txt"""
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                trip = Trip(
                    trip_id=row['trip_id'],
                    route_id=row['route_id'],
                    service_id=row['service_id'],
                    trip_headsign=row.get('trip_headsign'),
                    trip_short_name=row.get('trip_short_name'),
                    direction_id=int(row.get('direction_id', 0)),
                    block_id=row.get('block_id'),
                    shape_id=row.get('shape_id'),
                    wheelchair_accessible=int(row.get('wheelchair_accessible', 0)),
                    bikes_allowed=int(row.get('bikes_allowed', 0))
                )
                db.session.add(trip)
        db.session.commit()

    @staticmethod
    def import_stop_times(file_path):
        """Import stop times from GTFS stop_times.txt"""
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                stop_time = StopTime(
                    trip_id=row['trip_id'],
                    stop_id=row['stop_id'],
                    arrival_time=row['arrival_time'],
                    departure_time=row['departure_time'],
                    stop_sequence=int(row['stop_sequence']),
                    stop_headsign=row.get('stop_headsign'),
                    pickup_type=int(row.get('pickup_type', 0)),
                    drop_off_type=int(row.get('drop_off_type', 0)),
                    shape_dist_traveled=float(row.get('shape_dist_traveled', 0)),
                    timepoint=int(row.get('timepoint', 1))
                )
                db.session.add(stop_time)
        db.session.commit()

class RealtimeImporter:
    """Import GTFS real-time data into database"""
    
    @staticmethod
    def import_trip_update(trip_update_data, agency_id):
        """Import trip update from processed data"""
        trip_update = TripUpdate(
            trip_id=trip_update_data['trip_id'],
            route_id=trip_update_data['route_id'],
            direction_id=trip_update_data['direction_id'],
            start_time=trip_update_data['start_time'],
            start_date=trip_update_data['start_date'],
            schedule_relationship=trip_update_data['schedule_relationship'],
            feed_timestamp=datetime.now(),  # Use current time as feed timestamp
            agency_id=agency_id
        )
        db.session.add(trip_update)
        db.session.flush()

        # Import stop time updates
        for stop_update in trip_update_data['stop_updates']:
            stop_time_update = StopTimeUpdate(
                trip_update_id=trip_update.id,
                stop_id=stop_update['stop_id'],
                stop_sequence=stop_update['stop_sequence'],
                arrival_time=datetime.fromtimestamp(stop_update['arrival_time']) if stop_update['arrival_time'] else None,
                departure_time=datetime.fromtimestamp(stop_update['departure_time']) if stop_update['departure_time'] else None
            )
            db.session.add(stop_time_update)
        db.session.commit()

    @staticmethod
    def import_vehicle_position(vehicle_data, agency_id):
        """Import vehicle position from processed data"""
        position = VehiclePosition(
            vehicle_id=vehicle_data['vehicle_id'],
            trip_id=vehicle_data.get('trip_id'),
            current_stop_sequence=vehicle_data['current_stop_sequence'],
            current_status=vehicle_data['current_status'],
            timestamp=datetime.now(),  # Use current time as timestamp
            latitude=vehicle_data['position']['latitude'],
            longitude=vehicle_data['position']['longitude'],
            speed=vehicle_data['position'].get('speed'),
            bearing=vehicle_data['position'].get('bearing'),
            feed_timestamp=datetime.now(),  # Use current time as feed timestamp
            agency_id=agency_id
        )
        db.session.add(position)
        db.session.commit()

    @staticmethod
    def import_service_alert(feed, agency_id):
        """Import service alert from GTFS real-time feed"""
        for entity in feed.entity:
            if entity.HasField('alert'):
                alert = entity.alert
                service_alert = ServiceAlert(
                    active_period_start=datetime.fromtimestamp(alert.active_period[0].start) if alert.active_period else None,
                    active_period_end=datetime.fromtimestamp(alert.active_period[0].end) if alert.active_period else None,
                    informed_entity_type=alert.informed_entity[0].entity_type if alert.informed_entity else None,
                    informed_entity_id=alert.informed_entity[0].entity_id if alert.informed_entity else None,
                    cause=alert.cause,
                    effect=alert.effect,
                    url=alert.url.translation[0].text if alert.url else None,
                    header_text=alert.header.translation[0].text if alert.header else None,
                    description_text=alert.description.translation[0].text if alert.description else None,
                    tts_header_text=alert.tts_header.translation[0].text if alert.tts_header else None,
                    tts_description_text=alert.tts_description.translation[0].text if alert.tts_description else None,
                    severity_level=alert.severity_level,
                    feed_timestamp=datetime.fromtimestamp(feed.header.timestamp),
                    agency_id=agency_id
                )
                db.session.add(service_alert)
        db.session.commit() 