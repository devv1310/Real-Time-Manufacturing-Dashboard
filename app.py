import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
from data_generator import ManufacturingDataGenerator
from alert_system import AlertSystem
from utils import format_percentage, format_number, get_status_color

# Configure page
st.set_page_config(
    page_title="Manufacturing Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_generator' not in st.session_state:
    st.session_state.data_generator = ManufacturingDataGenerator()
if 'alert_system' not in st.session_state:
    st.session_state.alert_system = AlertSystem()
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# Auto-refresh functionality
refresh_interval = st.sidebar.selectbox(
    "Refresh Interval (seconds)",
    [5, 10, 30, 60],
    index=1
)

# Auto-refresh logic
if datetime.now() - st.session_state.last_update > timedelta(seconds=refresh_interval):
    st.session_state.last_update = datetime.now()
    st.rerun()

# Main header with factory image
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <img src="https://pixabay.com/get/g15add56cefd56fb274e0d219c3b26d4347a994bfdd4bd9b222f9e3aa51353096798ca852390d5b31884282d0408c0608581d118d4aa4da5dce84608bb826b3b6_1280.jpg" 
         style="width: 100%; height: 200px; object-fit: cover; border-radius: 10px;">
</div>
""", unsafe_allow_html=True)

st.title("🏭 Real-Time Manufacturing Dashboard")
st.markdown("---")

# Sidebar navigation
st.sidebar.title("Dashboard Navigation")
page = st.sidebar.selectbox(
    "Select View",
    ["Overview", "Machine Status", "Historical Analysis", "Alerts & Settings"]
)

# Get current data
current_data = st.session_state.data_generator.generate_current_data()
machines = st.session_state.data_generator.get_machine_list()

if page == "Overview":
    st.header("📊 Production Overview")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Overall Equipment Effectiveness (OEE)",
            format_percentage(current_data['oee']),
            delta=f"{current_data['oee_trend']:+.1f}%"
        )
    
    with col2:
        st.metric(
            "Production Count",
            format_number(current_data['production_count']),
            delta=f"{current_data['production_trend']:+.0f}"
        )
    
    with col3:
        st.metric(
            "Downtime (minutes)",
            format_number(current_data['downtime_minutes']),
            delta=f"{current_data['downtime_trend']:+.0f} min"
        )
    
    with col4:
        st.metric(
            "Cycle Time (seconds)",
            f"{current_data['cycle_time']:.1f}s",
            delta=f"{current_data['cycle_trend']:+.1f}s"
        )
    
    st.markdown("---")
    
    # Real-time charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Production Rate Trend")
        production_data = st.session_state.data_generator.generate_time_series_data('production_rate', hours=8)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=production_data['timestamp'],
            y=production_data['value'],
            mode='lines+markers',
            name='Production Rate',
            line=dict(color='#1f77b4', width=3)
        ))
        
        fig.update_layout(
            title="Units per Hour",
            xaxis_title="Time",
            yaxis_title="Units/Hour",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("OEE Breakdown")
        oee_data = {
            'Metric': ['Availability', 'Performance', 'Quality'],
            'Value': [current_data['availability'], current_data['performance'], current_data['quality']]
        }
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=oee_data['Metric'],
            y=oee_data['Value'],
            marker_color=['#2E86AB', '#A23B72', '#F18F01']
        ))
        
        fig.update_layout(
            title="OEE Components (%)",
            yaxis=dict(range=[0, 100]),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Machine overview table
    st.subheader("🔧 Machine Status Overview")
    machine_status_data = []
    for machine in machines:
        status_data = st.session_state.data_generator.generate_machine_status(machine)
        machine_status_data.append({
            'Machine': machine,
            'Status': status_data['status'],
            'Efficiency': f"{status_data['efficiency']:.1f}%",
            'Temperature': f"{status_data['temperature']:.1f}°C",
            'Vibration': f"{status_data['vibration']:.2f}mm/s",
            'Last Update': status_data['last_update'].strftime("%H:%M:%S")
        })
    
    df_status = pd.DataFrame(machine_status_data)
    
    # Color code the status column
    def color_status(val):
        color = get_status_color(val)
        return f'background-color: {color}; color: white; font-weight: bold;'
    
    styled_df = df_status.style.applymap(color_status, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True)

elif page == "Machine Status":
    st.header("🔧 Machine Status Detail")
    
    # Machine selector
    selected_machine = st.selectbox("Select Machine", machines)
    
    # Get detailed machine data
    machine_detail = st.session_state.data_generator.generate_machine_detail(selected_machine)
    
    # Machine status cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_color = get_status_color(machine_detail['status'])
        st.markdown(f"""
        <div style="padding: 1rem; border-radius: 10px; background-color: {status_color}; color: white; text-align: center;">
            <h3>Status</h3>
            <h2>{machine_detail['status']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Efficiency", f"{machine_detail['efficiency']:.1f}%")
    
    with col3:
        st.metric("Temperature", f"{machine_detail['temperature']:.1f}°C")
    
    with col4:
        st.metric("Vibration", f"{machine_detail['vibration']:.2f}mm/s")
    
    st.markdown("---")
    
    # Machine performance charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Temperature Trend")
        temp_data = st.session_state.data_generator.generate_time_series_data('temperature', hours=4, machine=selected_machine)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=temp_data['timestamp'],
            y=temp_data['value'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#ff7f0e', width=3)
        ))
        
        # Add threshold lines
        fig.add_hline(y=75, line_dash="dash", line_color="red", annotation_text="High Temp Threshold")
        fig.add_hline(y=25, line_dash="dash", line_color="blue", annotation_text="Low Temp Threshold")
        
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Temperature (°C)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Vibration Analysis")
        vibration_data = st.session_state.data_generator.generate_time_series_data('vibration', hours=4, machine=selected_machine)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=vibration_data['timestamp'],
            y=vibration_data['value'],
            mode='lines+markers',
            name='Vibration',
            line=dict(color='#2ca02c', width=3)
        ))
        
        fig.add_hline(y=5.0, line_dash="dash", line_color="red", annotation_text="High Vibration Threshold")
        
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Vibration (mm/s)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Production cycles
    st.subheader("Recent Production Cycles")
    cycles_data = st.session_state.data_generator.generate_production_cycles(selected_machine)
    df_cycles = pd.DataFrame(cycles_data)
    st.dataframe(df_cycles, use_container_width=True)

elif page == "Historical Analysis":
    st.header("📈 Historical Data Analysis")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now().date() - timedelta(days=7))
    with col2:
        end_date = st.date_input("End Date", datetime.now().date())
    
    # Analysis type selector
    analysis_type = st.selectbox(
        "Analysis Type",
        ["Production Trends", "Downtime Analysis", "Efficiency Comparison", "Quality Metrics"]
    )
    
    if analysis_type == "Production Trends":
        st.subheader("Production Volume Over Time")
        
        # Generate historical production data
        days = (end_date - start_date).days
        historical_data = st.session_state.data_generator.generate_historical_data('production', days)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=historical_data['date'],
            y=historical_data['value'],
            mode='lines+markers',
            name='Daily Production',
            fill='tonexty'
        ))
        
        fig.update_layout(
            title="Daily Production Volume",
            xaxis_title="Date",
            yaxis_title="Units Produced",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Daily Production", f"{historical_data['value'].mean():.0f}")
        with col2:
            st.metric("Peak Production Day", f"{historical_data['value'].max():.0f}")
        with col3:
            st.metric("Total Production", f"{historical_data['value'].sum():.0f}")
    
    elif analysis_type == "Downtime Analysis":
        st.subheader("Downtime Events Analysis")
        
        # Generate downtime events
        downtime_events = st.session_state.data_generator.generate_downtime_events(days=(end_date - start_date).days)
        df_downtime = pd.DataFrame(downtime_events)
        
        # Downtime by machine
        fig = px.bar(df_downtime, x='machine', y='duration_minutes', color='reason',
                    title="Downtime by Machine and Reason")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Downtime events table
        st.subheader("Recent Downtime Events")
        st.dataframe(df_downtime, use_container_width=True)
    
    elif analysis_type == "Efficiency Comparison":
        st.subheader("Machine Efficiency Comparison")
        
        # Generate efficiency data for all machines
        efficiency_data = []
        for machine in machines:
            eff_data = st.session_state.data_generator.generate_historical_data('efficiency', days=(end_date - start_date).days, machine=machine)
            for i, row in eff_data.iterrows():
                efficiency_data.append({
                    'Date': row['date'],
                    'Machine': machine,
                    'Efficiency': row['value']
                })
        
        df_efficiency = pd.DataFrame(efficiency_data)
        
        # Line chart comparing efficiency
        fig = px.line(df_efficiency, x='Date', y='Efficiency', color='Machine',
                     title="Machine Efficiency Trends")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Average efficiency by machine
        avg_efficiency = df_efficiency.groupby('Machine')['Efficiency'].mean().reset_index()
        fig_bar = px.bar(avg_efficiency, x='Machine', y='Efficiency',
                        title="Average Efficiency by Machine")
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

elif page == "Alerts & Settings":
    st.header("🚨 Alert System & Settings")
    
    # Alert configuration
    st.subheader("Alert Thresholds")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Temperature Alerts**")
        temp_high = st.number_input("High Temperature Threshold (°C)", value=75.0, step=1.0)
        temp_low = st.number_input("Low Temperature Threshold (°C)", value=25.0, step=1.0)
        
        st.write("**Production Alerts**")
        prod_low = st.number_input("Low Production Threshold (units/hour)", value=50, step=5)
        
    with col2:
        st.write("**Vibration Alerts**")
        vib_high = st.number_input("High Vibration Threshold (mm/s)", value=5.0, step=0.1)
        
        st.write("**Efficiency Alerts**")
        eff_low = st.number_input("Low Efficiency Threshold (%)", value=70.0, step=1.0)
    
    if st.button("Update Alert Thresholds"):
        st.session_state.alert_system.update_thresholds({
            'temp_high': temp_high,
            'temp_low': temp_low,
            'vibration_high': vib_high,
            'production_low': prod_low,
            'efficiency_low': eff_low
        })
        st.success("Alert thresholds updated successfully!")
    
    st.markdown("---")
    
    # Active alerts
    st.subheader("🔔 Active Alerts")
    
    # Check for alerts based on current data
    alerts = st.session_state.alert_system.check_alerts(current_data, machines, st.session_state.data_generator)
    
    if alerts:
        for alert in alerts:
            alert_color = "red" if alert['severity'] == "Critical" else "orange" if alert['severity'] == "Warning" else "blue"
            st.markdown(f"""
            <div style="padding: 1rem; border-left: 5px solid {alert_color}; background-color: rgba(255,0,0,0.1); margin: 0.5rem 0;">
                <strong>{alert['severity']}: {alert['title']}</strong><br>
                {alert['message']}<br>
                <small>Machine: {alert['machine']} | Time: {alert['timestamp']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No active alerts - All systems operating normally")
    
    st.markdown("---")
    
    # System status
    st.subheader("🔧 System Status")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Data Sources", "5/5 Connected", delta="All Online")
    with col2:
        st.metric("Last Data Update", st.session_state.last_update.strftime("%H:%M:%S"))
    with col3:
        st.metric("Alert System", "Active", delta="Monitoring")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    Manufacturing Dashboard v1.0 | Real-time monitoring and analytics
    <br>
    <img src="https://pixabay.com/get/gabbd38805a28e0f9603932b0cffd22bcfe577abbb35d113186e11fb126cc802a61a233a00986eefe035ce87cb7b9e7ef5fd80e9c32462eb144c37ee65c19f639_1280.jpg" 
         style="width: 100%; max-width: 400px; height: 100px; object-fit: cover; margin-top: 1rem; border-radius: 5px;">
</div>
""", unsafe_allow_html=True)

# Auto-refresh indicator
with st.sidebar:
    st.markdown("---")
    st.info(f"⏱️ Auto-refresh: {refresh_interval}s\n\nLast updated: {st.session_state.last_update.strftime('%H:%M:%S')}")
