from django.shortcuts import render, redirect
from employeedashboard.views import displayemployee
from django.contrib.auth.decorators import login_required
from employeedashboard.models import Employee
from seats.models import Seat
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4
from datetime import datetime
from report.views import returnstats

# Create your views here.
@login_required(login_url='/login/')
def dashboard(request):
    context = returnstats(request)
    return render(request, 'admin_dash.html', context)

@login_required(login_url='/login/')
def requests(request):
    return render(request, 'allot_req.html', {})


def floor1(request):
    return render(request, 'trial.html', {})
