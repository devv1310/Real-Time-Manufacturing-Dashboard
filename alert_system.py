from datetime import datetime, timedelta
import random

class AlertSystem:
    def __init__(self):
        self.thresholds = {
            'temp_high': 75.0,
            'temp_low': 25.0,
            'vibration_high': 5.0,
            'production_low': 50,
            'efficiency_low': 70.0,
            'oee_low': 60.0
        }
        
        self.alert_history = []

    def update_thresholds(self, new_thresholds):
        """Update alert thresholds"""
        self.thresholds.update(new_thresholds)

    def check_alerts(self, current_data, machines, data_generator):
        """Check for alert conditions and return active alerts"""
        alerts = []
        
        # Check overall OEE
        if current_data['oee'] < self.thresholds['oee_low']:
            alerts.append({
                'severity': 'Critical',
                'title': 'Low Overall Equipment Effectiveness',
                'message': f"OEE has dropped to {current_data['oee']:.1f}%, below threshold of {self.thresholds['oee_low']}%",
                'machine': 'All Lines',
                'timestamp': datetime.now().strftime("%H:%M:%S"),
                'metric': 'OEE',
                'value': current_data['oee']
            })

        # Check individual machines
        for machine in machines:
            machine_status = data_generator.generate_machine_status(machine)
            
            # Temperature alerts
            if machine_status['temperature'] > self.thresholds['temp_high']:
                alerts.append({
                    'severity': 'Warning',
                    'title': 'High Temperature Alert',
                    'message': f"Temperature is {machine_status['temperature']:.1f}°C, exceeding {self.thresholds['temp_high']}°C threshold",
                    'machine': machine,
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'metric': 'Temperature',
                    'value': machine_status['temperature']
                })
            
            elif machine_status['temperature'] < self.thresholds['temp_low']:
                alerts.append({
                    'severity': 'Info',
                    'title': 'Low Temperature Alert',
                    'message': f"Temperature is {machine_status['temperature']:.1f}°C, below {self.thresholds['temp_low']}°C threshold",
                    'machine': machine,
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'metric': 'Temperature',
                    'value': machine_status['temperature']
                })

            # Vibration alerts
            if machine_status['vibration'] > self.thresholds['vibration_high']:
                alerts.append({
                    'severity': 'Critical',
                    'title': 'High Vibration Detected',
                    'message': f"Vibration level is {machine_status['vibration']:.2f}mm/s, exceeding safe threshold of {self.thresholds['vibration_high']}mm/s",
                    'machine': machine,
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'metric': 'Vibration',
                    'value': machine_status['vibration']
                })

            # Production rate alerts
            if machine_status['production_rate'] < self.thresholds['production_low']:
                alerts.append({
                    'severity': 'Warning',
                    'title': 'Low Production Rate',
                    'message': f"Production rate is {machine_status['production_rate']:.0f} units/hour, below target of {self.thresholds['production_low']}",
                    'machine': machine,
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'metric': 'Production Rate',
                    'value': machine_status['production_rate']
                })

            # Efficiency alerts
            if machine_status['efficiency'] < self.thresholds['efficiency_low']:
                alerts.append({
                    'severity': 'Major',
                    'title': 'Low Machine Efficiency',
                    'message': f"Machine efficiency is {machine_status['efficiency']:.1f}%, below acceptable threshold of {self.thresholds['efficiency_low']}%",
                    'machine': machine,
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'metric': 'Efficiency',
                    'value': machine_status['efficiency']
                })

            # Machine error status
            if machine_status['status'] == 'Error':
                alerts.append({
                    'severity': 'Critical',
                    'title': 'Machine Error Status',
                    'message': f"Machine is in error state and requires immediate attention",
                    'machine': machine,
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'metric': 'Status',
                    'value': machine_status['status']
                })

        # Randomly generate some alerts to simulate real conditions
        if random.random() < 0.3:  # 30% chance of additional alert
            sample_alerts = [
                {
                    'severity': 'Warning',
                    'title': 'Material Low',
                    'message': 'Raw material inventory is running low for Line-A',
                    'machine': 'Line-A-Press-01',
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'metric': 'Inventory',
                    'value': 'Low'
                },
                {
                    'severity': 'Info',
                    'title': 'Planned Maintenance Due',
                    'message': 'Scheduled maintenance window approaching in 2 hours',
                    'machine': 'Line-B-Welding-03',
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'metric': 'Maintenance',
                    'value': 'Due'
                },
                {
                    'severity': 'Major',
                    'title': 'Quality Check Required',
                    'message': 'Quality parameters showing deviation from specification',
                    'machine': 'Quality-Station-06',
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'metric': 'Quality',
                    'value': 'Deviation'
                }
            ]
            alerts.append(random.choice(sample_alerts))

        # Store in history
        for alert in alerts:
            self.alert_history.append({
                **alert,
                'created_at': datetime.now()
            })

        # Keep only recent alerts (last 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.alert_history = [alert for alert in self.alert_history if alert['created_at'] > cutoff_time]

        return alerts

    def get_alert_history(self, hours=24):
        """Get alert history for the specified number of hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [alert for alert in self.alert_history if alert['created_at'] > cutoff_time]

    def get_alert_summary(self):
        """Get summary of alerts by severity"""
        recent_alerts = self.get_alert_history(24)
        
        summary = {
            'Critical': len([a for a in recent_alerts if a['severity'] == 'Critical']),
            'Major': len([a for a in recent_alerts if a['severity'] == 'Major']),
            'Warning': len([a for a in recent_alerts if a['severity'] == 'Warning']),
            'Info': len([a for a in recent_alerts if a['severity'] == 'Info'])
        }
        
        return summary

    def acknowledge_alert(self, alert_id):
        """Mark an alert as acknowledged"""
        # In a real system, this would update the alert status in a database
        pass

    def clear_alerts(self, machine=None):
        """Clear alerts for a specific machine or all alerts"""
        if machine:
            self.alert_history = [alert for alert in self.alert_history if alert['machine'] != machine]
        else:
            self.alert_history = []
