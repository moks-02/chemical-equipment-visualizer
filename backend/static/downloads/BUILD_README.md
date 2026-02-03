# Desktop Application Build and Distribution

This directory contains the downloadable desktop application executable.

## Building the Desktop Application

To build the desktop application executable:

1. Navigate to the frontend-desktop directory:
   ```bash
   cd frontend-desktop
   ```

2. Run the build script:
   ```bash
   python build_exe.py
   ```

3. The script will:
   - Install PyInstaller if not already installed
   - Clean previous builds
   - Build a standalone executable using PyInstaller
   - Copy the executable to `backend/static/downloads/`
   - Create a README.txt with installation instructions

## File Size

The executable is approximately 79 MB and contains:
- Python runtime
- PyQt5 libraries
- Matplotlib and dependencies
- Pandas and NumPy
- All application code

## Distribution

The executable is served through the Django backend API at:
- Info endpoint: `GET /api/download/desktop-app/info/`
- Download endpoint: `GET /api/download/desktop-app/`

Users can download it from the web interface by clicking the "Download App" tab in the sidebar.

## Git Considerations

The executable file is excluded from version control via `.gitignore` due to its large size. 
To distribute the application, you should:
1. Build it on the target deployment server
2. Or use a separate file hosting service (S3, CDN, etc.)
3. Update the backend API to point to the hosted location

## Security Note

The executable is a standalone Windows application that requires:
- Windows 10 or later
- Network access to the backend API server
- User credentials for authentication

The application communicates with the backend server specified during login (default: http://localhost:8000).
