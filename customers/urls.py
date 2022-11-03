from django.urls import path

# Importing all customer views
from .views import *

app_name = "customers"

urlpatterns = [
    path("logout/", logoutView, name = "logout"),
    path("dashboard/", dashboardView, name = "dashboard"),
    path("accounts/<str:number>/", accountView, name = "account"),
    path("cards/<str:number>/", cardView, name = "card"),
    path("transfers/<str:number>/", transfersView, name = "transfers"),
    path("transfer/", transferView, name = "transfer"),
    path("deposits/<str:number>/", depositsView, name = "deposits"),
    path("deposit/", depositView, name = "deposit"),
    path("withdrawals/<str:number>/", withdrawalsView, name = "withdrawals"),
    path("withdrawal/", withdrawalView, name = "withdrawal"),
    path("transactions/<int:page>/", transactionsView, name = "transactions"),
    path("cards/update/<str:number>/", changePinView, name = "changePIN"),
    path("accounts/update/<str:number>/", changePhoneView, name = "changePhone")
]