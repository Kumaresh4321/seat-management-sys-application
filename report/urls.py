from django.urls import path, include
from . import views

urlpatterns = [
    path('reports/', views.reports, name="reports"),
    path('generate_pdf/', views.generate_pdf, name="generate_pdf" ),
    ]
