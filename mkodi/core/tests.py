from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from taxpayers.models import Taxpayer


class MKodiAccountSyncTests(TestCase):
    def test_signup_uses_admin_taxpayer_record(self):
        Taxpayer.objects.create(
            nida_number='NIDA-001',
            tin_number='123456789',
            phone_number='255712345678',
            full_name='Admin Managed Taxpayer',
            brela_number='BRELA-001',
            tax_compliance_score=92,
            credit_score=88,
        )

        response = self.client.post(reverse('signup'), {
            'tin_number': '123456789',
            'password': 'secret1234',
            'password_confirm': 'secret1234',
        })

        self.assertRedirects(response, reverse('home'))
        user = User.objects.get(username='123456789')
        self.assertEqual(user.first_name, 'Admin Managed Taxpayer')
        self.assertEqual(user.email, '')
        taxpayer = Taxpayer.objects.get(tin_number='123456789')
        self.assertEqual(taxpayer.brela_number, 'BRELA-001')
        self.assertEqual(taxpayer.tax_compliance_score, 92)
        self.assertEqual(taxpayer.credit_score, 88)

    def test_signup_rejects_tin_missing_from_admin_records(self):
        response = self.client.post(reverse('signup'), {
            'tin_number': '999999999',
            'password': 'secret1234',
            'password_confirm': 'secret1234',
        })

        self.assertRedirects(response, reverse('signup'))
        self.assertFalse(User.objects.filter(username='999999999').exists())

    def test_password_can_be_changed(self):
        user = User.objects.create_user(username='change-me', password='oldpass123')
        self.client.force_login(user)
        response = self.client.post(reverse('change_password'), {
            'current_password': 'oldpass123',
            'new_password': 'newpass123',
            'confirm_password': 'newpass123',
        })
        self.assertRedirects(response, reverse('profile'))
        user.refresh_from_db()
        self.assertTrue(user.check_password('newpass123'))

    def test_profile_photo_accepts_image(self):
        user = User.objects.create_user(username='photo-user', password='oldpass123')
        self.client.force_login(user)
        photo = SimpleUploadedFile('avatar.png', b'not-a-real-image', content_type='image/png')
        response = self.client.post(reverse('profile'), {'photo': photo})
        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(user.profile.photo.name.endswith('.png'))
