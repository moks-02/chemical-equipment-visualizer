from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    
    # Dataset operations
    path('upload/', views.upload_csv, name='upload-csv'),
    path('datasets/', views.list_datasets, name='list-datasets'),
    path('datasets/<int:pk>/', views.get_dataset_detail, name='dataset-detail'),
    path('datasets/<int:pk>/report/', views.generate_report, name='generate-report'),
    path('datasets/<int:pk>/preview/', views.preview_report, name='preview-report'),
    path('datasets/<int:pk>/delete/', views.delete_dataset, name='delete-dataset'),
]
