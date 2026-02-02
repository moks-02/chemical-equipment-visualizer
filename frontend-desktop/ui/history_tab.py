"""
History Tab - Shows list of uploaded datasets
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from config import COLORS
from datetime import datetime


class HistoryTab(QWidget):
    """History tab showing uploaded datasets"""
    
    def __init__(self, api_client, main_window):
        super().__init__()
        self.api_client = api_client
        self.main_window = main_window
        self.init_ui()
        self.load_history()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Upload History")
        title.setFont(QFont("Inter", 20, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("secondary")
        refresh_btn.clicked.connect(self.load_history)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Scroll area for dataset list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {COLORS['bg_primary']};
            }}
            QScrollBar:vertical {{
                background-color: {COLORS['bg_secondary']};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {COLORS['bg_hover']};
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {COLORS['border']};
            }}
        """)
        
        # Content widget for datasets
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(10)
        self.content_layout.setAlignment(Qt.AlignTop)
        
        self.content_widget.setLayout(self.content_layout)
        scroll.setWidget(self.content_widget)
        
        layout.addWidget(scroll)
        self.setLayout(layout)
    
    def load_history(self):
        """Load and display upload history"""
        # Clear existing content
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Fetch datasets
        result = self.api_client.get_datasets()
        
        if result['success']:
            datasets = result['data']
            
            if not datasets:
                empty_label = QLabel("No datasets uploaded yet.")
                empty_label.setStyleSheet(f"""
                    color: {COLORS['text_secondary']};
                    font-size: 16px;
                    padding: 40px;
                """)
                empty_label.setAlignment(Qt.AlignCenter)
                self.content_layout.addWidget(empty_label)
            else:
                for dataset in datasets:
                    dataset_widget = self.create_dataset_row(dataset)
                    self.content_layout.addWidget(dataset_widget)
        else:
            error_label = QLabel(f"Error loading history: {result.get('error', 'Unknown error')}")
            error_label.setStyleSheet(f"color: {COLORS['error']}; padding: 20px;")
            self.content_layout.addWidget(error_label)
    
    def create_dataset_row(self, dataset):
        """Create a horizontal row widget for a dataset"""
        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 15px;
            }}
            QWidget:hover {{
                background-color: {COLORS['bg_hover']};
                border-color: {COLORS['primary']};
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        # Icon
        icon_label = QLabel("📄")
        icon_label.setFont(QFont("Inter", 24))
        layout.addWidget(icon_label)
        
        # Info section
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        filename = QLabel(dataset.get('filename', 'Unknown'))
        filename.setFont(QFont("Inter", 16, QFont.Bold))
        filename.setStyleSheet(f"color: {COLORS['text_primary']};")
        info_layout.addWidget(filename)
        
        # Date and entry count
        meta_layout = QHBoxLayout()
        
        upload_date = dataset.get('upload_date', '')
        if upload_date:
            try:
                # Parse ISO format datetime with timezone
                dt = datetime.fromisoformat(upload_date.replace('Z', '+00:00'))
                # Convert to local timezone
                local_dt = dt.astimezone()
                date_str = local_dt.strftime('%b %d, %Y %I:%M %p')
            except:
                date_str = upload_date
        else:
            date_str = 'Unknown date'
        
        date_label = QLabel(f"📅 {date_str}")
        date_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 15px;")
        meta_layout.addWidget(date_label)
        
        entry_count = dataset.get('entry_count', 0)
        count_badge = QLabel(f"{entry_count} entries")
        count_badge.setStyleSheet(f"""
            color: {COLORS['primary']};
            background-color: {COLORS['bg_tertiary']};
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: bold;
        """)
        meta_layout.addWidget(count_badge)
        
        meta_layout.addStretch()
        info_layout.addLayout(meta_layout)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Action buttons
        view_btn = QPushButton("👁 View")
        view_btn.setFixedWidth(100)
        view_btn.clicked.connect(lambda: self.view_dataset(dataset['id']))
        layout.addWidget(view_btn)
        
        download_btn = QPushButton("📥 PDF")
        download_btn.setObjectName("secondary")
        download_btn.setFixedWidth(100)
        download_btn.clicked.connect(lambda: self.download_pdf(dataset))
        layout.addWidget(download_btn)
        
        delete_btn = QPushButton("🗑 Delete")
        delete_btn.setObjectName("secondary")
        delete_btn.setFixedWidth(100)
        delete_btn.setStyleSheet(f"""
            QPushButton#secondary {{
                background-color: {COLORS['bg_tertiary']};
                color: {COLORS['error']};
                border: 1px solid {COLORS['error']};
            }}
            QPushButton#secondary:hover {{
                background-color: {COLORS['error']};
                color: white;
            }}
        """)
        delete_btn.clicked.connect(lambda: self.delete_dataset(dataset['id']))
        layout.addWidget(delete_btn)
        
        widget.setLayout(layout)
        return widget
    
    def view_dataset(self, dataset_id):
        """View dataset in dashboard"""
        self.main_window.load_dataset(dataset_id)
    
    def download_pdf(self, dataset):
        """Download PDF report for dataset"""
        from PyQt5.QtWidgets import QFileDialog
        
        filename = dataset.get('filename', 'report')
        if filename.endswith('.csv'):
            filename = filename[:-4]
        
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            f"{filename}_report.pdf",
            "PDF Files (*.pdf)"
        )
        
        if save_path:
            try:
                if not save_path.endswith('.pdf'):
                    save_path += '.pdf'
                
                result = self.api_client.download_pdf(dataset['id'], save_path)
                
                if result['success']:
                    QMessageBox.information(
                        self,
                        "Success",
                        f"PDF report saved to:\n{save_path}"
                    )
                else:
                    error_msg = result.get('error', 'Download failed')
                    QMessageBox.critical(
                        self,
                        "Download Failed",
                        f"Error: {error_msg}\n\nPlease ensure the backend is running."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to download PDF: {str(e)}"
                )
    
    def delete_dataset(self, dataset_id):
        """Delete a dataset"""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this dataset?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            result = self.api_client.delete_dataset(dataset_id)
            
            if result['success']:
                QMessageBox.information(self, "Success", "Dataset deleted successfully")
                self.load_history()
                
                # Clear dashboard if this was the current dataset
                if (self.main_window.current_dataset and 
                    self.main_window.current_dataset.get('id') == dataset_id):
                    self.main_window.current_dataset = None
                    self.main_window.dashboard_tab.display_dataset(None)
            else:
                error_msg = result.get('error', 'Delete failed')
                QMessageBox.critical(
                    self,
                    "Delete Failed",
                    f"Error: {error_msg}"
                )
