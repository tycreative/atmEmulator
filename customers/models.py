# Import for model creation
from django.db import models

# Import for model internals
from django.contrib.auth.models import User
from machines.models import Machine

# Importing other elements
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone


# ATM Account Model
class Account(models.Model):

    user = models.ForeignKey(
        User,
        related_name = "account",
        verbose_name = "User",
        help_text = "The user associated with this account.",
        default = None,
        on_delete = models.DO_NOTHING
        )

    number = models.CharField(
        verbose_name = "Account Number",
        help_text = "The number associated with this account.",
        max_length = 8,
        blank = False,
        unique = True,
        primary_key = True,
        validators = [RegexValidator(regex = "^(1-)?\d{8}$", message = "Field must contain 8 digits.")]
        )

    name = models.CharField(
        verbose_name = "Account Name",
        help_text = "The name of this account.",
        max_length = 150,
        blank = False
        )

    phone_number = models.CharField(
        verbose_name = "Phone Number",
        help_text = "The phone number associated with this account. Use format: XXX-XXX-XXXX.",
        max_length = 13,
        blank = False,
        validators = [RegexValidator(regex = "^(1-)?\d{3}-\d{3}-\d{4}$", message = "Phone number not in required format.")]
        )

    balance = models.DecimalField(
        verbose_name = "Balance",
        help_text = "The monetary balance of this account.",
        max_digits = 19,
        decimal_places = 2,
        default = 0.00,
        blank = False,
        validators = [MinValueValidator(-1000000000), MaxValueValidator(1000000000)]
        )

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.account_number)])

    def __str__(self):
        return f"#{self.number} ({self.name})"


# ATM Card Model
class Card(models.Model):

    account = models.ForeignKey(
        Account,
        related_name = "card",
        verbose_name = "Account",
        help_text = "The account associated with this ATM card.",
        default = None,
        on_delete = models.DO_NOTHING,
        blank = False
        )

    holder = models.CharField(
        verbose_name = "ATM Card Holder",
        help_text = "Name of the holder of this ATM card.",
        max_length = 150,
        blank = True
    )

    number = models.CharField(
        verbose_name = "ATM Card Number",
        help_text = "The number associated with this ATM card. Use format: XXXX-XXXX-XXXX-XXXX.",
        max_length = 19,
        blank = False,
        primary_key = True,
        validators = [RegexValidator(regex = "^(1-)?\d{4}-\d{4}-\d{4}-\d{4}$", message = "Card number not in required format.")]
        )

    pin = models.CharField(
        verbose_name = "PIN",
        help_text = "The personal identification number assigned to this ATM card.",
        max_length = 4,
        blank = False,
        validators = [RegexValidator(regex = "^(1-)?\d{4}$", message = "PIN number must be 4 digits.")]
        )

    status = models.BooleanField(
        verbose_name = "Active",
        help_text = "The current status of this ATM card.",
        default = True
        )

    date_issued = models.DateField(
        verbose_name = "Date of Issue",
        help_text = "The date in which this ATM card was issued.",
        default = timezone.now,
        editable = True,
        blank = False
        )

    expiry_date = models.DateField(
        verbose_name = "Expiration Date",
        help_text = "The date in which this ATM card expires.",
        editable = True,
        blank = False
        )

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.card_number)])

    def __str__(self):
        return f"Card #{self.number}"


# Transaction Model
class Transaction(models.Model):

    user = models.ForeignKey(
        User,
        related_name = "transaction",
        verbose_name = "User",
        on_delete = models.DO_NOTHING,
        blank = False
    )

    machine = models.ForeignKey(
        Machine,
        related_name = "transaction",
        verbose_name = "ATM",
        on_delete = models.DO_NOTHING,
        blank = False
    )

    account = models.ForeignKey(
        Account,
        related_name = "transaction",
        verbose_name = "Account",
        on_delete = models.DO_NOTHING,
        blank = False
    )

    date_time = models.DateTimeField(
        verbose_name = "Time of Transaction",
        default = timezone.now,
        blank = False
    )

    amount = models.DecimalField(
        verbose_name = "Transaction Amount",
        max_digits = 19,
        decimal_places = 2,
        blank = False,
        validators = [MinValueValidator(0.01), MaxValueValidator(1000000000)]
    )

    category = models.CharField(
        verbose_name = "Transaction Type",
        max_length = 15,
        blank = False
    )

    positive = models.BooleanField(
        verbose_name = "Positive Change",
        default = True,
        blank = False
    )

    def get_absolute_url(self):
        return reverse('model-detail-view', args = [str(self.id)])

    def __str__(self):
        return f"Transaction #{self.id}"