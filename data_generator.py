import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import math

class ManufacturingDataGenerator:
    def __init__(self):
        self.machines = [
            "Line-A-Press-01", "Line-A-Assembly-02", "Line-B-Welding-03", 
            "Line-B-Paint-04", "Line-C-Packaging-05", "Quality-Station-06"
        ]
        self.base_time = datetime.now()
        
        # Realistic manufacturing parameters
        self.machine_configs = {
            "Line-A-Press-01": {"base_temp": 45, "base_production": 120, "base_efficiency": 85},
            "Line-A-Assembly-02": {"base_temp": 35, "base_production": 80, "base_efficiency": 90},
            "Line-B-Welding-03": {"base_temp": 65, "base_production": 60, "base_efficiency": 82},
            "Line-B-Paint-04": {"base_temp": 40, "base_production": 75, "base_efficiency": 88},
            "Line-C-Packaging-05": {"base_temp": 30, "base_production": 150, "base_efficiency": 92},
            "Quality-Station-06": {"base_temp": 25, "base_production": 200, "base_efficiency": 95}
        }
        
        # Downtime reasons
        self.downtime_reasons = [
            "Planned Maintenance", "Material Shortage", "Tool Change",
            "Quality Issue", "Machine Breakdown", "Setup/Changeover"
        ]

    def get_machine_list(self):
        return self.machines

    def generate_current_data(self):
        """Generate current overall manufacturing data"""
        # Time-based variations to simulate realistic patterns
        hour = datetime.now().hour
        day_factor = 0.8 + 0.4 * math.sin(2 * math.pi * hour / 24)  # Higher during day shift
        
        base_oee = 75 + 15 * day_factor + random.gauss(0, 3)
        base_oee = max(50, min(95, base_oee))  # Clamp between 50-95%
        
        return {
            'oee': base_oee,
            'oee_trend': random.gauss(0, 2),
            'availability': base_oee + random.gauss(5, 3),
            'performance': base_oee + random.gauss(2, 4),
            'quality': base_oee + random.gauss(8, 2),
            'production_count': int(1200 * day_factor + random.gauss(0, 100)),
            'production_trend': random.gauss(0, 50),
            'downtime_minutes': max(0, int(60 - 40 * day_factor + random.gauss(0, 15))),
            'downtime_trend': random.gauss(0, 10),
            'cycle_time': 45 + random.gauss(0, 5) - 10 * (day_factor - 0.5),
            'cycle_trend': random.gauss(0, 2)
        }

    def generate_machine_status(self, machine):
        """Generate current status for a specific machine"""
        config = self.machine_configs[machine]
        
        # Machine status determination
        status_rand = random.random()
        if status_rand < 0.15:
            status = "Error"
            efficiency = random.uniform(0, 30)
        elif status_rand < 0.25:
            status = "Idle"
            efficiency = random.uniform(0, 10)
        else:
            status = "Running"
            efficiency = config["base_efficiency"] + random.gauss(0, 8)
        
        efficiency = max(0, min(100, efficiency))
        
        return {
            'status': status,
            'efficiency': efficiency,
            'temperature': config["base_temp"] + random.gauss(0, 8),
            'vibration': abs(random.gauss(2.5, 1.0)),
            'production_rate': config["base_production"] + random.gauss(0, 15),
            'last_update': datetime.now()
        }

    def generate_machine_detail(self, machine):
        """Generate detailed data for a specific machine"""
        status_data = self.generate_machine_status(machine)
        config = self.machine_configs[machine]
        
        return {
            **status_data,
            'uptime_hours': random.uniform(120, 168),  # Hours in last week
            'total_production_today': int(config["base_production"] * 8 * random.uniform(0.7, 1.1)),
            'defect_rate': random.uniform(0.1, 3.0),
            'maintenance_due': random.randint(5, 45)  # Days
        }

    def generate_time_series_data(self, metric_type, hours=8, machine=None):
        """Generate time series data for charts"""
        timestamps = []
        values = []
        
        start_time = datetime.now() - timedelta(hours=hours)
        
        for i in range(hours * 12):  # Every 5 minutes
            timestamp = start_time + timedelta(minutes=i*5)
            timestamps.append(timestamp)
            
            # Time-based patterns
            hour_factor = 0.8 + 0.4 * math.sin(2 * math.pi * timestamp.hour / 24)
            noise = random.gauss(0, 0.1)
            
            if metric_type == 'production_rate':
                base_value = 100 * hour_factor
                value = base_value + base_value * noise
                if machine and machine in self.machine_configs:
                    value = self.machine_configs[machine]["base_production"] * (1 + noise)
            elif metric_type == 'temperature':
                base_value = 50 if not machine else self.machine_configs[machine]["base_temp"]
                value = base_value + 10 * noise + 5 * math.sin(2 * math.pi * i / 144)  # Daily cycle
            elif metric_type == 'vibration':
                base_value = 2.0
                value = abs(base_value + base_value * noise * 0.5)
            elif metric_type == 'efficiency':
                base_value = 85 * hour_factor
                value = base_value + base_value * noise * 0.1
                if machine and machine in self.machine_configs:
                    value = self.machine_configs[machine]["base_efficiency"] * (1 + noise * 0.1)
            else:
                value = 50 + 30 * hour_factor + 20 * noise
            
            values.append(max(0, value))
        
        return pd.DataFrame({
            'timestamp': timestamps,
            'value': values
        })

    def generate_production_cycles(self, machine, count=10):
        """Generate recent production cycles for a machine"""
        cycles = []
        base_time = datetime.now()
        
        config = self.machine_configs[machine]
        
        for i in range(count):
            start_time = base_time - timedelta(minutes=i*15 + random.randint(0, 10))
            cycle_time = 45 + random.gauss(0, 8)  # seconds
            end_time = start_time + timedelta(seconds=cycle_time)
            
            quality_score = random.uniform(85, 100)
            status = "Pass" if quality_score > 90 else "Inspect" if quality_score > 80 else "Fail"
            
            cycles.append({
                'Cycle': f"C{1000 + i}",
                'Start Time': start_time.strftime("%H:%M:%S"),
                'End Time': end_time.strftime("%H:%M:%S"),
                'Cycle Time (s)': f"{cycle_time:.1f}",
                'Quality Score': f"{quality_score:.1f}",
                'Status': status
            })
        
        return cycles

    def generate_historical_data(self, metric_type, days=7, machine=None):
        """Generate historical data for analysis"""
        dates = []
        values = []
        
        start_date = datetime.now().date() - timedelta(days=days)
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            dates.append(date)
            
            # Weekly patterns (lower on weekends)
            weekday_factor = 0.7 if date.weekday() >= 5 else 1.0
            trend_factor = 1 + (i / days) * 0.1  # Slight upward trend
            noise = random.gauss(0, 0.15)
            
            if metric_type == 'production':
                base_value = 8000 * weekday_factor * trend_factor
                value = int(base_value * (1 + noise))
            elif metric_type == 'efficiency':
                base_efficiency = 85 if not machine else self.machine_configs[machine]["base_efficiency"]
                value = base_efficiency * weekday_factor * trend_factor * (1 + noise * 0.1)
            elif metric_type == 'downtime':
                base_value = 120 / weekday_factor  # More downtime on weekends
                value = max(0, base_value * (1 + noise))
            else:
                value = 100 * weekday_factor * trend_factor * (1 + noise)
            
            values.append(max(0, value))
        
        return pd.DataFrame({
            'date': dates,
            'value': values
        })

    def generate_downtime_events(self, days=7):
        """Generate downtime events for analysis"""
        events = []
        
        # Generate 2-5 events per day
        for day in range(days):
            event_count = random.randint(1, 4)
            event_date = datetime.now().date() - timedelta(days=days-day)
            
            for _ in range(event_count):
                machine = random.choice(self.machines)
                reason = random.choice(self.downtime_reasons)
                duration = random.randint(5, 180)  # 5 minutes to 3 hours
                
                start_time = datetime.combine(event_date, datetime.min.time()) + timedelta(
                    hours=random.randint(6, 22),
                    minutes=random.randint(0, 59)
                )
                
                events.append({
                    'machine': machine,
                    'reason': reason,
                    'start_time': start_time.strftime("%Y-%m-%d %H:%M"),
                    'duration_minutes': duration,
                    'severity': 'Critical' if duration > 120 else 'Major' if duration > 60 else 'Minor'
                })
        
        return sorted(events, key=lambda x: x['start_time'], reverse=True)
