from django.urls import path, include
from employeedashboard import views
from admindashboard.views import requests
from .views import submit_request

urlpatterns = [
    path('seatrequests/', submit_request, name="seatrequests"),
    path('requests/', requests, name="requests"),
]
