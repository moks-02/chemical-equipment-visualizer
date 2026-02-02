from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
import os
import json


class UploadedDataset(models.Model):
    """
    Model to store uploaded CSV datasets and their analysis summaries.
    Automatically maintains only the last 5 datasets per user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    filename = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='datasets/')
    upload_date = models.DateTimeField(auto_now_add=True)
    summary_json = models.JSONField(default=dict, blank=True)
    
    # Store parsed data as JSON for quick retrieval
    data_json = models.JSONField(default=list, blank=True)
    
    class Meta:
        ordering = ['-upload_date']
        verbose_name = 'Uploaded Dataset'
        verbose_name_plural = 'Uploaded Datasets'
    
    def __str__(self):
        return f"{self.filename} - {self.upload_date.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        """Override save to maintain only last 5 datasets per user"""
        super().save(*args, **kwargs)
        
        # Get all datasets for this user ordered by upload date (newest first)
        user_datasets = UploadedDataset.objects.filter(user=self.user)
        
        # If more than 5, delete the oldest ones
        if user_datasets.count() > 5:
            datasets_to_delete = user_datasets[5:]
            for dataset in datasets_to_delete:
                # Delete the file from filesystem
                if dataset.file_path:
                    try:
                        if os.path.isfile(dataset.file_path.path):
                            os.remove(dataset.file_path.path)
                    except Exception as e:
                        print(f"Error deleting file: {e}")
                # Delete the database record
                dataset.delete()
    
    def get_summary(self):
        """Return the summary as a dictionary"""
        return self.summary_json
    
    def get_data(self):
        """Return the parsed data as a list"""
        return self.data_json
