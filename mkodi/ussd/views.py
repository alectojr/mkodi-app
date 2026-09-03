from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from taxpayers.models import Taxpayer
from payments.models import Payment
import random
import string
from .models import USSDSession

@csrf_exempt
def ussd_handler(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text', '')

        # Get or create session
        session, _ = USSDSession.objects.get_or_create(
            session_id=session_id,
            defaults={'phone_number': phone_number}
        )

        response_text = handle_ussd_menu(session, text)
        return JsonResponse({'response': response_text})

    return JsonResponse({'error': 'Only POST allowed'}, status=405)


def handle_ussd_menu(session, text):
    if text == "":
        return "CON Welcome to MKodi - Tax Made Easy\n1. Check My Tax\n2. Pay Tax\n3. Register Business\n4. Credit Score\n0. Exit"

    # Split input by *
    user_input = text.split('*')

    if user_input[0] == "1":   # Check Tax
        if len(user_input) == 1:
            return "CON Enter your NIDA Number:"
        else:
            nida = user_input[1]
            try:
                tp = Taxpayer.objects.get(nida_number=nida)
                return f"END Name: {tp.full_name}\nTax Due: TZS {tp.estimated_income}\nScore: {tp.tax_compliance_score}%"
            except Taxpayer.DoesNotExist:
                return "END NIDA not found. Register first."

    elif user_input[0] == "2":
        if len(user_input) == 1:
            return "CON Enter your NIDA Number:"
        if len(user_input) == 2:
            return "CON Enter payment amount:"
        try:
            taxpayer = Taxpayer.objects.get(nida_number=user_input[1], is_active=True)
            amount = float(user_input[2])
            if amount <= 0:
                raise ValueError
            control_number = "99" + ''.join(random.choices(string.digits, k=10))
            Payment.objects.create(
                taxpayer=taxpayer,
                control_number=control_number,
                amount=amount,
                payment_method='ussd',
            )
            return f"END Payment request created\nControl No: {control_number}\nAmount: TZS {amount:,.2f}"
        except (Taxpayer.DoesNotExist, ValueError):
            return "END Invalid NIDA or amount. Try again."

    elif user_input[0] == "0":
        return "END Thank you for using MKodi!"

    return "END Invalid option. Try again."