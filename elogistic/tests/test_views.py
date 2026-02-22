from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from elogistic.models import NetworkNode


class NetworkNodeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.active_user = User.objects.create_user(username='active', password='pass', is_active=True)
        self.inactive_user = User.objects.create_user(username='inactive', password='pass', is_active=False)
        self.node = NetworkNode.objects.create(
            type='factory',
            name='Test Factory',
            email='test@test.com',
            country='Russia',
            city='Moscow',
            street='Lenina',
            house_number='1',
            debt=1000  # 10.00 рублей
        )

    def test_active_user_can_list(self):
        self.client.force_authenticate(user=self.active_user)
        response = self.client.get('/api/nodes/')
        self.assertEqual(response.status_code, 200)

    def test_inactive_user_cannot_list(self):
        self.client.force_authenticate(user=self.inactive_user)
        response = self.client.get('/api/nodes/')
        self.assertEqual(response.status_code, 403)
        self.assertIn('не активна', response.data['detail'])

    def test_unauthenticated_user_cannot_list(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/nodes/')
        self.assertEqual(response.status_code, 403)
        self.assertIn('Authentication credentials were not provided.', response.data['detail'])

    def test_filter_by_country(self):
        self.client.force_authenticate(user=self.active_user)
        response = self.client.get('/api/nodes/?country=Russia')
        self.assertEqual(response.status_code, 200)
        # Проверим, что в ответе есть наш узел (можно проверить длину)
        self.assertGreaterEqual(len(response.data), 1)

    def test_delete_not_allowed(self):
        self.client.force_authenticate(user=self.active_user)
        response = self.client.delete(f'/api/nodes/{self.node.id}/')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed
