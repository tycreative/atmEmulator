# Imports for rendering and redirecting
from django.shortcuts import render, redirect

# Imports for form validation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout

# Importing models
from customers.models import Card
from .models import Machine

# Importing forms
from customers.forms import loginForm

# Importing other elements
from customers.views import session


# User Login View
def loginView(request):

    # Proceed to dashboard if user is logged in
    if request.user.is_authenticated:
        return redirect("customers:dashboard")

    display = "none"
    # User Login Form
    form = loginForm(request.POST or None)
    if request.method == "POST":
        display = "block"

        # Get Machine user is accessing from
        if session("machine") == "":
            try:
                session("machine", Machine.objects.get(pk = request.POST.get("machine")))
            except ObjectDoesNotExist:
                form.add_error(None, "Please select a machine first.")

        # Form Validation
        if form.is_valid():
            card = Card.objects.get(number = form.cleaned_data["number"])
            pin = form.cleaned_data["pin"]

            if card.pin != pin:
                form.add_error("pin", "PIN is incorrect.")

            else:
                account = card.account

                if not hasattr(account, "user"):
                    form.add_error(None, "Linked account does not have a user attached to it. Please contact an administrator to resolve this issue.")

                else:
                    # Login user and check that it worked
                    user = account.user
                    login(request, user)
                    if not user.is_authenticated:
                        form.add_error(None, "Unable to login. Please check your login details and try again. If the problem persists, contact an administrator.")
                    else:
                        return redirect("customers:dashboard")

    # Template Context
    context = {
        "form": form,
        "machines": Machine.objects.all(),
        "display": display,
        "selected": session("machine")
    }
    return render(request, "login.html", context)