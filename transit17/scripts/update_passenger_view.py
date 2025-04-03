import sys
import os
from datetime import datetime

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import db
from backend.models.static import Route, Stop
from backend.models.realtime import ServiceAlert, VehiclePosition

def get_service_status():
    """Get current service status for all lines"""
    status = {
        'subway': 'All Lines Operating',
        'lirr': 'Normal Service',
        'mnr': 'Normal Service'
    }
    
    # Check for service alerts
    alerts = ServiceAlert.query.filter(
        (ServiceAlert.active_period_end > datetime.now()) | 
        (ServiceAlert.active_period_end.is_(None))
    ).all()
    
    if alerts:
        status['subway'] = 'Service Alerts'
    
    return status

def get_subway_lines_status():
    """Get status for each subway line"""
    lines = {
        'A C E': 'Good Service',
        'B D F M': 'Good Service',
        'G': 'Good Service',
        'J Z': 'Good Service',
        'L': 'Good Service',
        'N Q R W': 'Good Service',
        '1 2 3': 'Good Service',
        '4 5 6': 'Good Service',
        '7': 'Good Service'
    }
    
    # Check for delays or disruptions
    alerts = ServiceAlert.query.filter(
        (ServiceAlert.active_period_end > datetime.now()) | 
        (ServiceAlert.active_period_end.is_(None))
    ).all()
    
    for alert in alerts:
        # Update line status based on alerts
        # This is a simplified version - in reality, you'd parse the alert text
        # to determine which lines are affected
        pass
    
    return lines

def get_major_stations():
    """Get information about major stations"""
    stations = [
        {
            'name': 'Times Square - 42nd St',
            'lines': '1 2 3 7 N Q R W S',
            'status': 'Open'
        },
        {
            'name': 'Grand Central - 42nd St',
            'lines': '4 5 6 7 S',
            'status': 'Open'
        },
        {
            'name': 'Penn Station',
            'lines': '1 2 3 A C E',
            'status': 'Open'
        }
    ]
    
    # Check station status based on vehicle positions
    positions = VehiclePosition.query.order_by(
        VehiclePosition.timestamp.desc()
    ).limit(100).all()
    
    # Update station status based on recent vehicle positions
    # This is a simplified version - in reality, you'd analyze the positions
    # to determine if stations are operating normally
    
    return stations

def get_service_alerts():
    """Get current service alerts"""
    alerts = ServiceAlert.query.filter(
        (ServiceAlert.active_period_end > datetime.now()) | 
        (ServiceAlert.active_period_end.is_(None))
    ).order_by(ServiceAlert.active_period_start.desc()).limit(5).all()
    
    return alerts

if __name__ == '__main__':
    # Get current data
    service_status = get_service_status()
    subway_lines = get_subway_lines_status()
    stations = get_major_stations()
    alerts = get_service_alerts()
    
    # Print data for debugging
    print("\nService Status:")
    print(service_status)
    
    print("\nSubway Lines Status:")
    print(subway_lines)
    
    print("\nMajor Stations:")
    print(stations)
    
    print("\nService Alerts:")
    for alert in alerts:
        print(f"- {alert.header_text}")
        print(f"  {alert.description_text}")
        print(f"  Start: {alert.active_period_start}")
        if alert.active_period_end:
            print(f"  End: {alert.active_period_end}") 