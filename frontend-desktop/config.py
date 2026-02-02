"""
Configuration settings for the desktop application
"""

# API Configuration
API_BASE_URL = "http://localhost:8000/api"

# API Endpoints
ENDPOINTS = {
    'login': f"{API_BASE_URL}/login/",
    'signup': f"{API_BASE_URL}/signup/",
    'upload': f"{API_BASE_URL}/upload/",
    'datasets': f"{API_BASE_URL}/datasets/",
    'dataset_detail': f"{API_BASE_URL}/datasets/{{id}}/",
    'dataset_delete': f"{API_BASE_URL}/datasets/{{id}}/delete/",
    'download_pdf': f"{API_BASE_URL}/datasets/{{id}}/report/",
}

# Application Settings
APP_TITLE = "ChemEquip Visualizer"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Color Theme (matching web frontend)
COLORS = {
    'primary': '#ef4444',
    'bg_primary': '#0a0a0a',
    'bg_secondary': '#141414',
    'bg_tertiary': '#1a1a1a',
    'bg_hover': '#1f1f1f',
    'text_primary': '#ffffff',
    'text_secondary': '#9ca3af',
    'border': '#2a2a2a',
    'success': '#10b981',
    'error': '#ef4444',
}

# Chart Colors
CHART_COLORS = [
    '#ef4444', '#f97316', '#f59e0b', '#eab308', '#84cc16',
    '#22c55e', '#10b981', '#14b8a6', '#06b6d4', '#0ea5e9',
    '#3b82f6', '#6366f1', '#8b5cf6', '#a855f7', '#d946ef'
]
