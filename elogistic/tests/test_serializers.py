from django.test import SimpleTestCase
from rest_framework.exceptions import ValidationError
from elogistic.serializers import RublesField

class RublesFieldTest(SimpleTestCase):
    def setUp(self):
        self.field = RublesField()

    def test_to_representation(self):
        self.assertEqual(self.field.to_representation(10050), '100.50')

    def test_to_internal_value_valid(self):
        self.assertEqual(self.field.to_internal_value("100.50"), 10050)
        self.assertEqual(self.field.to_internal_value("100"), 10000)
        self.assertEqual(self.field.to_internal_value("0.01"), 1)

    def test_invalid_format(self):
        with self.assertRaises(ValidationError):
            self.field.to_internal_value("100.123")
        with self.assertRaises(ValidationError):
            self.field.to_internal_value("abc")
        with self.assertRaises(ValidationError):
            self.field.to_internal_value("")
        with self.assertRaises(ValidationError):
            self.field.to_internal_value(None)

    def test_negative_value(self):
        with self.assertRaises(ValidationError):
            self.field.to_internal_value("-50.00")
