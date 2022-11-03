from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from .models import Account, Card

# Importing other elements
from decimal import Decimal
import datetime


# Account Testing
class AccountTests(TestCase):

    def setUp(self):
        # Set up testing Account
        self.user = User(username="test", password="t3st1N6!", first_name="Test", last_name="Case", is_staff=False, is_active=True, is_superuser=False)
        self.user.save()
        self.account = Account(user=self.user, number="01101001", name="Testing", phone_number="123-456-7890", balance=100.00)
        self.account.save()

    def testAccount(self):
        # Verify that Account was successfully created
        self.assertEqual(Account.objects.all().count(), 1)
        data = Account.objects.get(number = "01101001")
        self.assertEqual(data.user, self.user)
        self.assertEqual(data.name, "Testing")
        self.assertEqual(data.phone_number, "123-456-7890")
        self.assertAlmostEqual(data.balance, Decimal(100.00))

    def testAccount_badNumber(self):
        # Verify that bad numbers aren't allowed
        self.account.number = "testing"
        self.assertRaises(Exception, self.account.save())
        self.account.number = 1
        self.assertRaises(Exception, self.account.save())
        self.account.number = -1
        self.assertRaises(Exception, self.account.save())
        self.account.number = "1234567"
        self.assertRaises(Exception, self.account.save())
        self.account.number = "123456789"
        self.assertRaises(Exception, self.account.save())
        self.account.number = "1234five"
        self.assertRaises(Exception, self.account.save())

    def testAccount_badPhone(self):
        # Verify that phone number has to be right format
        self.account.phone_number = "1234567890"
        self.assertRaises(Exception, self.account.save())
        self.account.phone_number = "testing"
        self.assertRaises(Exception, self.account.save())
        self.account.phone_number = 1234567890
        self.assertRaises(Exception, self.account.save())
        self.account.phone_number = -1234567890
        self.assertRaises(Exception, self.account.save())
        self.account.phone_number = "9999999999999"
        self.assertRaises(Exception, self.account.save())
        self.account.phone_number = "1"
        self.assertRaises(Exception, self.account.save())

    def testAccount_badBalance(self):
        # Verify that certain balances aren't allowed
        self.account.balance = 9999999999999
        self.assertRaises(Exception, self.account.save())
        self.account.balance = "100.00"
        self.assertRaises(Exception, self.account.save())
        self.account.balance = -9999999999999
        self.assertRaises(Exception, self.account.save())


# Card Testing
class CardTests(TestCase):

    def setUp(self):
        # Set up testing Card
        self.user = User(username="test", password="t3st1N6!", first_name="Test", last_name="Case", is_staff=False, is_active=True, is_superuser=False)
        self.user.save()
        self.account = Account(user=self.user, number="01101001", name="Testing", phone_number="123-456-7890", balance=100.00)
        self.account.save()
        self.card = Card(account=self.account, holder="Tester", number="1234-1234-1234-1234", pin="1234", status=True, date_issued=datetime.date(2021, 11, 4), expiry_date=datetime.date(2026, 11, 10))
        self.card.save()

    def testCard(self):
        # Verify that Card was successfully created
        self.assertEqual(Card.objects.all().count(), 1)
        data = Card.objects.get(number = "1234-1234-1234-1234")
        self.assertEqual(data.account, self.account)
        self.assertEqual(data.holder, "Tester")
        self.assertEqual(data.pin, "1234")
        self.assertEqual(data.status, True)
        self.assertLess(data.date_issued, datetime.datetime.now().date())
        self.assertGreater(data.expiry_date, datetime.datetime.now().date())

    def testCard_badNumber(self):
        # Verify that bad numbers aren't allowed
        self.card.number = "testing"
        self.assertRaises(Exception, self.card.save())
        self.card.number = 1
        self.assertRaises(Exception, self.card.save())
        self.card.number = -1
        self.assertRaises(Exception, self.card.save())
        self.card.number = "1234-1234-1234-123"
        self.assertRaises(Exception, self.card.save())
        self.card.number = "1234-1234-1234-12345"
        self.assertRaises(Exception, self.card.save())
        self.card.number = "1234-1234-1234-five"
        self.assertRaises(Exception, self.card.save())

    def testCard_badPIN(self):
        # Verify that bad PIN's aren't allowed
        self.card.pin = "test"
        self.assertRaises(Exception, self.card.save())
        self.card.pin = 1234
        self.assertRaises(Exception, self.card.save())
        self.card.pin = -1234
        self.assertRaises(Exception, self.card.save())
        self.card.pin = "123"
        self.assertRaises(Exception, self.card.save())
        self.card.pin = "12345"
        self.assertRaises(Exception, self.card.save())
        self.card.pin = "123a"
        self.assertRaises(Exception, self.card.save())