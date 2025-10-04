# 🌍 Iran Earthquake Data Monitor

[![Update Earthquake Data](https://github.com/asghariali1/Iran-Earthquake-Data/actions/workflows/update-earthquake-data.yml/badge.svg)](https://github.com/asghariali1/Iran-Earthquake-Data/actions/workflows/update-earthquake-data.yml)
[![Deploy to GitHub Pages](https://github.com/asghariali1/Iran-Earthquake-Data/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/asghariali1/Iran-Earthquake-Data/actions/workflows/deploy-pages.yml)

**Live Website:** [https://asghariali1.github.io/Iran-Earthquake-Data/](https://asghariali1.github.io/Iran-Earthquake-Data/)

An automated earthquake monitoring system that tracks and visualizes earthquake data for Iran and surrounding regions. The system automatically updates every 6 hours with the latest data from USGS.

## 🚀 Features

- **Real-time Updates**: Automatically fetches and updates earthquake data every 6 hours
- **Interactive Visualization**: Live map showing recent earthquakes with magnitude-based markers
- **Frequency Analysis**: Statistical analysis of earthquake frequency over time
- **GitHub Actions Automation**: Fully automated data pipeline using GitHub Actions
- **Mobile Responsive**: Works perfectly on desktop and mobile devices

## 📊 Data Sources

- **USGS Earthquake API**: Real-time earthquake data from the United States Geological Survey
- **Historical Data**: Comprehensive historical earthquake records for Iran region
- **Auto-generated Statistics**: Frequency counts and trends generated automatically

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python 3.9+
- **APIs**: USGS Earthquake API, Leaflet Maps
- **Automation**: GitHub Actions
- **Hosting**: GitHub Pages

## 📈 Auto-Update System

The system uses GitHub Actions to automatically:

1. **Fetch Latest Data**: Every 6 hours, fetch new earthquake data from USGS
2. **Update Database**: Merge new data with existing records
3. **Generate Statistics**: Create frequency counts and analysis
4. **Deploy Updates**: Automatically push changes to the live website

## 🗂️ File Structure

```
Iran-Earthquake-Data/
├── index.html              # Main website interface
├── script.js               # Frontend JavaScript logic
├── styles.css              # Website styling
├── data.json               # Main earthquake database
├── data.csv                # CSV format data
├── update_earthquake_data_github.py  # GitHub Actions updater
├── update_earthquake_data.py         # Local updater script
├── Frequency_counter.py     # Statistical analysis generator
├── server.py               # Local development server
├── earthquake_proxy.py     # API proxy server
└── .github/workflows/      # GitHub Actions automation
    ├── update-earthquake-data.yml
    └── deploy-pages.yml
```

## 🚀 Quick Start

### View Live Website
Simply visit: [https://asghariali1.github.io/Iran-Earthquake-Data/](https://asghariali1.github.io/Iran-Earthquake-Data/)

### Run Locally
```bash
# Clone the repository
git clone https://github.com/asghariali1/Iran-Earthquake-Data.git
cd Iran-Earthquake-Data

# Make scripts executable
chmod +x start_full_system.sh
chmod +x start_website.sh

# Start the full system (with auto-updates)
./start_full_system.sh

# Or just start the website
./start_website.sh
```

## 🔄 Manual Data Update

To manually update the earthquake data:

```bash
# Update with latest weekly data
python3 update_earthquake_data.py

# Generate new frequency statistics
python3 Frequency_counter.py
```

## 📱 Usage

1. **View Recent Earthquakes**: The map shows recent earthquakes with color-coded magnitude indicators
2. **Filter by Magnitude**: Use the controls to filter earthquakes by magnitude
3. **View Details**: Click on any earthquake marker to see detailed information
4. **Check Statistics**: View frequency analysis and trends in the sidebar

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **USGS**: For providing real-time earthquake data
- **Leaflet**: For the interactive mapping library
- **GitHub Actions**: For automated deployment and updates

---

**Note**: Data is automatically updated every 6 hours. For the most recent updates, check the GitHub Actions tab or the timestamp on the live website.