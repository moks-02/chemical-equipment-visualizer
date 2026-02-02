from django.contrib import admin
from .models import UploadedDataset


@admin.register(UploadedDataset)
class UploadedDatasetAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'upload_date', 'get_total_count')
    list_filter = ('upload_date',)
    search_fields = ('filename',)
    readonly_fields = ('upload_date', 'summary_json', 'data_json')
    
    def get_total_count(self, obj):
        return obj.summary_json.get('total_count', 0)
    get_total_count.short_description = 'Total Equipment'
    
    fieldsets = (
        ('File Information', {
            'fields': ('filename', 'file_path', 'upload_date')
        }),
        ('Analysis Data', {
            'fields': ('summary_json', 'data_json'),
            'classes': ('collapse',)
        }),
    )
