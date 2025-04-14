from django.contrib import admin
from .models import MedicalFacility

@admin.register(MedicalFacility)
class MedicalFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility_type', 'location', 'is_approved', 'created_by', 'created_at')
    list_filter = ('facility_type', 'is_approved', 'location')
    search_fields = ('name', 'location', 'address', 'services')
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    list_editable = ('is_approved',)
    
    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
