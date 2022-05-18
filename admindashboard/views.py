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
#from datetime import today

departments = ['Marketing', 'Operations', 'Finance', 'Sales', 'Human Resources', 'Technical']

# Create your views here.
@login_required(login_url='/accounts/login/')
def dashboard(request):
    #context = displayemployee(request, request.user)
    context = returnstats(request)
    return render(request, 'admin_dash.html', context)

@login_required(login_url='/accounts/login/')
def requests(request):
    #context = displayemployee(request, request.user)
    return render(request, 'allot_req.html', {})

@login_required
def returnstats(request):
    floor1_progress = []
    for dept in departments:
        floor1_progress.append(Seat.objects.filter(department_name=dept).filter(state='oc').count()*100/Seat.objects.filter(department_name=dept).count())
    context = {
    'reportname': 'Floorwise Report',
    'floor1_marketing': floor1_progress[0],
    'floor1_operations': floor1_progress[1],
    'floor1_finance': floor1_progress[2],
    'floor1_sales': floor1_progress[3],
    'floor1_hr': floor1_progress[4],
    'floor1_technical': floor1_progress[5],
    }
    return context

@login_required
def reports(request):
    return render(request, 'reports.html', {})

@login_required
def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    #d = datetime.today().strftime('%Y-\m-%d')
    #response['Content-Disposition'] = f'inline; filename="{d}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize = A4)

    data = returnstats(request)

    p.setFont("Helvetica", 15, leading=None)
    p.drawString(260, 800, "Seat Management System")
    p.line(0, 780, 1000, 780)
    p.line(0, 778, 1000, 778)
    x1 = 20
    y1 = 750

    for key, value in data.items():
        p.setFont("Helvetica", 15, leading=None)
        p.drawString(x1, y1-12, f"{key}")
        p.drawString(x1, y1-32, f"{value}")
        y1 = y1-60

    #p.setTitle(f'Report on {d}')
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
