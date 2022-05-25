from django.urls import path, include
from .views import emphome, empreq
from request_realloc.views import add_req

urlpatterns = [
    path('employee/', emphome),
    path('seatrequests/', add_req)
]
