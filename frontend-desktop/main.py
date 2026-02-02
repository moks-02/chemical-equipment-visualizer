"""
Chemical Equipment Parameter Visualizer - Desktop Application
Main entry point for the PyQt5 desktop application
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from ui.login_window import LoginWindow

def main():
    """Initialize and run the application"""
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Inter", 10)
    app.setFont(font)
    
    # Set application metadata
    app.setApplicationName("ChemEquip Visualizer")
    app.setOrganizationName("ChemEquip")
    app.setApplicationVersion("1.0.0")
    
    # Create and show login window
    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
