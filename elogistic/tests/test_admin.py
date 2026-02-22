from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from elogistic.admin import NetworkNodeAdmin, NetworkNodeForm
from elogistic.models import NetworkNode


class NetworkNodeAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = NetworkNodeAdmin(NetworkNode, self.site)
        self.user = User.objects.create_superuser(username='admin', password='pass', is_active=True)
        self.client.force_login(self.user)
        self.node = NetworkNode.objects.create(
            type='factory', name='Test', email='test@test.com',
            country='Russia', city='Moscow', street='Lenina', house_number='1', debt=1000
        )

    def test_supplier_link_with_supplier(self):
        node2 = NetworkNode.objects.create(
            type='retail', name='Child', email='child@test.com',
            country='Russia', city='SPb', street='Nevsky', house_number='10',
            supplier=self.node, debt=0
        )
        link = self.admin.supplier_link(node2)
        self.assertIn(str(self.node.id), link)
        self.assertIn(self.node.name, link)

    def test_supplier_link_without_supplier(self):
        link = self.admin.supplier_link(self.node)
        self.assertEqual(link, "-")

    def test_debt_display_list(self):
        display = self.admin.debt_display_list(self.node)
        self.assertEqual(display, "10.00 ₽")

    def test_clear_debt_action(self):
        # Выбираем объекты для action (например, self.node)
        data = {
            'action': 'clear_debt',
            '_selected_action': [self.node.id],
        }
        # Отправляем POST на страницу списка объектов
        response = self.client.post('/admin/elogistic/networknode/', data)
        self.assertEqual(response.status_code, 302)  # редирект после action
        self.node.refresh_from_db()
        self.assertEqual(self.node.debt, 0)

    def test_admin_list_page(self):
        response = self.client.get('/admin/elogistic/networknode/')
        self.assertEqual(response.status_code, 200)

    def test_admin_add_page(self):
        response = self.client.get('/admin/elogistic/networknode/add/')
        self.assertEqual(response.status_code, 200)


class NetworkNodeFormTest(TestCase):
    def test_form_init_new_object(self):
        form = NetworkNodeForm()
        self.assertEqual(form.fields['debt_display'].initial, '0.00 ₽')
        self.assertEqual(form.fields['debt_rub'].initial, 0)

    def test_form_init_existing_object(self):
        node = NetworkNode.objects.create(
            type='factory', name='Test', email='test@test.com',
            country='Russia', city='Moscow', street='Lenina', house_number='1',
            debt=123456  # 1234.56 рублей
        )
        form = NetworkNodeForm(instance=node)
        self.assertEqual(form.fields['debt_display'].initial, '1 234.56 ₽')
        self.assertEqual(form.fields['debt_rub'].initial, 1234.56)
