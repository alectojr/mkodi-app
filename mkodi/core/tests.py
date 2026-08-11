from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class MKodiInnovationPlanTests(TestCase):
    def test_home_dashboard_shows_innovation_plan_summary(self):
        user = User.objects.create_user(
            username='123456789',
            password='secret1234',
            first_name='Micaih'
        )
        self.client.force_login(user)

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MKodi (Mobile-Kodi)')
        self.assertContains(response, 'Zero-rated access')
        self.assertContains(response, 'USSD + Zero-Rated Web Portal')
        self.assertContains(response, 'Onboard 1,000,000 informal traders within 24 months')
