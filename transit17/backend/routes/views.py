from flask import Blueprint, render_template
from datetime import datetime
from backend.models import (
    Route, Stop, Trip, StopTime,
    TripUpdate, StopTimeUpdate, VehiclePosition, ServiceAlert
)

bp = Blueprint('views', __name__)

@bp.route('/')
def index():
    # 获取统计数据
    stats = {
        'routes_count': Route.query.count(),
        'stops_count': Stop.query.count(),
        'trips_count': Trip.query.count(),
        'stop_times_count': StopTime.query.count(),
        'trip_updates_count': TripUpdate.query.count(),
        'stop_time_updates_count': StopTimeUpdate.query.count(),
        'vehicle_positions_count': VehiclePosition.query.count(),
        'service_alerts_count': ServiceAlert.query.count()
    }

    # 获取示例数据
    routes = Route.query.limit(10).all()
    stops = Stop.query.limit(10).all()
    vehicle_positions = VehiclePosition.query.order_by(
        VehiclePosition.timestamp.desc()
    ).limit(10).all()
    
    # 获取当前有效的服务提醒
    service_alerts = ServiceAlert.query.filter(
        (ServiceAlert.active_period_end > datetime.now()) | 
        (ServiceAlert.active_period_end.is_(None))
    ).limit(5).all()

    return render_template(
        'index.html',
        stats=stats,
        routes=routes,
        stops=stops,
        vehicle_positions=vehicle_positions,
        service_alerts=service_alerts
    ) 