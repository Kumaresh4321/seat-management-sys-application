from django.urls import path
from . import views
from .views import VerificationView, VerificationView2


urlpatterns = [
    path('add_req',views.add_req),
    path('verify/<uidb64>/<token>', VerificationView.as_view(), name='verify'),
    path('verify2/<uidb64>/<token>', VerificationView2.as_view(), name='verify2')
]
