from rest_framework import serializers
from .models import UploadedDataset


class UploadedDatasetSerializer(serializers.ModelSerializer):
    """Serializer for UploadedDataset model"""
    summary = serializers.JSONField(source='summary_json', read_only=True)
    data = serializers.JSONField(source='data_json', read_only=True)
    entry_count = serializers.SerializerMethodField()
    
    class Meta:
        model = UploadedDataset
        fields = ['id', 'filename', 'file_path', 'upload_date', 'summary', 'data', 'entry_count']
        read_only_fields = ['id', 'upload_date', 'summary', 'data']
    
    def get_entry_count(self, obj):
        """Calculate the number of entries in the dataset"""
        if obj.data_json and isinstance(obj.data_json, list):
            return len(obj.data_json)
        return 0


class DatasetListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing datasets (without full data)"""
    summary = serializers.JSONField(source='summary_json', read_only=True)
    entry_count = serializers.SerializerMethodField()
    
    class Meta:
        model = UploadedDataset
        fields = ['id', 'filename', 'upload_date', 'summary', 'entry_count']
        read_only_fields = ['id', 'filename', 'upload_date', 'summary']
    
    def get_entry_count(self, obj):
        """Calculate the number of entries in the dataset"""
        if obj.data_json and isinstance(obj.data_json, list):
            return len(obj.data_json)
        return 0


class CSVUploadSerializer(serializers.Serializer):
    """Serializer for CSV file upload"""
    file = serializers.FileField(required=True)
    
    def validate_file(self, value):
        """Validate that the uploaded file is a CSV"""
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed")
        
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 10MB")
        
        return value
