import os
from datetime import timedelta

# database configuration
SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.abspath("backend/data/mta_data.db")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# data retention period (hours)
DATA_RETENTION_HOURS = 24

# data cleanup interval (minutes)
CLEANUP_INTERVAL_MINUTES = 60

# API polling interval (seconds)
API_POLL_INTERVAL = 30

# logging configuration
LOG_LEVEL = 'INFO'
LOG_FILE = 'app.log'

# cache configuration
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes

# GTFS static data URLs
GTFS_URLS = {
    'subway': 'http://web.mta.info/developers/data/nyct/subway/google_transit.zip',
    'lirr': 'http://web.mta.info/developers/data/lirr/google_transit.zip',
    'mnr': 'http://web.mta.info/developers/data/mnr/google_transit.zip'
}

# data storage configuration
class StorageConfig:
    # data chunk size (amount of data each chunk can store)
    CHUNK_SIZE = 1000
    
    # enable data compression
    ENABLE_COMPRESSION = True
    
    # API polling interval (seconds)
    API_POLL_INTERVAL = 30
    
    # cleanup interval (minutes)
    CLEANUP_INTERVAL = 60
    
    # data cleanup strategy
    CLEANUP_STRATEGY = {
        'trip_updates': timedelta(hours=24),
        'vehicle_positions': timedelta(hours=24),
        'alerts': timedelta(days=7),
        'elevator_status': timedelta(days=30)
    } 