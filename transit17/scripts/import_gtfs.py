import sys
import os
import logging
from datetime import datetime

# Add project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import create_app, db
from backend.services.data.importer import GTFSImporter
from backend.config.settings import GTFS_URLS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def import_gtfs_data():
    """Import GTFS static data for all agencies"""
    app = create_app()
    with app.app_context():
        importer = GTFSImporter()
        
        for agency_id, url in GTFS_URLS.items():
            try:
                logger.info(f"Importing GTFS data for {agency_id}")
                importer.import_gtfs(url, agency_id)
                logger.info(f"Successfully imported GTFS data for {agency_id}")
            except Exception as e:
                logger.error(f"Error importing GTFS data for {agency_id}: {e}")

if __name__ == '__main__':
    import_gtfs_data() 