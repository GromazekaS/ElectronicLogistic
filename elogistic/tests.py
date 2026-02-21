from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import NetworkNode, Product
from rest_framework.exceptions import ValidationError
from .serializers import RublesField

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


class RublesFieldTest(SimpleTestCase):
    def setUp(self):
        self.field = RublesField()

    def test_to_representation(self):
        # Копейки → рубли (строка с двумя знаками)
        self.assertEqual(self.field.to_representation(10050), "100.50")
        self.assertEqual(self.field.to_representation(0), "0.00")
        self.assertEqual(self.field.to_representation(1), "0.01")
        self.assertEqual(self.field.to_representation(123456789), "1234567.89")

    def test_to_internal_value_valid(self):
        # Валидные входные строки
        self.assertEqual(self.field.to_internal_value("100.50"), 10050)
        self.assertEqual(self.field.to_internal_value("0.00"), 0)
        self.assertEqual(self.field.to_internal_value("0.01"), 1)
        self.assertEqual(self.field.to_internal_value("1234567.89"), 123456789)
        self.assertEqual(self.field.to_internal_value("100"), 10000)  # целое
        self.assertEqual(self.field.to_internal_value("100.5"), 10050)  # один знак

    def test_to_internal_value_invalid_format(self):
        # Неверные форматы
        with self.assertRaises(ValidationError):
            self.field.to_internal_value("100.123")  # три знака после запятой
        with self.assertRaises(ValidationError):
            self.field.to_internal_value("abc")
        with self.assertRaises(ValidationError):
            self.field.to_internal_value("100,50")  # запятая вместо точки
        with self.assertRaises(ValidationError):
            self.field.to_internal_value("")
        with self.assertRaises(ValidationError):
            self.field.to_internal_value(None)

    def test_negative_value(self):
        # Отрицательные суммы
        with self.assertRaises(ValidationError) as cm:
            self.field.to_internal_value("-100.50")
        self.assertIn('отрицательной', str(cm.exception).lower())

class DebtAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.active_user = User.objects.create_user(username='active', password='pass', is_active=True)
        self.client.force_authenticate(user=self.active_user)
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

    def test_create_with_debt(self):
        data = {
            'type': 'retail',
            'name': 'New Shop',
            'email': 'shop@test.com',
            'country': 'Russia',
            'city': 'SPb',
            'street': 'Nevsky',
            'house_number': '10',
            'debt': '100.50',
            'currency': 'RUB',
            'products': []
        }
        response = self.client.post('/api/nodes/', data, format='json')
        self.assertEqual(response.status_code, 201)
        node = NetworkNode.objects.get(name='New Shop')
        self.assertEqual(node.debt, 10050)

    def test_create_without_debt(self):
        data = {
            'type': 'retail',
            'name': 'Another Shop',
            'email': 'shop2@test.com',
            'country': 'Russia',
            'city': 'SPb',
            'street': 'Nevsky',
            'house_number': '12',
            'currency': 'RUB',
            'products': []
        }
        response = self.client.post('/api/nodes/', data, format='json')
        self.assertEqual(response.status_code, 201)
        node = NetworkNode.objects.get(name='Another Shop')
        self.assertEqual(node.debt, 0)

    def test_create_with_invalid_debt(self):
        data = {
            'type': 'retail',
            'name': 'Bad Shop',
            'email': 'bad@test.com',
            'country': 'Russia',
            'city': 'SPb',
            'street': 'Nevsky',
            'house_number': '10',
            'debt': '100.123',  # три знака
            'currency': 'RUB',
            'products': []
        }
        response = self.client.post('/api/nodes/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('debt', response.data)

    def test_create_with_negative_debt(self):
        data = {
            'type': 'retail',
            'name': 'Negative Shop',
            'email': 'neg@test.com',
            'country': 'Russia',
            'city': 'SPb',
            'street': 'Nevsky',
            'house_number': '10',
            'debt': '-50.00',
            'currency': 'RUB',
            'products': []
        }
        response = self.client.post('/api/nodes/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('debt', response.data)

    def test_create_with_non_numeric_debt(self):
        data = {
            'type': 'retail',
            'name': 'Alpha Shop',
            'email': 'alpha@test.com',
            'country': 'Russia',
            'city': 'SPb',
            'street': 'Nevsky',
            'house_number': '10',
            'debt': 'abc',
            'currency': 'RUB',
            'products': []
        }
        response = self.client.post('/api/nodes/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('debt', response.data)

    def test_update_debt_ignored(self):
        # Пытаемся обновить debt, но он не должен измениться
        response = self.client.patch(f'/api/nodes/{self.node.id}/', {'debt': '200.00'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.node.refresh_from_db()
        self.assertEqual(self.node.debt, 1000)  # осталось прежним

    def test_update_with_invalid_debt_returns_error(self):
        # Даже некорректный debt при обновлении вызывает ошибку
        response = self.client.patch(f'/api/nodes/{self.node.id}/', {'debt': 'abc'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.node.refresh_from_db()
        self.assertEqual(self.node.debt, 1000)  # значение не изменилось
