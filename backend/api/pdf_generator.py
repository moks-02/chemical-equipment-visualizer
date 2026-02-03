from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np


def generate_pdf_report(dataset):
    """
    Generate a PDF report for the given dataset.
    
    Args:
        dataset: UploadedDataset model instance
        
    Returns:
        io.BytesIO: PDF file buffer
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=12,
        alignment=TA_CENTER,
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#283593'),
        spaceAfter=10,
        spaceBefore=10,
    )
    
    # Title
    title = Paragraph("Chemical Equipment Analysis Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Dataset Information
    info_data = [
        ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['Dataset Filename:', dataset.filename],
        ['Upload Date:', dataset.upload_date.strftime('%Y-%m-%d %H:%M:%S')],
        ['Total Equipment:', str(dataset.summary_json.get('total_count', 0))],
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary Statistics Section
    summary_heading = Paragraph("Summary Statistics", heading_style)
    elements.append(summary_heading)
    
    summary = dataset.summary_json
    summary_data = [
        ['Metric', 'Average', 'Minimum', 'Maximum'],
        [
            'Flowrate',
            f"{summary.get('avg_flowrate', 0):.2f}",
            f"{summary.get('min_flowrate', 0):.2f}",
            f"{summary.get('max_flowrate', 0):.2f}"
        ],
        [
            'Pressure',
            f"{summary.get('avg_pressure', 0):.2f}",
            f"{summary.get('min_pressure', 0):.2f}",
            f"{summary.get('max_pressure', 0):.2f}"
        ],
        [
            'Temperature',
            f"{summary.get('avg_temperature', 0):.2f}",
            f"{summary.get('min_temperature', 0):.2f}",
            f"{summary.get('max_temperature', 0):.2f}"
        ],
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976d2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Equipment Type Distribution Section
    distribution_heading = Paragraph("Equipment Type Distribution", heading_style)
    elements.append(distribution_heading)
    
    type_distribution = summary.get('equipment_type_distribution', {})
    distribution_data = [['Equipment Type', 'Count', 'Percentage']]
    
    total_count = summary.get('total_count', 1)
    for equip_type, count in sorted(type_distribution.items()):
        percentage = (count / total_count) * 100
        distribution_data.append([
            equip_type,
            str(count),
            f"{percentage:.1f}%"
        ])
    
    dist_table = Table(distribution_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976d2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e3f2fd')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#e3f2fd'), colors.white]),
    ]))
    
    elements.append(dist_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Page break before charts
    elements.append(PageBreak())
    
    # Charts Section
    charts_heading = Paragraph("Data Visualizations", heading_style)
    elements.append(charts_heading)
    elements.append(Spacer(1, 0.2*inch))
    
    # Generate Pie Chart - Equipment Type Distribution
    pie_chart_img = generate_pie_chart_distribution(type_distribution)
    if pie_chart_img:
        elements.append(pie_chart_img)
        elements.append(Spacer(1, 0.3*inch))
    
    # Generate Bar Chart - Equipment Count by Type
    bar_chart_img = generate_type_count_bar_chart(type_distribution)
    if bar_chart_img:
        elements.append(bar_chart_img)
        elements.append(Spacer(1, 0.3*inch))
    
    # Generate Line Chart - Parameter Trends
    line_chart_img = generate_parameters_trend_chart(dataset.data_json)
    if line_chart_img:
        elements.append(line_chart_img)
        elements.append(Spacer(1, 0.3*inch))
    
    # Page break before equipment data
    elements.append(PageBreak())
    
    # Equipment Data Section (show first 20 rows)
    data_heading = Paragraph("Equipment Data (First 20 rows)", heading_style)
    elements.append(data_heading)
    
    data = dataset.data_json[:20]  # Limit to first 20 rows
    if data:
        equipment_data = [['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temp']]
        
        for row in data:
            equipment_data.append([
                row.get('Equipment Name', '')[:30],  # Truncate long names
                row.get('Type', '')[:20],
                f"{row.get('Flowrate', 0):.1f}",
                f"{row.get('Pressure', 0):.1f}",
                f"{row.get('Temperature', 0):.1f}"
            ])
        
        equipment_table = Table(equipment_data, colWidths=[2*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
        equipment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976d2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ]))
        
        elements.append(equipment_table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return buffer


def generate_pie_chart_distribution(type_distribution):
    """
    Generate a pie chart for equipment type distribution.
    
    Args:
        type_distribution: Dictionary of equipment types and counts
        
    Returns:
        Image: ReportLab Image object
    """
    if not type_distribution:
        return None
    
    try:
        # Create figure with square aspect ratio for cleaner pie chart
        fig, ax = plt.subplots(figsize=(6, 6))
        
        # Prepare data
        types = list(type_distribution.keys())
        counts = list(type_distribution.values())
        
        # Create color palette (matching Chart.js colors)
        colors_palette = ['#ef4444', '#f97316', '#f59e0b', '#eab308', '#84cc16', 
                         '#22c55e', '#10b981', '#14b8a6', '#06b6d4', '#0ea5e9',
                         '#3b82f6', '#6366f1', '#8b5cf6', '#a855f7', '#d946ef']
        colors_list = [colors_palette[i % len(colors_palette)] for i in range(len(types))]
        
        # Create pie chart with equal aspect ratio
        wedges, texts, autotexts = ax.pie(counts, labels=types, autopct='%1.1f%%',
                                           colors=colors_list, startangle=90,
                                           pctdistance=0.85, textprops={'fontsize': 10})
        
        # Customize text
        for text in texts:
            text.set_fontsize(11)
            text.set_fontweight('bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        
        # Ensure equal aspect ratio (perfect circle)
        ax.axis('equal')
        
        ax.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        # Save to buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close(fig)
        
        # Create ReportLab Image with square dimensions
        img = Image(img_buffer, width=5*inch, height=5*inch)
        return img
        
    except Exception as e:
        plt.close('all')
        return None


def generate_type_count_bar_chart(type_distribution):
    """
    Generate a bar chart for equipment count by type.
    
    Args:
        type_distribution: Dictionary of equipment types and counts
        
    Returns:
        Image: ReportLab Image object
    """
    if not type_distribution:
        return None
    
    try:
        # Create figure
        fig, ax = plt.subplots(figsize=(7, 4))
        
        # Prepare data
        types = list(type_distribution.keys())
        counts = list(type_distribution.values())
        
        # Create bar chart with red color theme
        bars = ax.bar(types, counts, color='#ef4444', edgecolor='white', linewidth=1.5)
        
        # Customize chart
        ax.set_xlabel('Equipment Type', fontsize=11, fontweight='bold')
        ax.set_ylabel('Count', fontsize=11, fontweight='bold')
        ax.set_title('Equipment Count by Type', fontsize=13, fontweight='bold', pad=15)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Rotate x-axis labels if needed
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save to buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close(fig)
        
        # Create ReportLab Image
        img = Image(img_buffer, width=6*inch, height=3.5*inch)
        return img
        
    except Exception as e:
        plt.close('all')
        return None


def generate_parameters_trend_chart(data):
    """
    Generate a line chart showing parameter trends over first 20 equipment items.
    
    Args:
        data: List of equipment data dictionaries
        
    Returns:
        Image: ReportLab Image object
    """
    try:
        # Create figure
        fig, ax = plt.subplots(figsize=(7, 4))
        
        # Prepare data (first 20 items)
        limited_data = data[:20] if len(data) > 20 else data
        indices = list(range(len(limited_data)))
        
        flowrates = [item.get('Flowrate', 0) for item in limited_data]
        pressures = [item.get('Pressure', 0) for item in limited_data]
        temperatures = [item.get('Temperature', 0) for item in limited_data]
        
        # Create line chart
        ax.plot(indices, flowrates, marker='o', linewidth=2, markersize=4, 
               label='Flowrate', color='#3b82f6')
        ax.plot(indices, pressures, marker='s', linewidth=2, markersize=4,
               label='Pressure', color='#ef4444')
        ax.plot(indices, temperatures, marker='^', linewidth=2, markersize=4,
               label='Temperature', color='#10b981')
        
        # Customize chart
        ax.set_xlabel('Equipment Index', fontsize=11, fontweight='bold')
        ax.set_ylabel('Value', fontsize=11, fontweight='bold')
        ax.set_title('Parameter Trends (First 20 Items)', fontsize=13, fontweight='bold', pad=15)
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        
        # Save to buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close(fig)
        
        # Create ReportLab Image
        img = Image(img_buffer, width=6*inch, height=3.5*inch)
        return img
        
    except Exception as e:
        plt.close('all')
        return None
