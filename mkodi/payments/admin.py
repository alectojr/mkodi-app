from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = ['taxpayer', 'control_number', 'amount', 'payment_method', 'status', 'created_at', 'paid_at']
	search_fields = ['control_number', 'transaction_id', 'taxpayer__tin_number', 'taxpayer__full_name']
	list_filter = ['status', 'payment_method', 'created_at']
	readonly_fields = ['created_at', 'paid_at']
