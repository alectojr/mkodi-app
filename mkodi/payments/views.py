import json
import random
import string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from taxpayers.models import Taxpayer
from .models import Payment

@csrf_exempt
def generate_control_number(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

        nida = data.get('nida_number')
        amount = data.get('amount')

        try:
            taxpayer = Taxpayer.objects.get(nida_number=nida)
            control_number = "99" + ''.join(random.choices(string.digits, k=10))
            Payment.objects.create(
                taxpayer=taxpayer,
                control_number=control_number,
                amount=amount or 0,
                payment_method=data.get('payment_method', 'GePG'),
            )

            return JsonResponse({
                "success": True,
                "control_number": control_number,
                "amount": amount,
                "taxpayer_name": taxpayer.full_name,
                "message": "Control Number Generated Successfully!",
                "next_step": "initiate_stk_push"
            })
        except Taxpayer.DoesNotExist:
            return JsonResponse({"success": False, "error": "NIDA not found"}, status=404)
    
    return JsonResponse({"error": "POST method required"}, status=405)


@csrf_exempt
def initiate_stk_push(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

        # Reads values from the JSON body instead of request.POST
        control_number = data.get('control_number')
        phone_number = data.get('phone_number')

        if not control_number or not phone_number:
            return JsonResponse({"success": False, "error": "Missing required fields"}, status=400)

        transaction_id = "TX" + ''.join(random.choices(string.digits, k=12))
        payment = Payment.objects.filter(control_number=control_number).first()
        if payment:
            payment.transaction_id = transaction_id
            payment.status = 'completed'
            payment.paid_at = timezone.now()
            payment.save(update_fields=['transaction_id', 'status', 'paid_at'])

        return JsonResponse({
            "success": True,
            "message": "STK Push initiated! Enter PIN on your phone.",
            "control_number": control_number,
            "transaction_id": transaction_id,
            "status": "pending"
        })
    
    return JsonResponse({"error": "POST method required"}, status=405)
