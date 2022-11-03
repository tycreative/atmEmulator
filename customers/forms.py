# Import for form creation
from django import forms

# Importing models
from .models import Account, Card, Transaction

# Import for validation-related handling
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist

# Importing other elements
from django.utils import timezone
import datetime


# User Login Form
class loginForm(forms.ModelForm):

    # Using Card model
    class Meta:
        model = Card
        fields = ["number", "pin"]
        help_texts = {
            "number": "",
            "pin": ""
        }
            
    # Don't need to validate if unique
    def validate_unique(self):
        exclude = self._get_validation_exclusions()

    # Return validated number
    def clean_number(self):
        try:
            card = Card.objects.get(number = self.cleaned_data.get("number"))
            today = timezone.now()

            if not hasattr(card, "account"):
                raise forms.ValidationError("Card does not have an account attached to it. Please contact an administrator to resolve this issue.")

            elif not card.status:
                raise forms.ValidationError("Card is not activated. Please contact an administrator to resolve this issue.")

            elif card.expiry_date <= datetime.date(today.year, today.month, today.day):
                raise forms.ValidationError("Card has expired. Please contact an administrator to resolve this issue.")

            return card.number

        except ObjectDoesNotExist:
            raise forms.ValidationError("Not a valid ATM card number.")

    # Return pin
    def clean_pin(self):
        return self.cleaned_data.get("pin")


# Funds Transfer Form
class transferForm(forms.ModelForm):

    dest = forms.CharField(
        label = "Destination Account",
        max_length = 8
    )

    # Using Transaction model
    class Meta:
        model = Transaction
        fields = ["account", "dest", "amount"]
        labels = {
            "account": "Source Account",
            "amount": "Amount to Transfer"
        }

    # Return validated account
    def clean_account(self):
        try:
            return Account.objects.get(number = self.cleaned_data.get("account").number)
        except ObjectDoesNotExist:
            raise forms.ValidationError("Account does not exist.")

    # Return validated destination
    def clean_dest(self):
        try:
            return Account.objects.get(number = self.cleaned_data.get("dest"))
        except ObjectDoesNotExist:
            raise forms.ValidationError("Account does not exist.")

    # Return validated amount
    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount == "":
            raise forms.ValidationError("Please enter an amount.")

        elif amount <= 0:
            raise forms.ValidationError("Please enter an amount greater than zero.")

        elif amount > 1000000000:
            raise forms.ValidationError("Please enter a smaller amount.")
        
        return amount


# Exchange Funds Form
class fundsForm(forms.ModelForm):

    # Using Transaction model
    class Meta:
        model = Transaction
        fields = ["account", "amount"]
        labels = {
            "account": "Account",
            "amount": "Amount"
        }

    # Return validated account
    def clean_account(self):
        try:
            return Account.objects.get(number = self.cleaned_data.get("account").number)
        except ObjectDoesNotExist:
            raise forms.ValidationError("Account does not exist.")

    # Return validated amount
    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount <= 0:
            raise forms.ValidationError("Please enter an amount greater than zero.")

        elif amount > 1000000000:
            raise forms.ValidationError("Please enter a smaller amount.")
        
        return amount


# Change PIN Form
class changePinForm(forms.ModelForm):

    new_pin = forms.CharField(
        label = "New PIN",
        max_length = 4,
        required = True,
        validators = [RegexValidator(regex = "^(1-)?\d{4}$", message = "PIN number must be 4 digits.")]
    )

    confirm_pin = forms.CharField(
        label = "Confirm PIN",
        max_length = 4,
        required = True,
        validators = [RegexValidator(regex = "^(1-)?\d{4}$", message = "PIN number must be 4 digits.")]
    )

    # Using Card model
    class Meta:
        model = Card
        fields = ["pin", "new_pin", "confirm_pin"]
        labels = {
            "pin": "Current PIN"
        }

    # Return pin
    def clean_pin(self):
        return self.cleaned_data.get("pin")

    # Return new pin
    def clean_new_pin(self):
        return self.cleaned_data.get("new_pin")

    # Return confirm pin
    def clean_confirm_pin(self):
        return self.cleaned_data.get("confirm_pin")


# Change Phone Number Form
class changePhoneForm(forms.ModelForm):

    # Using Account model
    class Meta:
        model = Account
        fields = ["phone_number"]
        labels = {
            "phone_number": "New Phone Number"
        }

    # Return phone number
    def clean_phone_number(self):
        return self.cleaned_data.get("phone_number")
