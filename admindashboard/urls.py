from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('requests/', views.requests, name="requests"),
    path('reports/', views.reports, name="reports"),
    path('generate_pdf/', views.generate_pdf, name="generate_pdf" )
]
