"""
Main Application Window
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTabWidget, QMessageBox,
                             QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from api_client import APIClient
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT
from ui.dashboard_tab import DashboardTab
from ui.history_tab import HistoryTab


class MainWindow(QMainWindow):
    """Main application window with tabs"""
    
    def __init__(self, api_client: APIClient, username: str):
        super().__init__()
        self.api_client = api_client
        self.username = username
        self.current_dataset = None
        self.init_ui()
        self.load_initial_data()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("ChemEquip - Chemical Equipment Visualizer")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['bg_primary']};
            }}
            QWidget {{
                background-color: {COLORS['bg_primary']};
                color: {COLORS['text_primary']};
            }}
            QTabWidget::pane {{
                border: 1px solid {COLORS['border']};
                background-color: {COLORS['bg_primary']};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_secondary']};
                padding: 14px 32px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                min-width: 120px;
            }}
            QTabBar::tab:selected {{
                background-color: {COLORS['bg_primary']};
                color: {COLORS['primary']};
                border-bottom: 2px solid {COLORS['primary']};
            }}
            QTabBar::tab:hover {{
                background-color: {COLORS['bg_hover']};
            }}
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: #dc2626;
            }}
            QPushButton:pressed {{
                background-color: #b91c1c;
            }}
            QPushButton#secondary {{
                background-color: {COLORS['bg_tertiary']};
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['border']};
            }}
            QPushButton#secondary:hover {{
                background-color: {COLORS['bg_hover']};
                border: 2px solid {COLORS['primary']};
            }}
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Title
        title_layout = QVBoxLayout()
        title_label = QLabel("ChemEquip")
        title_label.setFont(QFont("Inter", 24, QFont.Bold))
        title_label.setStyleSheet(f"color: {COLORS['primary']};")
        title_layout.addWidget(title_label)
        
        subtitle = QLabel("Chemical Equipment Parameter Visualizer")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # User info and actions
        user_label = QLabel(f"👤 {self.username}")
        user_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px; margin-right: 15px;")
        header_layout.addWidget(user_label)
        
        upload_btn = QPushButton("📁 Upload CSV")
        upload_btn.clicked.connect(self.handle_upload)
        header_layout.addWidget(upload_btn)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("secondary")
        logout_btn.clicked.connect(self.handle_logout)
        header_layout.addWidget(logout_btn)
        
        main_layout.addLayout(header_layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Dashboard tab
        self.dashboard_tab = DashboardTab(self.api_client, self)
        self.tabs.addTab(self.dashboard_tab, "📊 Dashboard")
        
        # History tab
        self.history_tab = HistoryTab(self.api_client, self)
        self.tabs.addTab(self.history_tab, "📝 History")
        
        main_layout.addWidget(self.tabs)
        
        central_widget.setLayout(main_layout)
    
    def load_initial_data(self):
        """Load initial data (most recent dataset)"""
        result = self.api_client.get_datasets()
        
        if result['success'] and result['data']:
            datasets = result['data']
            if datasets:
                # Load most recent dataset
                most_recent = datasets[0]
                self.load_dataset(most_recent['id'])
    
    def handle_upload(self):
        """Handle CSV file upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            try:
                # Check if file exists and is readable
                import os
                if not os.path.exists(file_path):
                    QMessageBox.critical(
                        self,
                        "File Error",
                        "Selected file does not exist."
                    )
                    return
                
                result = self.api_client.upload_dataset(file_path)
                
                if result['success']:
                    QMessageBox.information(
                        self,
                        "Success",
                        "Dataset uploaded successfully!"
                    )
                    # Load the new dataset
                    dataset_id = result['data'].get('id')
                    if dataset_id:
                        self.load_dataset(dataset_id)
                    # Refresh history
                    self.history_tab.load_history()
                else:
                    error_msg = result.get('error', 'Upload failed')
                    # Try to extract more details from error
                    if 'response' in str(error_msg):
                        try:
                            import json
                            error_data = json.loads(error_msg)
                            error_msg = error_data.get('detail', error_msg)
                        except:
                            pass
                    QMessageBox.critical(
                        self,
                        "Upload Failed",
                        f"Error: {error_msg}\n\nPlease ensure:\n- Backend server is running\n- You are logged in\n- File is a valid CSV"
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to upload file: {str(e)}\n\nPlease check:\n- Backend is running at http://localhost:8000\n- File is accessible"
                )
    
    def load_dataset(self, dataset_id: int):
        """Load dataset details and update dashboard"""
        result = self.api_client.get_dataset_detail(dataset_id)
        
        if result['success']:
            self.current_dataset = result['data']
            self.dashboard_tab.display_dataset(self.current_dataset)
            # Switch to dashboard tab
            self.tabs.setCurrentIndex(0)
        else:
            error_msg = result.get('error', 'Failed to load dataset')
            QMessageBox.warning(
                self,
                "Error",
                f"Could not load dataset: {error_msg}"
            )
    
    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.api_client.clear_token()
            
            # Show login window
            from ui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            
            self.close()
