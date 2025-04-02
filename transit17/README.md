# MTA Transit Data Application

A Flask-based web application for fetching and displaying real-time transit data from the MTA (Metropolitan Transportation Authority) API.

## Project Structure

```
transit17/
├── app.py                    # Main application file
├── requirements.txt          # Dependencies
├── README.md                 # Project documentation
├── backend/
│   ├── api/
│   │   └── routes/          # API routes for different transit systems
│   ├── config/              # Configuration files
│   ├── models/              # Database models
│   ├── services/            # Service layer for business logic
│   └── error_handlers.py    # Error handling utilities
├── frontend/
│   ├── static/              # Static files (CSS, JS, images)
│   └── templates/           # HTML templates (e.g., index.html)
├── tests/                   # Test files
└── scripts/                 # Utility scripts
```

## Features

- Real-time data for:
  - Subway lines
  - Long Island Rail Road (LIRR)
  - Metro-North Railroad (MNR)
- Service alerts and status updates
- GTFS real-time data processing
- RESTful API endpoints

## API Endpoints

### Subway
- `GET /api/subway/status` - Get status for all subway lines
- `GET /api/subway/status/<line>` - Get status for specific line
- `GET /api/subway/feed/<line>` - Get GTFS feed for specific line
- `GET /api/subway/feed/all` - Get GTFS feeds for all lines

### LIRR
- `GET /api/lirr/realtime` - Get real-time LIRR data
- `GET /api/lirr/feed` - Get LIRR GTFS feed

### MNR
- `GET /api/mnr/realtime` - Get real-time MNR data
- `GET /api/mnr/feed` - Get MNR GTFS feed

### Alerts
- `GET /api/alerts/subway` - Get subway alerts
- `GET /api/alerts/lirr` - Get LIRR alerts
- `GET /api/alerts/mnr` - Get MNR alerts
- `GET /api/alerts/all` - Get all transit system alerts

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## Dependencies

- Flask
- SQLAlchemy
- requests
- protobuf
- python-dotenv

## License

MIT License 