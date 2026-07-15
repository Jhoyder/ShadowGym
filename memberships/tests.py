from django.test import TestCase
from django.db import IntegrityError

from .models import Plan

# Create your tests here.


class PlanModelTests(TestCase):
	def test_str_uses_custom_duration_label(self):
		plan = Plan.objects.create(name='Gold', price=150.00, duration_value=1, duration_unit=Plan.YEARS)
		self.assertIn('1 año', str(plan))

	def test_to_days_converts_months(self):
		plan = Plan.objects.create(name='Trimestral', price=90.00, duration_value=3, duration_unit=Plan.MONTHS)
		self.assertEqual(plan.duration_days, 90)

	def test_name_must_be_unique(self):
		Plan.objects.create(name='Mensual', price=30.00, duration_value=30, duration_unit=Plan.DAYS)

		with self.assertRaises(IntegrityError):
			Plan.objects.create(name='Mensual', price=35.00, duration_value=1, duration_unit=Plan.MONTHS)
