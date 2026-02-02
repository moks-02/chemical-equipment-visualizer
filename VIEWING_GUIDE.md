# How to View the Data Visualizations

The charts and visualizations are now displayed **directly in the website** using Chart.js. Here's how to see them:

## Prerequisites

1. **Backend Server Running**
   ```bash
   cd backend
   python manage.py runserver
   ```
   Should be running at: http://127.0.0.1:8000

2. **Frontend Server Running**
   ```bash
   cd frontend-web
   npm start
   ```
   Should open at: http://localhost:3000

## Steps to See Visualizations

### 1. Login/Register
- Open http://localhost:3000
- If you don't have an account, click "Don't have an account? Sign up" 
- Create an account or login with existing credentials

### 2. Upload Data
- Click on **"Upload Data"** tab in the sidebar
- Click **"Choose File"** and select your CSV file
  - Sample file location: `backend/chemical_equipment_data.csv`
- Click **"Upload and Analyze"**

### 3. View Visualizations
After upload completes, you'll automatically be taken to the **Dashboard** tab where you'll see:

#### Summary Statistics Cards
- Total Equipment Count
- Average Flowrate (with min-max range)
- Average Pressure (with min-max range)
- Average Temperature (with min-max range)

#### 5 Interactive Charts
1. **Pie Chart** - Equipment Type Distribution
2. **Bar Chart** - Equipment Count by Type
3. **Line Chart** - Equipment Parameters Trend (first 20 items)
   - Shows Flowrate, Pressure, Temperature trends
4. **Grouped Bar Chart** - Parameter Statistics (Avg, Min, Max)
5. **Scatter Plot** - Temperature vs Pressure Correlation

#### Data Table
- Complete data in tabular format with sorting

### 4. Switch Between Views
Use the sidebar to navigate:
- **Dashboard** - View uploaded data with all visualizations
- **Upload Data** - Upload new CSV files
- **History** - View and switch between your uploaded datasets (last 5)

## Features

✅ **No Preview Button** - All visualizations are inline
✅ **Interactive Charts** - Hover over charts to see detailed tooltips
✅ **Responsive Design** - Charts adapt to screen size
✅ **Real-time Updates** - Charts update immediately after upload
✅ **Dark Mode Toggle** - Switch themes using button in sidebar footer
✅ **Download PDF Report** - Generate PDF report for current dataset

## Chart Types Explained

- **Pie Chart**: Best for showing proportional distribution
- **Bar Charts**: Compare discrete categories and grouped values
- **Line Chart**: Show trends and patterns over sequence
- **Scatter Plot**: Reveal correlations between two variables

## Troubleshooting

If you don't see charts:
1. Make sure you've **uploaded a CSV file**
2. Check browser console (F12) for errors
3. Verify both backend and frontend servers are running
4. Try refreshing the page after upload
5. Make sure you're on the **Dashboard** tab, not Upload Data tab
