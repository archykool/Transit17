from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from mta_api import MTAAPI
from datetime import datetime
import time
import requests
from google.transit import gtfs_realtime_pb2
from error_handlers import (
    MTAConnectionError, 
    MTADataError, 
    handle_mta_error, 
    validate_vehicle_position
)
import os
from models import db, TripUpdate, StopTimeUpdate, VehiclePosition, Alert

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mta_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

# Initialize MTA API client
mta_api = MTAAPI()

# Initialize database
db.init_app(app)

# Define data model for subway status
class SubwayStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'line': self.line,
            'status': self.status,
            'timestamp': self.timestamp.isoformat()
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    try:
        # Fetch data from MTA API
        raw_data = mta_api.get_subway_status()
        if not raw_data:
            return jsonify({"error": "Failed to fetch data from MTA API"}), 500

        # Parse the data
        parsed_data = mta_api.parse_status_data(raw_data)
        
        # Store in database
        for status_data in parsed_data:
            status = SubwayStatus(
                line=status_data['line'],
                status=status_data['status'],
                timestamp=status_data['timestamp']
            )
            db.session.add(status)
        
        db.session.commit()
        
        # Return latest statuses
        latest_statuses = SubwayStatus.query.order_by(SubwayStatus.timestamp.desc()).limit(10).all()
        return jsonify([status.to_dict() for status in latest_statuses])
    
    except Exception as e:
        return handle_mta_error(e)

@app.route('/api/ace-feed')
def get_ace_feed():
    try:
        # MTA A/C/E feed URL
        url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace"
        
        # Make request to MTA API
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise MTAConnectionError(f"Failed to connect to MTA API: {str(e)}")
        
        # Parse GTFS-realtime feed
        try:
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
        except Exception as e:
            raise MTADataError(f"Failed to parse GTFS feed: {str(e)}")
        
        # Process entities
        entities = []
        for entity in feed.entity:
            entity_data = {}
            
            if entity.HasField('trip_update'):
                trip_update = entity.trip_update
                entity_data['type'] = 'trip_update'
                entity_data['trip_id'] = trip_update.trip.trip_id
                entity_data['route_id'] = trip_update.trip.route_id
                if trip_update.stop_time_update:
                    entity_data['stop_updates'] = []
                    for stop_update in trip_update.stop_time_update:
                        stop_data = {
                            'stop_id': stop_update.stop_id,
                            'arrival_time': stop_update.arrival.time if stop_update.HasField('arrival') else None,
                            'departure_time': stop_update.departure.time if stop_update.HasField('departure') else None
                        }
                        entity_data['stop_updates'].append(stop_data)
            
            elif entity.HasField('vehicle'):
                vehicle = entity.vehicle
                # Validate vehicle position
                position_status = validate_vehicle_position(vehicle)
                
                entity_data['type'] = 'vehicle'
                entity_data['vehicle_id'] = vehicle.vehicle.id
                entity_data['current_stop'] = vehicle.current_stop_sequence
                entity_data['status'] = vehicle.current_status
                entity_data['position'] = {
                    'latitude': vehicle.position.latitude,
                    'longitude': vehicle.position.longitude,
                    'status': position_status['status'],
                    'message': position_status['message']
                }
            
            elif entity.HasField('alert'):
                alert = entity.alert
                entity_data['type'] = 'alert'
                entity_data['active_period'] = str(alert.active_period)
                entity_data['cause'] = alert.cause
                entity_data['effect'] = alert.effect
                entity_data['url'] = alert.url
                entity_data['header_text'] = alert.header_text
                entity_data['description_text'] = alert.description_text
            
            entities.append(entity_data)
        
        return jsonify({
            'timestamp': feed.header.timestamp,
            'entity_count': len(feed.entity),
            'entities': entities
        })
        
    except Exception as e:
        return handle_mta_error(e)

def save_to_database(feed):
    """将GTFS数据保存到数据库"""
    feed_timestamp = datetime.fromtimestamp(feed.header.timestamp)
    
    # 保存行程更新
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            trip_update = TripUpdate(
                trip_id=entity.trip_update.trip.trip_id,
                route_id=entity.trip_update.trip.route_id,
                direction_id=entity.trip_update.trip.direction_id,
                start_time=entity.trip_update.trip.start_time,
                start_date=entity.trip_update.trip.start_date,
                schedule_relationship=entity.trip_update.trip.schedule_relationship,
                feed_timestamp=feed_timestamp
            )
            db.session.add(trip_update)
            db.session.flush()  # 获取trip_update的ID
            
            # 保存站点更新
            for stop_time_update in entity.trip_update.stop_time_update:
                stop_update = StopTimeUpdate(
                    trip_update_id=trip_update.id,
                    stop_id=stop_time_update.stop_id,
                    stop_sequence=stop_time_update.stop_sequence,
                    arrival_time=datetime.fromtimestamp(stop_time_update.arrival.time) if stop_time_update.HasField('arrival') else None,
                    departure_time=datetime.fromtimestamp(stop_time_update.departure.time) if stop_time_update.HasField('departure') else None
                )
                db.session.add(stop_update)
        
        # 保存车辆位置
        elif entity.HasField('vehicle'):
            vehicle = entity.vehicle
            vehicle_position = VehiclePosition(
                vehicle_id=vehicle.vehicle.id,
                label=vehicle.vehicle.label,
                license_plate=vehicle.vehicle.license_plate,
                current_stop_sequence=vehicle.current_stop_sequence,
                current_status=vehicle.current_status,
                timestamp=datetime.fromtimestamp(vehicle.timestamp),
                congestion_level=vehicle.congestion_level,
                occupancy_status=vehicle.occupancy_status,
                latitude=vehicle.position.latitude,
                longitude=vehicle.position.longitude,
                speed=vehicle.position.speed,
                bearing=vehicle.position.bearing,
                odometer=vehicle.position.odometer,
                feed_timestamp=feed_timestamp
            )
            db.session.add(vehicle_position)
        
        # 保存警报
        elif entity.HasField('alert'):
            alert = entity.alert
            alert_record = Alert(
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
                feed_timestamp=feed_timestamp
            )
            db.session.add(alert_record)
    
    try:
        db.session.commit()
        print("数据已成功保存到数据库")
    except Exception as e:
        db.session.rollback()
        print(f"保存数据时出错: {str(e)}")

# 修改get_subway_status函数来保存数据
@app.route('/api/subway-status')
def get_subway_status():
    try:
        feed = mta_api.get_feed()
        if feed:
            # 保存数据到数据库
            save_to_database(feed)
            # 处理数据并返回
            subway_data = process_subway_data(feed)
            return jsonify(subway_data)
        else:
            return jsonify({'error': '无法获取数据'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 