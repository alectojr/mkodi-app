from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from taxpayers.models import Taxpayer
from .models import Payment


class PaymentWorkflowTests(TestCase):
	def test_user_can_create_payment_request(self):
		taxpayer = Taxpayer.objects.create(
			nida_number='NIDA-PAY', tin_number='TIN-PAY',
			phone_number='255700000001', full_name='Payment User',
		)
		user = User.objects.create_user(username='TIN-PAY', password='password123')
		self.client.force_login(user)

		response = self.client.post(reverse('payments'), {
			'amount': '25000', 'payment_method': 'ussd',
		})

		self.assertRedirects(response, reverse('payments'))
		payment = Payment.objects.get(taxpayer=taxpayer)
		self.assertEqual(payment.amount, 25000)
		self.assertEqual(payment.payment_method, 'ussd')

	def test_user_can_view_own_receipt(self):
		taxpayer = Taxpayer.objects.create(
			nida_number='NIDA-REC', tin_number='TIN-REC',
			phone_number='255700000002', full_name='Receipt User',
		)
		user = User.objects.create_user(username='TIN-REC', password='password123')
		payment = Payment.objects.create(
			taxpayer=taxpayer, control_number='990000000001', amount=1000,
			payment_method='gepg', status='completed', transaction_id='TX-REC',
		)
		self.client.force_login(user)

		response = self.client.get(reverse('payment_receipt', args=[payment.id]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'TX-REC')
from django.test import TestCase

# Create your tests here.
