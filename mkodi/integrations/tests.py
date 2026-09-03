from django.test import TestCase
from django.urls import reverse

from taxpayers.models import Taxpayer


class Full360ViewTests(TestCase):
	def test_360_view_uses_admin_taxpayer_details(self):
		Taxpayer.objects.create(
			nida_number='NIDA-360',
			tin_number='TIN-360',
			phone_number='255700000360',
			full_name='360 Test Taxpayer',
			business_name='Test Traders',
			brela_number='BRELA-360',
			land_parcel='PLOT-360',
			tax_compliance_score=91,
			credit_score=87,
		)

		response = self.client.get(reverse('full_360_view', args=['TIN-360']))

		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertTrue(data['success'])
		self.assertEqual(data['taxpayer']['business_name'], 'Test Traders')
		self.assertEqual(data['taxpayer']['brela_number'], 'BRELA-360')
		self.assertEqual(data['land']['properties'][0]['parcel_number'], 'PLOT-360')
		self.assertEqual(data['taxpayer']['tax_compliance_score'], 91)
