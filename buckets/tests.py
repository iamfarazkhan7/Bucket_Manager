# File: buckets/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Bucket


class BucketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pass123', is_staff=True)

    def test_bucket_creation(self):
        bucket = Bucket.objects.create(
            name='Test Bucket',
            description='Test description',
            owner=self.user
        )
        self.assertEqual(str(bucket), 'Test Bucket (testuser)')

    def test_unique_together_constraint(self):
        Bucket.objects.create(name='Test Bucket', owner=self.user)
        with self.assertRaises(Exception):
            Bucket.objects.create(name='Test Bucket', owner=self.user)


class BucketViewsTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user('staff', 'staff@example.com', 'pass123', is_staff=True)
        self.normal_user = User.objects.create_user('normal', 'normal@example.com', 'pass123', is_staff=False)
        self.bucket = Bucket.objects.create(name='Test Bucket', owner=self.staff_user)

    def test_staff_can_access_bucket_list(self):
        self.client.login(username='staff', password='pass123')
        response = self.client.get(reverse('buckets:list'))
        self.assertEqual(response.status_code, 200)

    def test_non_staff_cannot_access_bucket_list(self):
        self.client.login(username='normal', password='pass123')
        response = self.client.get(reverse('buckets:list'))
        self.assertEqual(response.status_code, 403)

    def test_anonymous_redirected_to_login(self):
        response = self.client.get(reverse('buckets:list'))
        self.assertRedirects(response, '/accounts/login/?next=/buckets/')

    def test_owner_can_only_see_own_buckets(self):
        another_user = User.objects.create_user('another', 'another@example.com', 'pass123', is_staff=True)
        Bucket.objects.create(name='Another Bucket', owner=another_user)
        
        self.client.login(username='staff', password='pass123')
        response = self.client.get(reverse('buckets:list'))
        
        self.assertContains(response, 'Test Bucket')
        self.assertNotContains(response, 'Another Bucket')

    def test_bucket_create_view(self):
        self.client.login(username='staff', password='pass123')
        response = self.client.post(reverse('buckets:create'), {
            'name': 'New Bucket',
            'description': 'New description'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Bucket.objects.filter(name='New Bucket', owner=self.staff_user).exists())