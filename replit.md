# Manufacturing Dashboard

## Overview

This is a real-time manufacturing status dashboard built with Streamlit that provides live insights into manufacturing processes, tracks key performance indicators (KPIs), and generates smart alerts when thresholds are breached. The system simulates a manufacturing environment with multiple production lines, monitoring equipment effectiveness, production counts, and machine health metrics to empower decision-makers with actionable insights for reducing downtime and optimizing operations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for rapid dashboard development
- **Visualization**: Plotly for interactive charts and graphs including real-time metrics, trend analysis, and machine status indicators
- **Layout**: Wide-layout configuration with sidebar navigation for settings and controls
- **Auto-refresh**: Configurable refresh intervals (5-60 seconds) for real-time data updates

### Backend Architecture
- **Data Generation**: Simulated manufacturing data with realistic patterns based on time-of-day variations and machine-specific parameters
- **Alert System**: Rule-based alert engine that monitors thresholds for temperature, vibration, production rates, efficiency, and OEE metrics
- **Session Management**: Streamlit session state for maintaining data generators, alert systems, and update timestamps
- **Modular Design**: Separated concerns with dedicated modules for data generation, alert processing, and utility functions

### Data Management
- **In-Memory Storage**: Real-time data stored in session state for immediate access
- **Data Simulation**: Realistic manufacturing scenarios with configurable machine parameters, shift patterns, and downtime reasons
- **Machine Modeling**: Individual machine configurations with base temperatures, production rates, and efficiency metrics
- **Historical Context**: Alert history tracking for trend analysis

### Key Components
- **Manufacturing Data Generator**: Simulates six production lines with realistic operational parameters
- **Alert System**: Configurable threshold monitoring with severity levels (Warning, Critical)
- **Utility Functions**: Helper functions for data formatting, status color mapping, OEE calculations, and shift information
- **Real-time Updates**: Automatic page refresh based on configurable intervals

## External Dependencies

### Python Libraries
- **Streamlit**: Web application framework for dashboard interface
- **Plotly**: Interactive visualization library for charts and graphs
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing for data generation algorithms
- **DateTime**: Time-based data handling and shift calculations

### Visualization Assets
- **External Images**: Factory imagery from Pixabay for dashboard header
- **Color Schemes**: Predefined color palettes for status indicators and chart themes

### Data Sources
- **Simulated Data**: No external data sources; uses algorithmic generation for realistic manufacturing scenarios
- **Time-based Patterns**: Incorporates shift schedules and production cycles for authentic operational behavior