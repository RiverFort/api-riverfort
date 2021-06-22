from django.urls import path
from . import views

# app_name = 'notification'

urlpatterns = [
  path("add-company/", views.add_company, name="add_company"),
]