# Imports for rendering and redirecting
from django.shortcuts import render, redirect

# Imports for form validation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

# Importing models
from .models import Account, Card, Transaction
from machines.models import Machine, Refill

# Importing forms
from .forms import *

# Importing other elements
from django.contrib import messages
from django.utils import timezone
import datetime


# Global Session Variables
variables = {}

# Session Variables Helper Function
def session(var, value = None):
    global variables
    if value == None:
        if var in variables.keys():
            return variables[var]
        return ""
    else:
        variables[var] = value


# New Transaction Helper Function
def newTransaction(user, machine, account, amount, category, positive):
    try:
        return Transaction(user = user, machine = machine, account = account, amount = amount, category = category, positive = positive) 
    except:
        return None


# User Logout View
@login_required(login_url = "machines:login")
def logoutView(request):
    logout(request)
    # Reset session variables
    global variables
    variables = {}
    return redirect("machines:login")


# User Dashboard View
@login_required(login_url = "machines:login")
def dashboardView(request):
    # Dashboard Content
    accounts = Account.objects.filter(user = request.user)
    cards = Card.objects.filter(account__in = accounts)
    today = timezone.now()

    # Template Context
    context = {
        "accounts": accounts,
        "cards": cards,
        "date": datetime.date(today.year, today.month, today.day),
        "header": f"Welcome back, {request.user.first_name}.",
        "redirect": "accounts",
        "sections": ["accounts/accounts.html", "cards/cards.html", "actions.html"]
    }
    return render(request, "customers/index.html", context)


# Recent Transfers View
@login_required(login_url = "machines:login")
def transfersView(request, number = ""):
    accounts = Account.objects.filter(user = request.user)
    transactions = Transaction.objects.order_by("-date_time").filter(category = "Transfer", user = request.user)[:15]

    # Sort by Account Number
    if number != "":
        try:
            account = Account.objects.filter(user = request.user).get(number = number)
            transactions = Transaction.objects.order_by("-date_time").filter(category = "Transfer", user = request.user).filter(account = account)[:15]
        except ObjectDoesNotExist:
            pass

    # Template Context
    context = {
        "transactions": transactions,
        "accounts": accounts,
        "header": "Cash Where You Need It",
        "type": "transfers",
        "action": "Start a Transfer",
        "redirect": "transfers",
        "sections": ["accounts/accounts.html", "transactions/simple.html"]
    }
    return render(request, "customers/index.html", context)


# New Transfer View
@login_required(login_url = "machines:login")
def transferView(request, number = ""):    
    accounts = Account.objects.filter(user = request.user)
    transactions = Transaction.objects.order_by("-date_time").filter(category = "Transfer").filter(user = request.user)[:7]

    # New Transfer Form
    form = transferForm(request.POST or None)
    form.fields["account"].queryset = accounts
    if request.method == "POST" and form.is_valid():
        source = form.cleaned_data["account"]
        dest = form.cleaned_data["dest"]
        amount = form.cleaned_data["amount"]

        # Form Validation
        if source == dest:
            form.add_error("dest", "Cannot transfer to same account.")

        elif source.balance < amount:
            form.add_error("account", "Account has insufficient funds.")

        else:
            sent = newTransaction(source.user, session("machine"), source, amount, "Transfer", False)
            receive = newTransaction(dest.user, session("machine"), dest, amount, "Transfer", True)

            if sent == None or receive == None:
                form.add_error(None, "Transfer failed. Please check details and try again. If the problem persists, contact an administrator.")

            else:
                # Update Database
                source.balance -= amount
                dest.balance += amount
                source.save()
                dest.save()
                sent.save()
                receive.save()
                messages.add_message(request, 25, f"Successfully transferred ${amount} from Account {source} to destination account.")
                return redirect("customers:transfer")

    # Template Context
    context = {
        "form": form,
        "selected": number,
        "accounts": accounts,
        "transactions": transactions,
        "messages": messages.get_messages(request),
        "header": "Cash Where You Need It",
        "title": "New Transfer",
        "type": "transfers",
        "button": "Submit",
        "sections": ["form.html", "transactions/simple.html"]
    }
    return render(request, "customers/index.html", context)


# Recent Deposits View
@login_required(login_url = "machines:login")
def depositsView(request, number = ""):
    accounts = Account.objects.filter(user = request.user)
    transactions = Transaction.objects.order_by("-date_time").filter(category = "Deposit", user = request.user)[:15]

    # Sort by Account Number
    if number != "":
        try:
            account = Account.objects.filter(user = request.user).get(number = number)
            transactions = Transaction.objects.order_by("-date_time").filter(category = "Deposit", user = request.user).filter(account = account)[:15]
        except ObjectDoesNotExist:
            pass

    # Template Context
    context = {
        "selected": number,
        "accounts": accounts,
        "transactions": transactions,
        "header": "Save Cash For Later",
        "type": "deposits",
        "action": "Start a Deposit",
        "redirect": "deposits",
        "sections": ["accounts/accounts.html", "transactions/simple.html"]
    }
    return render(request, "customers/index.html", context)


# New Deposit View
@login_required(login_url = "machines:login")
def depositView(request, number = ""):
    accounts = Account.objects.filter(user = request.user)
    transactions = Transaction.objects.order_by("-date_time").filter(category = "Deposit").filter(user = request.user)[:7]

    # New Deposit Form
    form = fundsForm(request.POST or None)
    form.fields["account"].queryset = accounts
    if request.method == "POST" and form.is_valid():
        account = form.cleaned_data["account"]
        amount = form.cleaned_data["amount"]
        machine = session("machine")

        # Form Validation
        transaction = newTransaction(account.user, session("machine"), account, amount, "Deposit", True)
        refill = Refill(machine=machine, amount=amount, previous=machine.balance)

        if transaction == None:
            form.add_error(None, "Deposit failed. Please check details and try again. If the problem persists, contact an administrator.")

        else:
            # Update Database
            refill.save()
            account.balance += amount
            machine.balance += amount
            account.save()
            machine.save()
            transaction.save()
            messages.add_message(request, 25, f"Successfully deposited ${amount} to Account {account}.")
            return redirect("customers:deposit")

    # Template Context
    context = {
        "form": form,
        "selected": number,
        "accounts": accounts,
        "transactions": transactions,
        "messages": messages.get_messages(request),
        "header": "Save Cash For Later",
        "title": "New Deposit",
        "type": "deposits",
        "button": "Submit",
        "sections": ["form.html", "transactions/simple.html"]
    }
    return render(request, "customers/index.html", context)


# Recent Withdrawals View
@login_required(login_url = "machines:login")
def withdrawalsView(request, number = ""):
    accounts = Account.objects.filter(user = request.user)
    transactions = Transaction.objects.order_by("-date_time").filter(category = "Withdrawal", user = request.user)[:15]

    # Sort by Account Number
    if number != "":
        try:
            account = Account.objects.filter(user = request.user).get(number = number)
            transactions = Transaction.objects.order_by("-date_time").filter(category = "Withdrawal", user = request.user).filter(account = account)[:15]
        except ObjectDoesNotExist:
            pass

    # Template Context
    context = {
        "selected": number,
        "accounts": accounts,
        "transactions": transactions,
        "header": "Cash When You Need It",
        "type": "withdrawals",
        "action": "Start a Withdrawal",
        "redirect": "withdrawals",
        "sections": ["accounts/accounts.html", "transactions/simple.html"]
    }
    return render(request, "customers/index.html", context)


# New Withdrawal View
@login_required(login_url = "machines:login")
def withdrawalView(request, number = ""):
    accounts = Account.objects.filter(user = request.user)
    transactions = Transaction.objects.order_by("-date_time").filter(category = "Withdrawal").filter(user = request.user)[:7]

    # New Withdrawal Form
    form = fundsForm(request.POST or None)
    form.fields["account"].queryset = accounts
    if request.method == "POST" and form.is_valid():
        account = form.cleaned_data["account"]
        amount = form.cleaned_data["amount"]
        machine = session("machine")

        # Form Validation
        if (machine.balance - amount) <= machine.minimum:
            form.add_error(None, "This machine does not have enough funds currently to complete this request.")

        else:
            transaction = newTransaction(account.user, session("machine"), account, amount, "Withdrawal", False)

            if transaction == None:
                form.add_error(None, "Withdrawal failed. Please check details and try again. If the problem persists, contact an administrator.")

            else:
                # Update Database
                account.balance -= amount
                machine.balance -= amount
                account.save()
                machine.save()
                transaction.save()
                messages.add_message(request, 25, f"Successfully withdrew ${amount} from Account {account}.")
                return redirect("customers:withdrawal")

    # Template Context
    context = {
        "form": form,
        "selected": number,
        "accounts": accounts,
        "transactions": transactions,
        "messages": messages.get_messages(request),
        "header": "Cash When You Need It",
        "title": "New Withdrawal",
        "type": "withdrawals",
        "button": "Submit",
        "sections": ["form.html", "transactions/simple.html"]
    }
    return render(request, "customers/index.html", context)


# All Transactions View
@login_required(login_url = "machines:login")
def transactionsView(request, page):

    # Get Range of Page
    start = max(0, (page - 1) * 24)
    end = start + 24

    # Get Preferred Sorting
    if request.method == "POST":
        session("sorting", request.POST.get("sort"))

    if session("sorting") == "":
        session("sorting", "-date_time")

    # Template Context
    context = {
        "transactions": Transaction.objects.order_by(session("sorting")).filter(user = request.user)[start:end],
        "pages": list(range(1, round(Transaction.objects.filter(user = request.user).count() / 24) + 2)),
        "header": "Transaction History",
        "sections": ["transactions/full.html"]
    }
    return render(request, "customers/index.html", context)


# Account Details View
@login_required(login_url = "machines:login")
def accountView(request, number):
    account = None

    # Get User's Account
    try:
        account = Account.objects.get(user = request.user, number = number)
    except ObjectDoesNotExist:
        pass
    
    # Template Context
    context = {
        "account": account,
        "cards": Card.objects.filter(account = account).count(),
        "header": "Your Account",
        "sections": ["accounts/account.html", "accounts/actions.html"]
    }
    return render(request, "customers/index.html", context)


# Card Details View
@login_required(login_url = "machines:login")
def cardView(request, number):
    card = None
    today = timezone.now()

    # Get User's Card
    try:
        card = Card.objects.get(number = number, account__in = Account.objects.filter(user = request.user))
    except ObjectDoesNotExist:
        pass

    # Template Context
    context = {
        "card": card,
        "date": datetime.date(today.year, today.month, today.day),
        "header": "Your ATM Card",
        "sections": ["cards/card.html", "cards/actions.html"]
    }
    return render(request, "customers/index.html", context)


# Change PIN View
@login_required(login_url = "machines:login")
def changePinView(request, number):

    card = None
    # Get User's Card
    try:
        card = Card.objects.get(number = number, account__in = Account.objects.filter(user = request.user))
    except ObjectDoesNotExist:
        pass

    # Change PIN Form
    form = changePinForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        current_pin = form.cleaned_data["pin"]
        new_pin = form.cleaned_data["new_pin"]
        confirm_pin = form.cleaned_data["confirm_pin"]

        # Form Validation
        if card != None:
            if card.pin != current_pin:
                form.add_error("pin", "Incorrect PIN.")

            elif current_pin == new_pin:
                form.add_error("new_pin", "New PIN cannot be current PIN.")

            elif new_pin != confirm_pin:
                form.add_error("confirm_pin", "PIN does not match.")

            else:
                # Update Database
                card.pin = new_pin
                card.save()
                messages.add_message(request, 25, f"Card #{card.number} was updated successfully.")
                return redirect("customers:card", number=card.number)
        else:
            form.add_error(None, "This card does not belong to you.")

    # Template Context
    context = {
        "card": card,
        "form": form,
        "header": f"Modifying {card}",
        "title": "Change PIN",
        "button": "Update",
        "sections": ["form.html", "cards/actions.html"]
    }
    return render(request, "customers/index.html", context)


# Change Phone Number View
@login_required(login_url = "machines:login")
def changePhoneView(request, number):

    account = None

    # Get User's Account
    try:
        account = Account.objects.get(user = request.user, number = number)
    except ObjectDoesNotExist:
        pass

    # Change Phone Number Form
    form = changePhoneForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        phone_number = form.cleaned_data["phone_number"]

        # Form Validation
        if account != None:
            if account.phone_number == phone_number:
                form.add_error("phone_number", "New phone number cannot be same as current.")

            else:
                account.phone_number = phone_number
                account.save()
                messages.add_message(request, 25, f"Account {account} was updated successfully.")
                return redirect("customers:account", number=account.number)

        else:
            form.add_error(None, "This account does not belong to you.")

    # Template Context
    context = {
        "account": account,
        "form": form,
        "header": f"Modifying Account {account}",
        "title": "Change Phone Number",
        "button": "Update",
        "sections": ["form.html", "accounts/actions.html"]
    }
    return render(request, "customers/index.html", context)