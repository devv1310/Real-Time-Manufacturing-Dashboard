def format_percentage(value):
    """Format a number as a percentage string"""
    return f"{value:.1f}%"

def format_number(value):
    """Format a number with appropriate thousand separators"""
    if isinstance(value, float):
        return f"{value:,.1f}"
    else:
        return f"{value:,}"

def get_status_color(status):
    """Return color code based on machine status"""
    color_map = {
        'Running': '#28a745',  # Green
        'Idle': '#ffc107',     # Yellow
        'Error': '#dc3545',    # Red
        'Maintenance': '#6c757d',  # Gray
        'Offline': '#343a40'   # Dark gray
    }
    return color_map.get(status, '#6c757d')

def calculate_oee(availability, performance, quality):
    """Calculate Overall Equipment Effectiveness"""
    return (availability / 100) * (performance / 100) * (quality / 100) * 100

def get_shift_info():
    """Get current shift information"""
    from datetime import datetime
    
    hour = datetime.now().hour
    
    if 6 <= hour < 14:
        return "Day Shift", "06:00 - 14:00"
    elif 14 <= hour < 22:
        return "Evening Shift", "14:00 - 22:00"
    else:
        return "Night Shift", "22:00 - 06:00"

def format_duration(minutes):
    """Format duration from minutes to human readable format"""
    if minutes < 60:
        return f"{minutes:.0f} min"
    else:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:.0f}h {mins:.0f}m"

def generate_color_palette(n_colors):
    """Generate a color palette for charts"""
    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]
    
    if n_colors <= len(colors):
        return colors[:n_colors]
    else:
        # Generate additional colors if needed
        import matplotlib.cm as cm
        import numpy as np
        additional_colors = cm.Set3(np.linspace(0, 1, n_colors - len(colors)))
        return colors + [f"rgba({int(r*255)},{int(g*255)},{int(b*255)},1)" for r, g, b, a in additional_colors]

def validate_threshold(value, min_val=None, max_val=None):
    """Validate threshold values"""
    if min_val is not None and value < min_val:
        return False, f"Value must be at least {min_val}"
    if max_val is not None and value > max_val:
        return False, f"Value must be at most {max_val}"
    return True, "Valid"

def format_timestamp(timestamp):
    """Format timestamp for display"""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def calculate_availability(uptime_hours, total_hours):
    """Calculate machine availability percentage"""
    if total_hours == 0:
        return 0
    return (uptime_hours / total_hours) * 100

def get_machine_category(machine_name):
    """Get machine category from machine name"""
    if "Press" in machine_name:
        return "Press"
    elif "Assembly" in machine_name:
        return "Assembly"
    elif "Welding" in machine_name:
        return "Welding"
    elif "Paint" in machine_name:
        return "Finishing"
    elif "Packaging" in machine_name:
        return "Packaging"
    elif "Quality" in machine_name:
        return "Quality Control"
    else:
        return "General"
