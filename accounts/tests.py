from django.test import TestCase
from .models import Account

class AccountTests(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create(name="Alice", balance=100)
        self.account2 = Account.objects.create(name="Bob", balance=50)

    def test_transfer_funds(self):
        self.account1.balance -= 30
        self.account2.balance += 30
        self.account1.save()
        self.account2.save()

        self.assertEqual(self.account1.balance, 70)
        self.assertEqual(self.account2.balance, 80)
