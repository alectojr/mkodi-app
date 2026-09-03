from django.http import JsonResponse
from .models import Taxpayer

def taxpayer_lookup(request, nida_number):
    try:
        taxpayer = Taxpayer.objects.get(nida_number=nida_number)
        return JsonResponse({
            'nida_number': taxpayer.nida_number,
            'full_name': taxpayer.full_name,
            'phone_number': taxpayer.phone_number,
            'business_name': taxpayer.business_name,
            'estimated_income': str(taxpayer.estimated_income),
            'tax_score': taxpayer.tax_compliance_score,
        })
    except Taxpayer.DoesNotExist:
        return JsonResponse({'error': 'Taxpayer not found'}, status=404)


def register_taxpayer(request):
    return JsonResponse({'message': 'Registration endpoint ready'})


def account_lookup(request, tin_number):
    try:
        taxpayer = Taxpayer.objects.get(tin_number=tin_number, is_active=True)
    except Taxpayer.DoesNotExist:
        return JsonResponse({'error': 'No active taxpayer record found for this TIN.'}, status=404)

    return JsonResponse({
        'tin_number': taxpayer.tin_number,
        'full_name': taxpayer.full_name,
        'phone_number': taxpayer.phone_number,
        'email': taxpayer.email or '',
        'business_name': taxpayer.business_name or '',
        'brela_number': taxpayer.brela_number or '',
        'land_parcel': taxpayer.land_parcel or '',
        'estimated_income': str(taxpayer.estimated_income),
        'tax_compliance_score': taxpayer.tax_compliance_score,
        'credit_score': taxpayer.credit_score,
    })