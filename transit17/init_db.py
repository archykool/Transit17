from app import app, db
from models import TripUpdate, StopTimeUpdate, VehiclePosition, Alert

def init_database():
    with app.app_context():
        # create all tables
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    init_database() 