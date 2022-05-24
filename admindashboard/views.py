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
import json

# json_serializer = serializers.get_serializer("json")
departments = ['Marketing', 'Operations', 'Finance', 'Sales', 'Human Resources', 'Technical']

# Create your views here.
@login_required(login_url='/login/')
def dashboard(request):
    #context = displayemployee(request, request.user)
    context = returnstats(request)
    return render(request, 'admin_dash.html', context)

@login_required(login_url='/login/')
def requests(request):
    #context = displayemployee(request, request.user)
    return render(request, 'allot_req.html', {})

@login_required(login_url='/login/')
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
    print(context)
    return context

@login_required(login_url='/login/')
def reports(request):
    return render(request, 'reports.html', {})

def gen_data(floors, depts, statuses):
    data = {}
    if floors:
        floor_info = {}
        for f in floors:
            occ = Seat.objects.filter(state='oc').filter(floor_number=f).count()
            unocc = Seat.objects.filter(state='un').filter(floor_number=f).count()
            buff = Seat.objects.filter(state='bu').filter(floor_number=f).count()
            floor_info[f] = {
            'Occupied': occ,
            'Unoccupied': unocc,
            'Buffer': buff
            }
        data['Floors'] = floor_info
    if depts:
        dept_info = {}
        for d in depts:
            occ = Seat.objects.filter(state='oc').filter(department_name=d).count()
            unocc = Seat.objects.filter(state='un').filter(department_name=d).count()
            buff = Seat.objects.filter(state='bu').filter(department_name=d).count()
            dept_info[d] = {
            'Occupied': occ,
            'Unoccupied': unocc,
            'Buffer': buff
            }
        data['Department'] = dept_info
    if statuses:
        status_info = {}
        for s in statuses:
            if s == "Occupied": st = "oc"
            if s == "Unoccupied": st = "un"
            if s == "Buffer": st = "buff"
            status_info[s] = {
            'Total' : Seat.objects.filter(state=st).count()
            }

        data['Status'] = status_info

    print(data)

    return data


@login_required(login_url='/login/')
def generate_pdf(request):
    if request.method == 'POST':
        floor_select = request.POST.getlist('floor')
        dept_select = request.POST.getlist('dept')
        status_select = request.POST.getlist('status')
    print(floor_select)

    pdfdata = gen_data(floor_select, dept_select, status_select)
    response = HttpResponse(content_type='application/pdf')
    now = datetime.now()
    d = now.strftime('%Y-%m-%d')
    response['Content-Disposition'] = f"inline; filename = '{d}.pdf'"

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize = A4)

    p.setFont("Helvetica", 15, leading=None)
    p.drawString(220, 800, "Seat Management System")
    p.line(0, 780, 1000, 780)
    p.line(0, 778, 1000, 778)
    x1 = 20
    y1 = 750

    for key, value in pdfdata.items():
        y1 = y1 - 22
        if value:
            p.setFont("Helvetica", 15, leading=None)
            p.drawString(x1, y1-12, f"{key}")
            for k, v in value.items():
                p.setFont("Helvetica", 15, leading=None)
                p.drawString(x1+25, y1-32, f"{k}")
                y1 = y1-20
                for str, val in v.items():
                    p.setFont("Helvetica", 15, leading=None)
                    p.drawString(x1+40, y1-32, f"{str}: {val}")
                    y1 = y1-20


    p.setTitle(f'Report on {d}')
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

@login_required()
def viewfloor1(request):
    context = {}
    info = request.POST.get('seat_number')
    context['seat_number'] = info
    if context is None:
        return render(request, 'floor.html', {})
    else:
        print(context)
        return render(request, 'floor.html', context)


def viewseatinfo(request):
    # context = json.loads()
    # print(context)
    context = {}
    info = request.POST.get('seat_number')[4:]
    context['seat_number'] = info
    st = Seat.objects.filter(auto_increment_id = info)
    context['seat_status'] = st[0].state
    return render(request, 'seatinfo.html', context)

def loadsvg(request):
    return render(request, 'towera.svg', {})
