from mta_api import MTAAPI
import json
from datetime import datetime

def analyze_gtfs_feed(feed_type, feed_id):
    """analyze GTFS real-time data structure"""
    mta = MTAAPI()
    feed = mta.get_gtfs_feed(feed_type, feed_id)
    
    if not feed:
        print(f"Failed to get feed for {feed_type}/{feed_id}")
        return
        
    print(f"\nAnalyzing {feed_type}/{feed_id} feed structure:")
    print(f"Total entities: {len(feed.entity)}")
    
    # analyze different types of entities
    entity_types = {
        'trip_update': 0,
        'vehicle': 0,
        'alert': 0
    }
    
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            entity_types['trip_update'] += 1
        elif entity.HasField('vehicle'):
            entity_types['vehicle'] += 1
        elif entity.HasField('alert'):
            entity_types['alert'] += 1
            
    print("Entity types distribution:")
    for type_name, count in entity_types.items():
        print(f"  {type_name}: {count}")
        
    # analyze trip_update structure
    if entity_types['trip_update'] > 0:
        print("\nTrip Update structure:")
        trip_update = next(e.trip_update for e in feed.entity if e.HasField('trip_update'))
        print(f"  Trip ID: {trip_update.trip.trip_id}")
        print(f"  Route ID: {trip_update.trip.route_id}")
        print(f"  Direction ID: {trip_update.trip.direction_id}")
        print(f"  Start Time: {trip_update.trip.start_time}")
        print(f"  Start Date: {trip_update.trip.start_date}")
        print(f"  Schedule Relationship: {trip_update.trip.schedule_relationship}")
        print(f"  Stop Time Updates: {len(trip_update.stop_time_update)}")
        
    # analyze vehicle structure
    if entity_types['vehicle'] > 0:
        print("\nVehicle structure:")
        vehicle = next(e.vehicle for e in feed.entity if e.HasField('vehicle'))
        print(f"  Vehicle ID: {vehicle.vehicle.id}")
        print(f"  Label: {vehicle.vehicle.label}")
        print(f"  License Plate: {vehicle.vehicle.license_plate}")
        print(f"  Current Stop Sequence: {vehicle.current_stop_sequence}")
        print(f"  Current Status: {vehicle.current_status}")
        print(f"  Timestamp: {datetime.fromtimestamp(vehicle.timestamp)}")
        print(f"  Position: ({vehicle.position.latitude}, {vehicle.position.longitude})")
        print(f"  Speed: {vehicle.position.speed}")
        print(f"  Bearing: {vehicle.position.bearing}")
        
    # analyze alert structure
    if entity_types['alert'] > 0:
        print("\nAlert structure:")
        alert = next(e.alert for e in feed.entity if e.HasField('alert'))
        print(f"  Active Period: {alert.active_period}")
        print(f"  Cause: {alert.cause}")
        print(f"  Effect: {alert.effect}")
        print(f"  URL: {alert.url}")
        print(f"  Header Text: {alert.header_text}")
        print(f"  Description Text: {alert.description_text}")

def analyze_service_alerts():
    """analyze service alert data structure"""
    mta = MTAAPI()
    alerts = mta.get_all_alerts(format='json')
    
    if not alerts:
        print("Failed to get service alerts")
        return
        
    print("\nAnalyzing service alerts structure:")
    for alert_type, alert_data in alerts.items():
        print(f"\nAlert type: {alert_type}")
        print(f"Total alerts: {len(alert_data.get('alerts', []))}")
        
        if alert_data.get('alerts'):
            sample_alert = alert_data['alerts'][0]
            print("\nSample alert structure:")
            print(json.dumps(sample_alert, indent=2))

def analyze_elevator_status():
    """analyze elevator status data structure"""
    mta = MTAAPI()
    status = mta.get_elevator_status(format='json')
    
    if not status:
        print("Failed to get elevator status")
        return
        
    print("\nAnalyzing elevator status structure:")
    for status_type, status_data in status.items():
        print(f"\nStatus type: {status_type}")
        print(f"Total records: {len(status_data.get('outages', []))}")
        
        if status_data.get('outages'):
            sample_outage = status_data['outages'][0]
            print("\nSample outage structure:")
            print(json.dumps(sample_outage, indent=2))

if __name__ == '__main__':
    # test subway real-time data
    analyze_gtfs_feed('subway', 'ace')
    
    # test service alerts
    analyze_service_alerts()
    
    # test elevator status
    analyze_elevator_status() 