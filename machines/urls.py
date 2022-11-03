from django.urls import path

# Importing all machine views
from .views import *

app_name = "machines"

urlpatterns = [
    path("", loginView, name = "login")
]