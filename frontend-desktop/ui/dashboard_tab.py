"""
Dashboard Tab - Shows current dataset analytics and visualizations
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QScrollArea, QPushButton, QGridLayout, QMessageBox,
                             QFileDialog, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from config import COLORS
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DashboardTab(QWidget):
    """Dashboard tab showing dataset analytics"""
    
    def __init__(self, api_client, main_window):
        super().__init__()
        self.api_client = api_client
        self.main_window = main_window
        self.current_dataset = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Scroll area for content
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
        
        # Content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(20)
        
        # Empty state message
        self.empty_label = QLabel("No dataset loaded. Upload a CSV file to get started.")
        self.empty_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 16px;
            padding: 60px;
        """)
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(self.empty_label)
        
        self.content_widget.setLayout(self.content_layout)
        scroll.setWidget(self.content_widget)
        
        layout.addWidget(scroll)
        self.setLayout(layout)
    
    def display_dataset(self, dataset):
        """Display dataset information and visualizations"""
        self.current_dataset = dataset
        
        # Clear existing content
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Header with filename and actions
        header_layout = QHBoxLayout()
        
        filename_label = QLabel(f"📄 {dataset.get('filename', 'Unknown')}")
        filename_label.setFont(QFont("Inter", 18, QFont.Bold))
        filename_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        header_layout.addWidget(filename_label)
        
        header_layout.addStretch()
        
        download_btn = QPushButton("📥 Download PDF")
        download_btn.clicked.connect(self.download_pdf)
        header_layout.addWidget(download_btn)
        
        self.content_layout.addLayout(header_layout)
        
        # Summary section
        summary_group = self.create_summary_section(dataset)
        self.content_layout.addWidget(summary_group)
        
        # Charts section
        charts_group = self.create_charts_section(dataset)
        self.content_layout.addWidget(charts_group)
        
        # Parameter trends section
        trends_group = self.create_trends_section(dataset)
        self.content_layout.addWidget(trends_group)
        
        self.content_layout.addStretch()
    
    def create_summary_section(self, dataset):
        """Create summary statistics section"""
        group = QGroupBox("Summary Statistics")
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {COLORS['bg_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                color: {COLORS['text_primary']};
                padding: 20px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }}
        """)
        
        layout = QGridLayout()
        layout.setSpacing(15)
        
        summary = dataset.get('summary', {})
        
        stats = [
            ("Total Equipment", summary.get('total_equipment', 0)),
            ("Avg Flowrate", f"{summary.get('avg_flowrate', 0):.2f}"),
            ("Avg Pressure", f"{summary.get('avg_pressure', 0):.2f}"),
            ("Avg Temperature", f"{summary.get('avg_temperature', 0):.2f}"),
        ]
        
        row, col = 0, 0
        for label_text, value in stats:
            stat_widget = self.create_stat_card(label_text, str(value))
            layout.addWidget(stat_widget, row, col)
            col += 1
            if col >= 2:
                col = 0
                row += 1
        
        group.setLayout(layout)
        return group
    
    def create_stat_card(self, label, value):
        """Create a stat card widget"""
        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_tertiary']};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        layout.addWidget(label_widget)
        
        value_widget = QLabel(value)
        value_widget.setFont(QFont("Inter", 16, QFont.Bold))
        value_widget.setStyleSheet(f"color: {COLORS['primary']};")
        layout.addWidget(value_widget)
        
        widget.setLayout(layout)
        return widget
    
    def create_charts_section(self, dataset):
        """Create visualizations section with pie and bar charts side by side"""
        group = QGroupBox("Equipment Type Analysis")
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {COLORS['bg_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                color: {COLORS['text_primary']};
                padding: 20px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        summary = dataset.get('summary', {})
        
        # Debug output
        print(f"DEBUG - Summary keys: {summary.keys() if summary else 'None'}")
        print(f"DEBUG - Type distribution: {summary.get('type_distribution', {})}")
        
        # Pie chart - Equipment Type Distribution
        pie_canvas = self.create_pie_chart(summary.get('type_distribution', {}))
        layout.addWidget(pie_canvas)
        
        # Bar chart - Equipment Count by Type
        bar_canvas = self.create_bar_chart(summary.get('type_distribution', {}))
        layout.addWidget(bar_canvas)
        
        group.setLayout(layout)
        return group
    
    def create_trends_section(self, dataset):
        """Create parameter trends section"""
        group = QGroupBox("Parameter Trends")
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {COLORS['bg_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                color: {COLORS['text_primary']};
                padding: 20px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        data = dataset.get('data', [])
        
        # Debug output
        print(f"DEBUG - Data length: {len(data) if data else 0}")
        
        # Line chart - Parameter Trends
        line_canvas = self.create_line_chart(data)
        layout.addWidget(line_canvas)
        
        group.setLayout(layout)
        return group
    
    def create_pie_chart(self, type_distribution):
        """Create pie chart for equipment type distribution"""
        fig = Figure(figsize=(10, 6))
        fig.patch.set_facecolor(COLORS['bg_secondary'])
        ax = fig.add_subplot(111)
        ax.set_facecolor(COLORS['bg_secondary'])
        
        if type_distribution and len(type_distribution) > 0:
            types = list(type_distribution.keys())
            counts = list(type_distribution.values())
            
            # Colors matching web frontend
            colors = ['#ef4444', '#f97316', '#f59e0b', '#eab308', '#84cc16',
                     '#22c55e', '#10b981', '#14b8a6', '#06b6d4', '#0ea5e9',
                     '#3b82f6', '#6366f1', '#8b5cf6', '#a855f7', '#d946ef']
            colors_list = [colors[i % len(colors)] for i in range(len(types))]
            
            wedges, texts, autotexts = ax.pie(counts, labels=types, autopct='%1.1f%%',
                                               colors=colors_list, startangle=90,
                                               textprops={'color': COLORS['text_primary']})
            
            for text in texts:
                text.set_color(COLORS['text_primary'])
                text.set_fontsize(10)
                text.set_fontweight('bold')
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(9)
                autotext.set_fontweight('bold')
        else:
            # Show message when no data
            ax.text(0.5, 0.5, 'No equipment type data available', 
                   ha='center', va='center', 
                   color=COLORS['text_secondary'],
                   fontsize=12, transform=ax.transAxes)
            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
        
        ax.set_title('Equipment Type Distribution', color=COLORS['text_primary'],
                    fontsize=14, fontweight='bold', pad=15)
        ax.axis('equal')
        
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(400)
        canvas.setStyleSheet(f"background-color: {COLORS['bg_secondary']};")
        return canvas
    
    def create_bar_chart(self, type_distribution):
        """Create bar chart for equipment count by type"""
        fig = Figure(figsize=(10, 6))
        fig.patch.set_facecolor(COLORS['bg_secondary'])
        ax = fig.add_subplot(111)
        ax.set_facecolor(COLORS['bg_secondary'])
        
        if type_distribution and len(type_distribution) > 0:
            types = list(type_distribution.keys())
            counts = list(type_distribution.values())
            
            bars = ax.bar(types, counts, color=COLORS['primary'], edgecolor='white', linewidth=1.5)
            
            ax.set_xlabel('Equipment Type', color=COLORS['text_primary'], fontsize=11, fontweight='bold')
            ax.set_ylabel('Count', color=COLORS['text_primary'], fontsize=11, fontweight='bold')
            ax.tick_params(colors=COLORS['text_primary'])
            ax.grid(axis='y', alpha=0.3, linestyle='--', color=COLORS['border'])
            ax.set_axisbelow(True)
            
            if len(types) > 5:
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=9, fontweight='bold',
                       color=COLORS['text_primary'])
        else:
            # Show message when no data
            ax.text(0.5, 0.5, 'No equipment type data available', 
                   ha='center', va='center', 
                   color=COLORS['text_secondary'],
                   fontsize=12, transform=ax.transAxes)
            ax.set_xlabel('Equipment Type', color=COLORS['text_primary'], fontsize=11, fontweight='bold')
            ax.set_ylabel('Count', color=COLORS['text_primary'], fontsize=11, fontweight='bold')
            ax.tick_params(colors=COLORS['text_primary'])
        
        ax.set_title('Equipment Count by Type', color=COLORS['text_primary'],
                    fontsize=14, fontweight='bold', pad=15)
        
        fig.tight_layout()
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(400)
        canvas.setStyleSheet(f"background-color: {COLORS['bg_secondary']};")
        return canvas
    
    def create_line_chart(self, data):
        """Create line chart for parameter trends"""
        fig = Figure(figsize=(10, 6))
        fig.patch.set_facecolor(COLORS['bg_secondary'])
        ax = fig.add_subplot(111)
        ax.set_facecolor(COLORS['bg_secondary'])
        
        if data:
            limited_data = data[:20]
            indices = list(range(len(limited_data)))
            
            flowrates = [item.get('Flowrate', 0) for item in limited_data]
            pressures = [item.get('Pressure', 0) for item in limited_data]
            temperatures = [item.get('Temperature', 0) for item in limited_data]
            
            ax.plot(indices, flowrates, marker='o', linewidth=2, markersize=4,
                   label='Flowrate', color='#3b82f6')
            ax.plot(indices, pressures, marker='s', linewidth=2, markersize=4,
                   label='Pressure', color='#ef4444')
            ax.plot(indices, temperatures, marker='^', linewidth=2, markersize=4,
                   label='Temperature', color='#10b981')
            
            ax.set_xlabel('Equipment Index', color=COLORS['text_primary'], fontsize=11, fontweight='bold')
            ax.set_ylabel('Value', color=COLORS['text_primary'], fontsize=11, fontweight='bold')
            ax.tick_params(colors=COLORS['text_primary'])
            ax.legend(facecolor=COLORS['bg_tertiary'], edgecolor=COLORS['border'],
                     labelcolor=COLORS['text_primary'])
            ax.grid(alpha=0.3, linestyle='--', color=COLORS['border'])
            ax.set_axisbelow(True)
        
        ax.set_title('Parameter Trends (First 20 Items)', color=COLORS['text_primary'],
                    fontsize=14, fontweight='bold', pad=15)
        
        fig.tight_layout()
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(400)
        canvas.setStyleSheet(f"background-color: {COLORS['bg_secondary']};")
        return canvas
    
    def download_pdf(self):
        """Download PDF report"""
        if not self.current_dataset:
            QMessageBox.warning(
                self,
                "No Dataset",
                "Please load a dataset first."
            )
            return
        
        filename = self.current_dataset.get('filename', 'report')
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
                
                result = self.api_client.download_pdf(
                    self.current_dataset['id'],
                    save_path
                )
                
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
                        f"Error: {error_msg}"
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to download PDF: {str(e)}"
                )
