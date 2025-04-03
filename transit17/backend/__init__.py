from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.config.settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    
    # Initialize extensions
    db.init_app(app)
    
    # 注册蓝图
    from backend.routes import views
    app.register_blueprint(views.bp)
    
    return app

# import models
from backend.models.base import BaseModel
from backend.models.static import Route, Stop, Trip, StopTime
from backend.models.realtime import TripUpdate, StopTimeUpdate, VehiclePosition, ServiceAlert

__all__ = [
    'app',
    'db',
    'Route',
    'Stop',
    'Trip',
    'StopTime',
    'TripUpdate',
    'StopTimeUpdate',
    'VehiclePosition',
    'ServiceAlert'
] 