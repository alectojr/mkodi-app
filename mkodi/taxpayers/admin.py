from django.contrib import admin
from .models import Taxpayer

@admin.register(Taxpayer)
class TaxpayerAdmin(admin.ModelAdmin):
    list_display = ['nida_number', 'tin_number', 'full_name', 'phone_number', 'business_name', 'estimated_income', 'tax_compliance_score']
    search_fields = ['nida_number', 'tin_number', 'full_name']
    list_filter = ['is_active', 'date_registered', 'tax_compliance_score']
    fieldsets = (
        ('Personal Information', {
            'fields': ('nida_number', 'tin_number', 'full_name', 'phone_number', 'email')
        }),
        ('Business Information', {
            'fields': ('business_name', 'brela_number', 'land_parcel')
        }),
        ('Financial Data', {
            'fields': ('estimated_income',)
        }),
        ('Compliance Scores', {
            'fields': ('tax_compliance_score', 'credit_score')
        }),
        ('Status', {
            'fields': ('is_active', 'date_registered')
        }),
    )
    readonly_fields = ['date_registered']