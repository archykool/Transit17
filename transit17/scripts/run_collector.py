import sys
import os

# Add project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from backend import create_app
from backend.services.data.collector import DataCollector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        collector = DataCollector()
        collector.run_collection() 