from django.test import TestCase

from taxpayers.models import Taxpayer
from .models import USSDSession
from .views import handle_ussd_menu


class USSDWorkflowTests(TestCase):
	def test_payment_menu_creates_payment_request(self):
		taxpayer = Taxpayer.objects.create(
			nida_number='NIDA-USSD', tin_number='TIN-USSD',
			phone_number='255700000003', full_name='USSD User',
		)
		session = USSDSession.objects.create(session_id='session-1', phone_number='255700000003')

		self.assertIn('Enter your NIDA', handle_ussd_menu(session, '2'))
		self.assertIn('Enter payment amount', handle_ussd_menu(session, '2*NIDA-USSD'))
		response = handle_ussd_menu(session, '2*NIDA-USSD*5000')

		self.assertIn('Control No:', response)
		self.assertTrue(taxpayer.payment_set.filter(amount=5000, payment_method='ussd').exists())
from django.test import TestCase

# Create your tests here.
