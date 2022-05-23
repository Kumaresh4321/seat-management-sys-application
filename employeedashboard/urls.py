from django.urls import path, include
from .views import emphome

urlpatterns = [
    path('employee/', emphome),
]
