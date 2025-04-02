"""
MTA API endpoints configuration
"""

# Base URL for all MTA API endpoints
BASE_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds"

# Subway Realtime Feeds
SUBWAY_FEEDS = {
    'ace': 'nyct%2Fgtfs-ace',      # A/C/E/SR
    'bdfm': 'nyct%2Fgtfs-bdfm',    # B/D/F/M/SF
    'g': 'nyct%2Fgtfs-g',          # G
    'jz': 'nyct%2Fgtfs-jz',        # J/Z
    'nqrw': 'nyct%2Fgtfs-nqrw',    # N/R/Q/W
    'l': 'nyct%2Fgtfs-l',          # L
    '1234567s': 'nyct%2Fgtfs',     # 1/2/3/4/5/6/7/S
    'sir': 'nyct%2Fgtfs-si'        # SIR
}

# LIRR Realtime Feeds
LIRR_FEEDS = {
    'lirr': 'lirr%2Fgtfs-lirr'     # Long Island Rail Road
}

# MNR Realtime Feeds
MNR_FEEDS = {
    'mnr': 'mnr%2Fgtfs-mnr'        # Metro-North Railroad
}

# Service Alert Feeds (GTFS)
SERVICE_ALERTS_GTFS = {
    'all': 'camsys%2Fall-alerts',
    'subway': 'camsys%2Fsubway-alerts',
    'bus': 'camsys%2Fbus-alerts',
    'lirr': 'camsys%2Flirr-alerts',
    'mnr': 'camsys%2Fmnr-alerts'
}

# Service Alert Feeds (JSON)
SERVICE_ALERTS_JSON = {
    'all': 'camsys%2Fall-alerts.json',
    'subway': 'camsys%2Fsubway-alerts.json',
    'bus': 'camsys%2Fbus-alerts.json',
    'lirr': 'camsys%2Flirr-alerts.json',
    'mnr': 'camsys%2Fmnr-alerts.json'
}

# Elevator and Escalator Feeds (XML)
ELEVATOR_ESCALATOR_XML = {
    'current_outages': 'nyct%2Fnyct_ene.xml',
    'upcoming_outages': 'nyct%2Fnyct_ene_upcoming.xml',
    'equipment': 'nyct%2Fnyct_ene_equipments.xml'
}

# Elevator and Escalator Feeds (JSON)
ELEVATOR_ESCALATOR_JSON = {
    'current_outages': 'nyct%2Fnyct_ene.json',
    'upcoming_outages': 'nyct%2Fnyct_ene_upcoming.json',
    'equipment': 'nyct%2Fnyct_ene_equipments.json'
}

# Subway Status URL
SUBWAY_STATUS_URL = "https://api-endpoint.mta.info/status/subway"

def get_feed_url(feed_type, feed_id):
    """
    Get the complete URL for a specific feed type and ID
    """
    feed_mapping = {
        'subway': SUBWAY_FEEDS,
        'lirr': LIRR_FEEDS,
        'mnr': MNR_FEEDS,
        'alerts_gtfs': SERVICE_ALERTS_GTFS,
        'alerts_json': SERVICE_ALERTS_JSON,
        'elevator_xml': ELEVATOR_ESCALATOR_XML,
        'elevator_json': ELEVATOR_ESCALATOR_JSON
    }
    
    if feed_type not in feed_mapping:
        raise ValueError(f"Invalid feed type: {feed_type}")
        
    if feed_id not in feed_mapping[feed_type]:
        raise ValueError(f"Invalid feed ID for type {feed_type}: {feed_id}")
        
    return f"{BASE_URL}/{feed_mapping[feed_type][feed_id]}" 