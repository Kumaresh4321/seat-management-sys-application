from django.urls import path
from . import views

urlpatterns = [
    path('add_req',views.add_req),
]
