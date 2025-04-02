import sys
import os
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import create_app, db
from backend.models import (
    Route, Stop, Trip, StopTime,
    TripUpdate, StopTimeUpdate, VehiclePosition, ServiceAlert
)

def show_stats():
    """显示数据库统计信息"""
    app = create_app()
    with app.app_context():
        # 静态数据统计
        print("\n=== 静态数据统计 ===")
        print(f"路线数量: {Route.query.count()}")
        print(f"站点数量: {Stop.query.count()}")
        print(f"行程数量: {Trip.query.count()}")
        print(f"时刻表条目数量: {StopTime.query.count()}")
        
        # 实时数据统计
        print("\n=== 实时数据统计 ===")
        print(f"行程更新数量: {TripUpdate.query.count()}")
        print(f"站点时间更新数量: {StopTimeUpdate.query.count()}")
        print(f"车辆位置数量: {VehiclePosition.query.count()}")
        print(f"服务提醒数量: {ServiceAlert.query.count()}")
        
        # 显示一些示例数据
        print("\n=== 路线示例 ===")
        for route in Route.query.limit(5).all():
            print(f"路线 {route.route_id}: {route.route_long_name or route.route_short_name}")
        
        print("\n=== 站点示例 ===")
        for stop in Stop.query.limit(5).all():
            print(f"站点 {stop.stop_id}: {stop.stop_name} ({stop.stop_lat}, {stop.stop_lon})")
        
        print("\n=== 最新车辆位置 ===")
        for pos in VehiclePosition.query.order_by(VehiclePosition.timestamp.desc()).limit(5).all():
            print(f"车辆 {pos.vehicle_id}: 位置 ({pos.latitude}, {pos.longitude}), 时间: {pos.timestamp}")
        
        print("\n=== 当前服务提醒 ===")
        for alert in ServiceAlert.query.filter(
            (ServiceAlert.active_period_end > datetime.now()) | 
            (ServiceAlert.active_period_end.is_(None))
        ).limit(5).all():
            print(f"提醒: {alert.header_text}")

if __name__ == '__main__':
    show_stats() 