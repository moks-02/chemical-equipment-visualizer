# Chemical Equipment Parameter Visualizer

A hybrid Web + Desktop application for visualizing and analyzing chemical equipment data.

## Project Overview

This application allows users to upload CSV files containing chemical equipment data (Equipment Name, Type, Flowrate, Pressure, Temperature). It provides data visualization and analytics through both a React web interface and a PyQt5 desktop application, both connected to a Django REST API backend.

## Tech Stack

### Backend
- **Framework**: Django 6.0.1 + Django REST Framework 3.16.1
- **Database**: SQLite
- **Data Processing**: Pandas 3.0.0
- **PDF Generation**: ReportLab 4.4.9
- **CORS**: django-cors-headers 4.9.0

### Frontend (Web)
- **Framework**: React.js + Chart.js
- **Purpose**: Web-based interface with interactive charts

### Frontend (Desktop)
- **Framework**: PyQt5 + Matplotlib
- **Purpose**: Desktop application with same visualization capabilities

## Project Structure

```
chemical-equipment-visualizer/
├── backend/                    # Django REST API
│   ├── venv/                  # Python virtual environment
│   ├── config/                # Django project settings
│   ├── api/                   # API app
│   ├── manage.py              # Django management script
│   └── requirements.txt       # Python dependencies
├── frontend-web/              # React application (to be created)
├── frontend-desktop/          # PyQt5 application (to be created)
├── sample_equipment_data.csv  # Sample CSV file (to be created)
└── README.md                  # This file
```

## Setup Instructions

### Backend Setup (Phase 1 - ✅ COMPLETED)

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Activate virtual environment:
   ```bash
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. Install dependencies (already installed):
   ```bash
   pip install -r requirements.txt
   ```

4. Installed packages:
   - Django 6.0.1
   - Django REST Framework 3.16.1
   - django-cors-headers 4.9.0
   - pandas 3.0.0
   - reportlab 4.4.9
   - pillow 12.1.0

## Key Features (To Be Implemented)

- ✅ CSV Upload – Web and Desktop upload to backend
- ✅ Data Summary API – Total count, averages, type distribution
- ✅ Visualization – Chart.js (Web) and Matplotlib (Desktop)
- ✅ History Management – Store last 5 uploaded datasets
- ✅ PDF Report Generation
- ✅ Basic Authentication

## Development Status

- ✅ **Phase 1: Project Setup** - COMPLETED
  - Project structure created
  - Backend virtual environment set up
  - Django project and API app initialized
  - All dependencies installed

- 🔄 **Phase 2: Backend Development** - NEXT
  - Configure Django settings
  - Create database models
  - Implement REST API endpoints
  - Set up data processing logic

- ⏳ **Phase 3: Frontend Web Development** - PENDING
- ⏳ **Phase 4: Frontend Desktop Development** - PENDING
- ⏳ **Phase 5: Advanced Features** - PENDING
- ⏳ **Phase 6: Testing & Integration** - PENDING

## Next Steps

1. Configure Django settings (add DRF, CORS, apps to INSTALLED_APPS)
2. Create database models for UploadedDataset
3. Implement API views and serializers
4. Run migrations and test backend

## License

For intern screening task purposes.
