import sys
import os
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import db
from backend.models.static import Route, Stop, Trip, StopTime
from backend.models.realtime import TripUpdate, StopTimeUpdate, VehiclePosition, ServiceAlert

def show_stats():
    """显示数据库统计信息"""
    print("\n=== 静态数据统计 ===")
    print(f"路线数量: {Route.query.count()}")
    print(f"站点数量: {Stop.query.count()}")
    print(f"行程数量: {Trip.query.count()}")
    print(f"时刻表条目: {StopTime.query.count()}")
    
    print("\n=== 实时数据统计 ===")
    print(f"行程更新: {TripUpdate.query.count()}")
    print(f"站点时间更新: {StopTimeUpdate.query.count()}")
    print(f"车辆位置: {VehiclePosition.query.count()}")
    print(f"服务提醒: {ServiceAlert.query.count()}")

def show_examples():
    print("\n=== 示例数据 ===")
    
    print("\n路线示例:")
    routes = Route.query.limit(5).all()
    for route in routes:
        print(f"- {route.route_id}: {route.route_long_name or route.route_short_name}")

    print("\n站点示例:")
    stops = Stop.query.limit(5).all()
    for stop in stops:
        print(f"- {stop.stop_id}: {stop.stop_name}")

    print("\n最新车辆位置:")
    positions = VehiclePosition.query.order_by(VehiclePosition.timestamp.desc()).limit(5).all()
    for pos in positions:
        print(f"- 车辆 {pos.vehicle_id}: ({pos.latitude}, {pos.longitude}) at {pos.timestamp}")

    print("\n当前服务提醒:")
    alerts = ServiceAlert.query.filter(
        (ServiceAlert.active_period_end > datetime.now()) | 
        (ServiceAlert.active_period_end.is_(None))
    ).limit(5).all()
    for alert in alerts:
        print(f"- {alert.header_text}")
        print(f"  描述: {alert.description_text}")
        print(f"  开始时间: {alert.active_period_start}")
        if alert.active_period_end:
            print(f"  结束时间: {alert.active_period_end}")

if __name__ == '__main__':
    show_stats()
    show_examples() 