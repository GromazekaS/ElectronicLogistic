from django.test import TestCase
from elogistic.models import NetworkNode

class NetworkNodeModelTest(TestCase):
    def test_str_method(self):
        node = NetworkNode.objects.create(
            type='factory', name='Test', email='test@test.com',
            country='Russia', city='Moscow', street='Lenina', house_number='1'
        )
        self.assertEqual(str(node), 'Test')

    def test_hierarchy_role_factory(self):
        node = NetworkNode.objects.create(
            type='factory', name='Factory', email='factory@test.com',
            country='Russia', city='Moscow', street='Lenina', house_number='1'
        )
        self.assertEqual(node.hierarchy_role, 'factory')

    def test_hierarchy_role_retail(self):
        supplier = NetworkNode.objects.create(
            type='factory', name='Supplier', email='sup@test.com',
            country='Russia', city='Moscow', street='Lenina', house_number='1'
        )
        node = NetworkNode.objects.create(
            type='retail', name='Retail', email='retail@test.com',
            country='Russia', city='SPb', street='Nevsky', house_number='10',
            supplier=supplier
        )
        self.assertEqual(node.hierarchy_role, 'retail')

    def test_hierarchy_role_distributor(self):
        supplier = NetworkNode.objects.create(
            type='factory', name='Supplier', email='sup@test.com',
            country='Russia', city='Moscow', street='Lenina', house_number='1'
        )
        node = NetworkNode.objects.create(
            type='individual', name='Distributor', email='dist@test.com',
            country='Russia', city='SPb', street='Nevsky', house_number='10',
            supplier=supplier
        )
        customer = NetworkNode.objects.create(
            type='retail', name='Customer', email='cust@test.com',
            country='Russia', city='Kazan', street='Baumana', house_number='5',
            supplier=node
        )
        self.assertEqual(node.hierarchy_role, 'distributor')
        