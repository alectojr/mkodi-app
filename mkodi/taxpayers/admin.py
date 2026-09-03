from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
import csv
from django.http import HttpResponse
from .models import Taxpayer

@admin.register(Taxpayer)
class TaxpayerAdmin(admin.ModelAdmin):
    list_display = ['nida_number', 'tin_number', 'full_name', 'phone_number', 'business_name', 'estimated_income', 'tax_compliance_score', 'delete_link']
    search_fields = ['nida_number', 'tin_number', 'full_name']
    list_filter = ['is_active', 'date_registered', 'tax_compliance_score']
    actions = ['delete_selected', 'export_taxpayers']
    actions_on_top = True
    actions_on_bottom = True
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

    @admin.display(description='Delete')
    def delete_link(self, obj):
        url = reverse('admin:taxpayers_taxpayer_delete', args=[obj.pk])
        return format_html('<a class="deletelink" href="{}">Delete</a>', url)

    @admin.action(description='Export selected taxpayers as CSV')
    def export_taxpayers(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="taxpayers.csv"'
        writer = csv.writer(response)
        writer.writerow(['TIN', 'NIDA', 'Full name', 'Phone', 'Business', 'BRELA number', 'Income', 'Compliance', 'Credit score', 'Active'])
        for taxpayer in queryset:
            writer.writerow([
                taxpayer.tin_number, taxpayer.nida_number, taxpayer.full_name,
                taxpayer.phone_number, taxpayer.business_name, taxpayer.brela_number,
                taxpayer.estimated_income, taxpayer.tax_compliance_score,
                taxpayer.credit_score, taxpayer.is_active,
            ])
        return response