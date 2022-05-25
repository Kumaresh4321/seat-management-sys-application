from django.urls import path
from . import views
from .views import VerificationView


urlpatterns = [
    path('add_req',views.add_req),
    path('verify/<uidb64>/<token>', VerificationView.as_view(), name='verify')
]
