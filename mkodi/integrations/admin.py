from django.contrib import admin
from .models import BrelaRecord, LandRecord

@admin.register(BrelaRecord)
class BrelaRecordAdmin(admin.ModelAdmin):
    list_display = ['brela_number', 'business_name', 'taxpayer', 'business_type', 'assets_value', 'registration_date']
    search_fields = ['brela_number', 'business_name', 'taxpayer__tin_number', 'taxpayer__full_name']
    list_filter = ['business_type', 'registration_date']
    fieldsets = (
        ('Taxpayer Information', {
            'fields': ('taxpayer',)
        }),
        ('Business Details', {
            'fields': ('brela_number', 'business_name', 'business_type', 'registration_date')
        }),
        ('Financial Information', {
            'fields': ('assets_value', 'number_of_assets')
        }),
        ('Compliance', {
            'fields': ('last_filed',)
        }),
    )

@admin.register(LandRecord)
class LandRecordAdmin(admin.ModelAdmin):
    list_display = ['parcel_number', 'taxpayer', 'location', 'size_acres', 'estimated_value', 'ownership_type']
    search_fields = ['parcel_number', 'location', 'taxpayer__tin_number', 'taxpayer__full_name']
    list_filter = ['ownership_type', 'registration_date']
    fieldsets = (
        ('Taxpayer Information', {
            'fields': ('taxpayer',)
        }),
        ('Property Details', {
            'fields': ('parcel_number', 'location', 'size_acres', 'ownership_type', 'registration_date')
        }),
        ('Valuation', {
            'fields': ('estimated_value',)
        }),
    )
    readonly_fields = ['registration_date']
