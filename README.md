# ChemEquip Visualizer

A comprehensive chemical equipment parameter visualization system with web and desktop interfaces for analyzing and visualizing chemical equipment data.

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** (for backend and desktop app)
- **Node.js 16+** (for web frontend)
- **Git** (for cloning the repository)

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd chemical-equipment-visualizer
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```
   Backend will run on: http://localhost:8000

3. **Web Frontend Setup**
   ```bash
   cd frontend-web
   npm install
   npm start
   ```
   Web app will run on: http://localhost:3000

4. **Desktop App (Optional)**
   ```bash
   cd frontend-desktop
   # Ensure backend virtual environment is active
   pip install -r requirements.txt
   python main.py
   ```

## 📁 Project Structure

```
chemical-equipment-visualizer/
├── backend/                 # Django REST API
│   ├── api/                # API endpoints and logic
│   ├── config/             # Django settings
│   ├── static/downloads/   # Desktop app downloads
│   ├── manage.py
│   └── requirements.txt
├── frontend-web/           # React web application
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
├── frontend-desktop/       # PyQt5 desktop application
│   ├── ui/                 # Desktop UI components
│   ├── main.py
│   ├── build_exe.py        # Executable builder
│   └── requirements.txt
└── README.md              # This file
```

## 🔧 Features

### Web Application
- **Interactive Dashboard** - Real-time data visualization
- **CSV Upload** - Import equipment data files
- **Data Filtering** - Filter by equipment type, flowrate, pressure, temperature
- **Charts & Analytics** - Pie charts, bar charts, line graphs, scatter plots
- **PDF Reports** - Generate downloadable analysis reports
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Desktop App Download** - Get standalone desktop version

### Desktop Application
- **Offline Analysis** - Work without internet connection
- **Native Performance** - Fast data processing
- **Same Features** - All web features in desktop format
- **PDF Generation** - Create reports locally

### Backend API
- **RESTful API** - Clean, documented endpoints
- **User Authentication** - Token-based authentication
- **Data Management** - Upload, store, and retrieve datasets
- **Report Generation** - Server-side PDF creation

## 🔐 Default Authentication

**Default Login Credentials:**
- Username: `admin`
- Password: `admin123`

You can create additional users through the Django admin interface or API.

## 📊 Supported Data Format

Upload CSV files with the following columns:
- `Equipment Name` - Name of the equipment
- `Type` - Equipment type (Reactor, Heat Exchanger, Pump, etc.)
- `Flowrate` - Numeric flowrate value
- `Pressure` - Numeric pressure value  
- `Temperature` - Numeric temperature value

## 🛠 Development

### Running Tests
```bash
# Backend API tests
cd backend
python test_api.py

# Frontend tests
cd frontend-web
npm test
```

### Building Desktop App
```bash
cd frontend-desktop
python build_exe.py
```
This creates a standalone executable in the `dist/` folder.

### Environment Variables
Create a `.env` file in the backend directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🚀 Deployment

### Web Application
1. Set `DEBUG=False` in Django settings
2. Configure static files and database for production
3. Deploy backend to your server (Heroku, AWS, etc.)
4. Build React app: `npm run build`
5. Serve built files from your web server

### Desktop Application
1. Run `python build_exe.py` to create executable
2. Distribute the `.exe` file to users
3. Users can download directly from the web interface

## 🔍 Usage

1. **Start the Backend**: Run Django server on port 8000
2. **Access Web App**: Open browser to http://localhost:3000
3. **Login**: Use default credentials or create account
4. **Upload Data**: Go to Upload tab and select CSV file
5. **View Analytics**: Explore dashboard with charts and filters
6. **Generate Reports**: Download PDF reports
7. **Get Desktop App**: Use Download tab to get offline version

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
- Ensure Python virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`
- Run migrations: `python manage.py migrate`

**Frontend won't start:**
- Clear cache: `npm cache clean --force`
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version`

**Desktop app won't run:**
- Ensure backend server is running on port 8000
- Check server URL in desktop app settings
- Verify network connectivity

**CORS Issues:**
- Backend includes CORS headers for localhost:3000
- For production, update `CORS_ALLOWED_ORIGINS` in Django settings

### Performance Tips
- Limit CSV file size to < 50MB for optimal performance
- Use filtering to work with large datasets
- Desktop app provides better performance for large files

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review API documentation in the backend
3. Create an issue in the repository
4. Contact the development team

---

**Version:** 1.0.0  
**Last Updated:** February 2025

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
