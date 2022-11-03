from django.test import TestCase

# Create your tests here.
from .models import Machine

# Importing other elements
from decimal import Decimal
import datetime


# Machine Testing
class MachineTests(TestCase):

    def setUp(self):
        # Set up testing Machine
        self.machine = Machine(address="123 Testing Way", status=True, minimum=50.00, balance=100.00, maintenance=datetime.date(2021, 12, 14), last_refill=datetime.date(2021, 11, 4), next_refill=datetime.date(2021, 12, 14))
        self.machine.save()

    def testMachine(self):
        # Verify that Machine was successfully created
        self.assertEqual(Machine.objects.all().count(), 1)
        data = Machine.objects.get(pk = 1)
        self.assertEqual(data.address, "123 Testing Way")
        self.assertEqual(data.status, True)
        self.assertAlmostEqual(data.minimum, Decimal(50.00))
        self.assertAlmostEqual(data.balance, Decimal(100.00))
        self.assertGreater(data.maintenance, datetime.datetime.now().date())
        self.assertLess(data.last_refill, datetime.datetime.now().date())
        self.assertGreater(data.next_refill, datetime.datetime.now().date())

    def testMachine_badAddress(self):
        # Verify that bad addresses aren't allowed
        self.machine.address = 123
        self.assertRaises(Exception, self.machine.save())
        self.machine.address = "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
        self.assertRaises(Exception, self.machine.save())
        self.machine.address = ""
        self.assertRaises(Exception, self.machine.save())

    def testMachine_badMinimum(self):
        # Verify that bad minimums aren't allowed
        self.machine.minimum = 9999999999999
        self.assertRaises(Exception, self.machine.save())
        self.machine.minimum = "100.00"
        self.assertRaises(Exception, self.machine.save())
        self.machine.minimum = 0
        self.assertRaises(Exception, self.machine.save())
        self.machine.minimum = -9999999999999
        self.assertRaises(Exception, self.machine.save())

    def testMachine_badBalance(self):
        # Verify that certain balances aren't allowed
        self.machine.balance = 9999999999999
        self.assertRaises(Exception, self.machine.save())
        self.machine.balance = "100.00"
        self.assertRaises(Exception, self.machine.save())
        self.machine.balance = 0
        self.assertRaises(Exception, self.machine.save())
        self.machine.balance = -9999999999999
        self.assertRaises(Exception, self.machine.save())
