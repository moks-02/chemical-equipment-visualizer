"""
Login and Signup Window
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QStackedWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from api_client import APIClient
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT


class LoginWindow(QWidget):
    """Main login/signup window"""
    
    login_successful = pyqtSignal(str, str)  # Signal emits (token, username)
    
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("ChemEquip - Login")
        self.setFixedSize(500, 600)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_primary']};
                color: {COLORS['text_primary']};
            }}
            QLineEdit {{
                background-color: {COLORS['bg_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                color: {COLORS['text_primary']};
            }}
            QLineEdit:focus {{
                border: 1px solid {COLORS['primary']};
            }}
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
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
            }}
            QPushButton#secondary:hover {{
                background-color: {COLORS['bg_hover']};
            }}
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(60, 40, 60, 40)
        
        # Logo/Title
        title = QLabel("ChemEquip")
        title.setFont(QFont("Inter", 32, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['primary']};")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        subtitle = QLabel("Chemical Equipment Visualizer")
        subtitle.setFont(QFont("Inter", 12))
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; margin-bottom: 30px;")
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)
        
        # Stacked widget for login/signup forms
        self.stacked_widget = QStackedWidget()
        
        # Login form
        login_widget = self.create_login_form()
        self.stacked_widget.addWidget(login_widget)
        
        # Signup form
        signup_widget = self.create_signup_form()
        self.stacked_widget.addWidget(signup_widget)
        
        main_layout.addWidget(self.stacked_widget)
        
        self.setLayout(main_layout)
    
    def create_login_form(self):
        """Create login form widget"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Username field
        username_label = QLabel("Username")
        username_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        layout.addWidget(username_label)
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        layout.addWidget(self.login_username)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px; margin-top: 10px;")
        layout.addWidget(password_label)
        
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.returnPressed.connect(self.handle_login)
        layout.addWidget(self.login_password)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        login_btn.setMinimumHeight(45)
        layout.addWidget(login_btn)
        
        # Signup link
        signup_layout = QHBoxLayout()
        signup_layout.setAlignment(Qt.AlignCenter)
        signup_label = QLabel("Don't have an account?")
        signup_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        signup_layout.addWidget(signup_label)
        
        signup_link = QPushButton("Sign up")
        signup_link.setObjectName("secondary")
        signup_link.setFlat(True)
        signup_link.setStyleSheet(f"""
            QPushButton#secondary {{
                background-color: transparent;
                color: {COLORS['primary']};
                text-decoration: underline;
                padding: 5px;
            }}
            QPushButton#secondary:hover {{
                color: #dc2626;
            }}
        """)
        signup_link.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        signup_layout.addWidget(signup_link)
        
        layout.addLayout(signup_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_signup_form(self):
        """Create signup form widget"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Username field
        username_label = QLabel("Username")
        username_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        layout.addWidget(username_label)
        
        self.signup_username = QLineEdit()
        self.signup_username.setPlaceholderText("Choose a username")
        layout.addWidget(self.signup_username)
        
        # Email field
        email_label = QLabel("Email")
        email_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px; margin-top: 10px;")
        layout.addWidget(email_label)
        
        self.signup_email = QLineEdit()
        self.signup_email.setPlaceholderText("Enter your email")
        layout.addWidget(self.signup_email)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px; margin-top: 10px;")
        layout.addWidget(password_label)
        
        self.signup_password = QLineEdit()
        self.signup_password.setPlaceholderText("Choose a password")
        self.signup_password.setEchoMode(QLineEdit.Password)
        self.signup_password.returnPressed.connect(self.handle_signup)
        layout.addWidget(self.signup_password)
        
        # Signup button
        signup_btn = QPushButton("Sign Up")
        signup_btn.clicked.connect(self.handle_signup)
        signup_btn.setMinimumHeight(45)
        layout.addWidget(signup_btn)
        
        # Login link
        login_layout = QHBoxLayout()
        login_layout.setAlignment(Qt.AlignCenter)
        login_label = QLabel("Already have an account?")
        login_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        login_layout.addWidget(login_label)
        
        login_link = QPushButton("Login")
        login_link.setObjectName("secondary")
        login_link.setFlat(True)
        login_link.setStyleSheet(f"""
            QPushButton#secondary {{
                background-color: transparent;
                color: {COLORS['primary']};
                text-decoration: underline;
                padding: 5px;
            }}
            QPushButton#secondary:hover {{
                color: #dc2626;
            }}
        """)
        login_link.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        login_layout.addWidget(login_link)
        
        layout.addLayout(login_layout)
        
        widget.setLayout(layout)
        return widget
    
    def handle_login(self):
        """Handle login button click"""
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        result = self.api_client.login(username, password)
        
        if result['success']:
            token = result['data'].get('token')
            # Open main window
            from ui.main_window import MainWindow
            self.main_window = MainWindow(self.api_client, username)
            self.main_window.show()
            self.close()
        else:
            error_msg = result.get('error', 'Login failed')
            QMessageBox.critical(self, "Login Failed", f"Error: {error_msg}")
    
    def handle_signup(self):
        """Handle signup button click"""
        username = self.signup_username.text().strip()
        email = self.signup_email.text().strip()
        password = self.signup_password.text()
        
        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        
        result = self.api_client.signup(username, email, password)
        
        if result['success']:
            token = result['data'].get('token')
            # Open main window
            from ui.main_window import MainWindow
            self.main_window = MainWindow(self.api_client, username)
            self.main_window.show()
            self.close()
        else:
            error_msg = result.get('error', 'Signup failed')
            QMessageBox.critical(self, "Signup Failed", f"Error: {error_msg}")
