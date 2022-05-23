from django.urls import path, include
from . import views
from accounts.views import logout_user

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', logout_user, name="logout"),
    path('floor1/', views.floor1, name="floor1"),
]
