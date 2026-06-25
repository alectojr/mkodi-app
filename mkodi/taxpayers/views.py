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