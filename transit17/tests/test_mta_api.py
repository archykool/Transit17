import requests
from google.transit import gtfs_realtime_pb2
import time
from datetime import datetime

def analyze_gtfs_feed():
    # MTA A/C/E feed URL
    url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace"
    
    try:
        # Make request to MTA API
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse GTFS-realtime feed
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        
        print("\n=== Feed Header Information ===")
        print(f"Feed timestamp: {feed.header.timestamp}")
        print(f"Feed timestamp (human readable): {datetime.fromtimestamp(feed.header.timestamp)}")
        print(f"GTFS version: {feed.header.gtfs_realtime_version}")
        print(f"Number of entities: {len(feed.entity)}")
        
        # Analyze entity types
        entity_types = {
            'trip_update': 0,
            'vehicle': 0,
            'alert': 0
        }
        
        print("\n=== Entity Type Distribution ===")
        for entity in feed.entity:
            if entity.HasField('trip_update'):
                entity_types['trip_update'] += 1
            elif entity.HasField('vehicle'):
                entity_types['vehicle'] += 1
            elif entity.HasField('alert'):
                entity_types['alert'] += 1
        
        for entity_type, count in entity_types.items():
            print(f"{entity_type}: {count}")
        
        # Analyze trip updates
        print("\n=== Trip Update Analysis ===")
        trip_updates = [e for e in feed.entity if e.HasField('trip_update')]
        if trip_updates:
            trip = trip_updates[0].trip_update.trip
            print("\nTrip fields available:")
            print(f"- trip_id: {trip.trip_id}")
            print(f"- route_id: {trip.route_id}")
            print(f"- direction_id: {trip.direction_id}")
            print(f"- start_time: {trip.start_time}")
            print(f"- start_date: {trip.start_date}")
            print(f"- schedule_relationship: {trip.schedule_relationship}")
            
            if trip_updates[0].trip_update.stop_time_update:
                print("\nStop time update fields:")
                stop_update = trip_updates[0].trip_update.stop_time_update[0]
                print(f"- stop_id: {stop_update.stop_id}")
                print(f"- stop_sequence: {stop_update.stop_sequence}")
                print(f"- arrival: {stop_update.arrival.time if stop_update.HasField('arrival') else 'Not available'}")
                print(f"- departure: {stop_update.departure.time if stop_update.HasField('departure') else 'Not available'}")
        
        # Analyze vehicle positions
        print("\n=== Vehicle Position Analysis ===")
        vehicle_positions = [e for e in feed.entity if e.HasField('vehicle')]
        if vehicle_positions:
            vehicle = vehicle_positions[0].vehicle
            print("\nVehicle fields available:")
            print(f"- vehicle_id: {vehicle.vehicle.id}")
            print(f"- label: {vehicle.vehicle.label}")
            print(f"- license_plate: {vehicle.vehicle.license_plate}")
            print(f"- current_stop_sequence: {vehicle.current_stop_sequence}")
            print(f"- current_status: {vehicle.current_status}")
            print(f"- timestamp: {vehicle.timestamp}")
            print(f"- congestion_level: {vehicle.congestion_level}")
            print(f"- occupancy_status: {vehicle.occupancy_status}")
            print(f"- position: {vehicle.position.latitude}, {vehicle.position.longitude}")
            print(f"- speed: {vehicle.speed}")
            print(f"- bearing: {vehicle.bearing}")
            print(f"- odometer: {vehicle.odometer}")
        
        # Analyze alerts
        print("\n=== Alert Analysis ===")
        alerts = [e for e in feed.entity if e.HasField('alert')]
        if alerts:
            alert = alerts[0].alert
            print("\nAlert fields available:")
            print(f"- active_period: {alert.active_period}")
            print(f"- informed_entity: {alert.informed_entity}")
            print(f"- cause: {alert.cause}")
            print(f"- effect: {alert.effect}")
            print(f"- url: {alert.url}")
            print(f"- header_text: {alert.header_text}")
            print(f"- description_text: {alert.description_text}")
            print(f"- tts_header_text: {alert.tts_header_text}")
            print(f"- tts_description_text: {alert.tts_description_text}")
            print(f"- severity_level: {alert.severity_level}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    except Exception as e:
        print(f"Error processing feed: {e}")

if __name__ == "__main__":
    analyze_gtfs_feed() 