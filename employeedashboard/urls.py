from django.urls import path, include
from .views import emphome, empreq

urlpatterns = [
    path('employee/', emphome),
    path('seatrequests/', empreq)
]
