# Real-Time Manufacturing Status Dashboard

A comprehensive real-time dashboard that provides live insights into manufacturing processes, tracks key performance indicators (KPIs), and generates smart alerts to empower decision-makers with actionable insights for reducing downtime and optimizing operations.

![Manufacturing Dashboard](https://img.shields.io/badge/Status-Active-green) ![Python](https://img.shields.io/badge/Python-3.11-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)

## 🎯 Objectives

The goal of this project is to design and implement a real-time dashboard that:
- Provides live insights into manufacturing processes
- Tracks key performance indicators (KPIs) 
- Sends smart alerts when anomalies, delays, or breakdowns occur
- Empowers decision-makers, plant operators, and managers to quickly react to issues
- Reduces downtime and optimizes operations

## ✨ Key Features

### Real-Time Data Visualization
- **Live KPI Monitoring**: Overall Equipment Effectiveness (OEE), production counts, downtime, cycle times
- **Interactive Charts**: Line graphs, bar charts, heatmaps, and machine status indicators
- **Machine Status View**: Real-time status indicators (running, idle, error) for all production lines
- **Auto-refresh**: Configurable refresh intervals (5-60 seconds) for real-time updates

### Smart Alert System
- **Threshold Monitoring**: Configurable alerts for temperature, vibration, production rates, efficiency
- **Severity Levels**: Critical, Major, Warning, and Info alerts with visual indicators
- **Machine-Specific Alerts**: Individual machine monitoring with detailed status information
- **Alert History**: Track and analyze alert patterns over time

### Historical Data Analysis
- **Trend Analysis**: Compare performance across shifts, machines, and timeframes
- **Production Trends**: Daily production volume tracking with statistical summaries
- **Downtime Analysis**: Detailed breakdown of downtime events by machine and reason
- **Efficiency Comparison**: Machine-to-machine efficiency analysis and benchmarking

### User Interface
- **Responsive Design**: Clean, intuitive interface optimized for different screen sizes
- **Navigation**: Sidebar navigation with multiple dashboard views
- **Role-based Views**: Customizable dashboard layouts for different user roles
- **Interactive Controls**: Real-time filtering and configuration options

## 🛠️ Technology Stack

- **Frontend**: Streamlit for rapid dashboard development
- **Visualization**: Plotly for interactive charts and real-time graphics
- **Data Processing**: Pandas and NumPy for data manipulation and analysis
- **Backend Logic**: Python-based data generation and alert processing
- **Configuration**: TOML-based configuration management

## 📋 Prerequisites

- Python 3.11 or higher
- pip package manager

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/manufacturing-dashboard.git
   cd manufacturing-dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install streamlit plotly pandas numpy
   ```

3. **Configure the application:**
   ```bash
   mkdir -p .streamlit
   ```

4. **Run the dashboard:**
   ```bash
   streamlit run app.py --server.port 5000
   ```

5. **Access the dashboard:**
   Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
manufacturing-dashboard/
├── app.py                 # Main Streamlit application
├── data_generator.py      # Manufacturing data simulation
├── alert_system.py        # Alert monitoring and management
├── utils.py              # Utility functions and helpers
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── pyproject.toml        # Project dependencies
└── README.md             # Project documentation
```

## 🎮 Usage

### Dashboard Navigation

The dashboard includes four main views accessible via the sidebar:

1. **Overview**: High-level KPIs, production trends, and machine status summary
2. **Machine Status**: Detailed individual machine monitoring and performance metrics
3. **Historical Analysis**: Trend analysis, downtime reports, and efficiency comparisons
4. **Alerts & Settings**: Alert configuration, active alerts, and system status

### Key Metrics Monitored

- **Overall Equipment Effectiveness (OEE)**: Composite efficiency metric
- **Production Count**: Real-time production volume tracking
- **Downtime**: Machine downtime monitoring and analysis
- **Cycle Time**: Production cycle performance metrics
- **Temperature**: Machine temperature monitoring with thresholds
- **Vibration**: Equipment health monitoring via vibration analysis
- **Efficiency**: Individual machine efficiency tracking

### Alert Configuration

Navigate to "Alerts & Settings" to configure:
- Temperature thresholds (high/low)
- Vibration limits
- Production rate minimums
- Efficiency thresholds
- Alert notification preferences

## 📊 Data Simulation

The dashboard includes a sophisticated data generator that simulates:
- **6 Production Lines**: Press, Assembly, Welding, Paint, Packaging, and Quality stations
- **Realistic Patterns**: Time-of-day variations, shift patterns, and seasonal trends
- **Machine Parameters**: Individual machine characteristics and performance baselines
- **Downtime Events**: Realistic downtime scenarios with various causes
- **Alert Conditions**: Threshold breaches and anomaly detection

## 🔧 Configuration

### Streamlit Configuration (`.streamlit/config.toml`)
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

### Alert Thresholds
Default alert thresholds can be modified in the dashboard or programmatically:
- High Temperature: 75°C
- Low Temperature: 25°C
- High Vibration: 5.0 mm/s
- Low Production: 50 units/hour
- Low Efficiency: 70%

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py --server.port 5000
```

### Production Deployment
For production deployment, consider:
- Using environment variables for configuration
- Setting up proper logging and monitoring
- Implementing authentication and authorization
- Configuring SSL/TLS certificates
- Using a process manager like supervisor or systemd

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Future Enhancements

- **Real Data Integration**: Connect to actual manufacturing systems (MQTT, Kafka, REST APIs)
- **Predictive Analytics**: Machine learning models for predictive maintenance
- **Mobile App**: Native mobile application for on-the-go monitoring
- **Advanced Alerts**: Email, SMS, and Slack integration for notifications
- **Database Integration**: PostgreSQL/TimescaleDB for historical data storage
- **User Authentication**: Role-based access control and user management
- **Export Capabilities**: PDF reports and data export functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, questions, or feature requests:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation for troubleshooting guides

## 🏆 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for rapid web app development
- Visualization powered by [Plotly](https://plotly.com/)
- Data processing with [Pandas](https://pandas.pydata.org/) and [NumPy](https://numpy.org/)

---

**Real-Time Manufacturing Dashboard** - Empowering manufacturing excellence through data-driven insights.
