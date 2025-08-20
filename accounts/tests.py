# File: accounts/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsViewsTest(TestCase):
    def test_signup_view(self):
        """Test signup view creates user and logs them in"""
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        
        # First user should be staff
        user = User.objects.get(username='testuser')
        self.assertTrue(user.is_staff)

    def test_login_view(self):
        """Test login view"""
        User.objects.create_user('testuser', 'test@example.com', 'testpass123')
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_second_user_not_staff(self):
        """Test second user doesn't get staff privileges"""
        # Create first user
        User.objects.create_user('firstuser', 'first@example.com', 'pass123', is_staff=True)
        
        # Create second user via signup
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'seconduser',
            'email': 'second@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        
        user = User.objects.get(username='seconduser')
        self.assertFalse(user.is_staff)
