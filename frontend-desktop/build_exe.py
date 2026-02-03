"""
Build script for creating executable for Chemical Equipment Visualizer Desktop App
This script uses PyInstaller to create a standalone Windows executable
"""

import os
import sys
import shutil
import subprocess

def build_executable():
    """Build the Windows executable using PyInstaller"""
    
    print("=" * 60)
    print("Building Chemical Equipment Visualizer Desktop App")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")
    
    # Clean previous builds
    print("\nCleaning previous builds...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Removed {dir_name}/")
    
    # Remove old spec file if exists
    if os.path.exists('ChemEquipVisualizer.spec'):
        os.remove('ChemEquipVisualizer.spec')
        print("  Removed old spec file")
    
    print("\n" + "=" * 60)
    print("Building executable with PyInstaller...")
    print("=" * 60)
    
    # PyInstaller command
    command = [
        'pyinstaller',
        '--name=ChemEquipVisualizer',
        '--windowed',  # No console window
        '--onefile',   # Single executable file
        '--icon=NONE', # You can add an icon file path here if you have one
        '--add-data=ui;ui',  # Include ui folder
        '--hidden-import=PyQt5',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=matplotlib',
        '--hidden-import=matplotlib.backends.backend_qt5agg',
        '--hidden-import=pandas',
        '--hidden-import=requests',
        '--collect-all=matplotlib',
        'main.py'
    ]
    
    try:
        subprocess.check_call(command)
        print("\n" + "=" * 60)
        print("✓ Build completed successfully!")
        print("=" * 60)
        print(f"\nExecutable location: {os.path.abspath('dist/ChemEquipVisualizer.exe')}")
        print(f"File size: {os.path.getsize('dist/ChemEquipVisualizer.exe') / (1024*1024):.2f} MB")
        
        # Copy to backend static folder for web download
        backend_static = os.path.join('..', 'backend', 'static', 'downloads')
        os.makedirs(backend_static, exist_ok=True)
        
        dest_file = os.path.join(backend_static, 'ChemEquipVisualizer.exe')
        shutil.copy2('dist/ChemEquipVisualizer.exe', dest_file)
        print(f"\n✓ Copied to backend static folder: {dest_file}")
        
        # Create a README for the download
        readme_path = os.path.join(backend_static, 'README.txt')
        with open(readme_path, 'w') as f:
            f.write("Chemical Equipment Parameter Visualizer - Desktop Application\n")
            f.write("=" * 60 + "\n\n")
            f.write("Installation Instructions:\n")
            f.write("-" * 60 + "\n")
            f.write("1. Download ChemEquipVisualizer.exe\n")
            f.write("2. Run the executable - no installation required!\n")
            f.write("3. The application will start automatically\n\n")
            f.write("System Requirements:\n")
            f.write("-" * 60 + "\n")
            f.write("- Windows 10 or later\n")
            f.write("- Internet connection (for API access)\n")
            f.write("- Minimum 4GB RAM recommended\n\n")
            f.write("Default Server:\n")
            f.write("-" * 60 + "\n")
            f.write("- http://localhost:8000\n")
            f.write("- Make sure the backend server is running\n\n")
            f.write("Version: 1.0.0\n")
        
        print(f"✓ Created README.txt")
        print("\n" + "=" * 60)
        print("Build process completed!")
        print("=" * 60)
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    build_executable()
