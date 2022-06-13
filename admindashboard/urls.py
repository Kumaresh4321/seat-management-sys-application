from django.urls import path, include
from . import views
from accounts.views import logout_user
urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('requests/', views.requests, name="requests"),
    path('reports/', views.reports, name="reports"),
    path('generate_pdf/', views.generate_pdf, name="generate_pdf" ),
    path('logout/', logout_user, name="logout"),
    path('viewfloor1/', views.viewfloor1, name='viewfloor1'),
    path('viewfloor1/towera.svg', views.loadsvg, name='loadsvg'),
    path('viewseatinfo/', views.viewseatinfo, name="viewseatinfo"),
    path('allocateform/', views.allocateseat, name="allocateform")
]
