# ChemEquip Desktop Application

Desktop frontend for the Chemical Equipment Parameter Visualizer built with PyQt5.

## Features

- **User Authentication**: Login and signup functionality
- **CSV Upload**: Upload chemical equipment data files
- **Data Visualization**: View interactive charts and graphs
  - Pie chart for equipment type distribution
  - Bar chart for equipment count by type
  - Line chart for parameter trends
- **Upload History**: View and manage all uploaded datasets
- **PDF Reports**: Download detailed PDF reports with charts
- **Dark Theme**: Modern dark UI matching the web frontend

## Installation

1. **Install Python Dependencies**:
   ```bash
   cd frontend-desktop
   pip install -r requirements.txt
   ```

2. **Ensure Backend is Running**:
   The desktop app connects to the Django backend at `http://localhost:8000`
   
   ```bash
   cd backend
   python manage.py runserver
   ```

## Running the Application

```bash
cd frontend-desktop
python main.py
```

## Project Structure

```
frontend-desktop/
├── main.py              # Application entry point
├── config.py            # Configuration settings
├── api_client.py        # API communication layer
├── requirements.txt     # Python dependencies
└── ui/                  # UI components
    ├── __init__.py
    ├── login_window.py  # Login/signup window
    ├── main_window.py   # Main application window
    ├── dashboard_tab.py # Dashboard with visualizations
    └── history_tab.py   # Upload history management
```

## Usage

### First Time Users

1. Launch the application
2. Click "Sign up" to create a new account
3. Enter username, email, and password
4. You'll be automatically logged in

### Uploading Data

1. Click "📁 Upload CSV" in the top toolbar
2. Select a CSV file with chemical equipment data
3. The dashboard will automatically display the analytics

### Viewing Data

- **Dashboard Tab**: Shows current dataset with:
  - Summary statistics
  - Equipment type distribution (pie chart)
  - Equipment count by type (bar chart)
  - Parameter trends (line chart)
  
- **History Tab**: Shows all uploaded datasets with options to:
  - View dataset in dashboard
  - Download PDF report
  - Delete dataset

### Downloading Reports

1. Click "📥 Download PDF" from the dashboard or history
2. Choose save location
3. PDF report includes all charts and data tables

## Requirements

- Python 3.8+
- PyQt5 5.15+
- matplotlib 3.8+
- requests 2.31+
- pandas 2.1+

## Color Theme

The desktop app uses the same color scheme as the web frontend:
- Primary: Red (#ef4444)
- Background: Dark (#0a0a0a, #141414, #1a1a1a)
- Text: White (#ffffff) and Gray (#9ca3af)

## API Configuration

The app connects to the backend API at `http://localhost:8000/api` by default.

To change this, edit `config.py`:

```python
API_BASE_URL = "http://your-server:port/api"
```

## Troubleshooting

### Connection Error
- Ensure the Django backend is running at `http://localhost:8000`
- Check that port 8000 is not blocked by firewall

### Login Failed
- Verify username and password are correct
- Ensure backend database has user account

### Upload Failed
- Check CSV file format matches expected structure
- Ensure file has required columns: Equipment Name, Type, Flowrate, Pressure, Temperature

## Support

For issues or questions, please refer to the main project documentation in the root README.md
