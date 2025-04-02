import sys
import os

# Add project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import create_app, db
from backend.models import (
    TripUpdate, StopTimeUpdate, VehiclePosition, ServiceAlert,
    Route, Stop, Trip, StopTime
)

def init_db():
    """Initialize database"""
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database initialized successfully.")

def clear_db():
    """Clear all data from the database"""
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("All tables dropped successfully")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'clear':
        clear_db()
    init_db() 