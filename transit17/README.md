# MTA Transit Data Collection and Visualization

A comprehensive system for collecting, storing, and visualizing MTA (Metropolitan Transportation Authority) transit data, including subway, LIRR, and Metro-North services.

## Project Structure

```
.
├── backend/                 # Core application code
│   ├── api/                # API endpoints and routes
│   ├── config/             # Configuration files
│   ├── data/               # Database files
│   ├── models/             # Database models
│   ├── routes/             # Web routes
│   ├── services/           # MTA service implementations
│   └── templates/          # HTML templates
├── frontend/               # Frontend assets
│   ├── static/             # Static files (CSS, JS, images)
│   └── templates/          # HTML templates
├── scripts/                # Utility scripts
│   ├── run_collector.py    # Data collection service
│   ├── serve_data.py       # Data serving service
│   ├── show_data.py        # Data statistics viewer
│   ├── import_gtfs.py      # GTFS static data importer
│   └── init_db.py          # Database initialization
└── config/                 # Configuration files
```

## Features

- Real-time data collection from MTA APIs
- Historical data storage and analysis
- Web-based data visualization
- Support for multiple transit systems:
  - NYC Subway
  - Long Island Rail Road (LIRR)
  - Metro-North Railroad (MNR)

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables in `.env`:
   ```
   MTA_API_KEY=your_api_key_here
   ```
4. Initialize the database:
   ```bash
   python scripts/init_db.py
   ```
5. Import GTFS static data:
   ```bash
   python scripts/import_gtfs.py
   ```

## Usage

### Data Collection

Start the data collection service:
```bash
python scripts/run_collector.py
```

### Data Visualization

1. Start the web server:
   ```bash
   python scripts/run_app.py
   ```
2. Access the web interface at `http://localhost:5000`

### Data Management

- View data statistics:
  ```bash
  python scripts/show_data.py
  ```
- Clean up old data:
  ```bash
  python scripts/run_cleanup.py
  ```

## API Endpoints

- `/api/subway/status` - Subway line statuses
- `/api/lirr/realtime` - LIRR real-time data
- `/api/mnr/realtime` - MNR real-time data
- `/api/alerts/subway` - Subway service alerts

## Data Models

- Static Data:
  - Routes
  - Stops
  - Trips
  - Stop Times

- Real-time Data:
  - Trip Updates
  - Stop Time Updates
  - Vehicle Positions
  - Service Alerts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 