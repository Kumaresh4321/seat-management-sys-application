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
import math

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
    floor1_progress_un = []
    floor1_progress_buf = []
    for dept in departments:
        floor1_progress.append(math.floor(Seat.objects.filter(department_name=dept).filter(state='oc').count()*100/(Seat.objects.filter(department_name=dept).count() + 1)))
        floor1_progress_un.append(math.floor(Seat.objects.filter(department_name=dept).filter(state='un').count()*100/(Seat.objects.filter(department_name=dept).count() + 1)))
        floor1_progress_buf.append(math.floor(Seat.objects.filter(department_name=dept).filter(state='bu').count()*100/(Seat.objects.filter(department_name=dept).count() + 1)))
    print(floor1_progress_un)
    context = {
    'reportname_1': 'Floorwise Report: Occupied Seats',
    'floor1_marketing': floor1_progress[0],
    'floor1_operations': floor1_progress[1],
    'floor1_finance': floor1_progress[2],
    'floor1_sales': floor1_progress[3],
    'floor1_hr': floor1_progress[4],
    'floor1_technical': floor1_progress[5],
    'reportname_2': 'Floorwise Report: Unoccupied Seats',
    'floor1_marketing_un': floor1_progress_un[0],
    'floor1_operations_un': floor1_progress_un[1],
    'floor1_finance_un': floor1_progress_un[2],
    'floor1_sales_un': floor1_progress_un[3],
    'floor1_hr_un': floor1_progress_un[4],
    'floor1_technical_un': floor1_progress_un[5],
    'reportname_3': 'Floorwise Report: Buffer Seats',
    'floor1_marketing_buf': floor1_progress_buf[0],
    'floor1_operations_buf': floor1_progress_buf[1],
    'floor1_finance_buf': floor1_progress_buf[2],
    'floor1_sales_buf': floor1_progress_buf[3],
    'floor1_hr_buf': floor1_progress_buf[4],
    'floor1_technical_buf': floor1_progress_buf[5],
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
            if s == "Buffer": st = "bu"
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
    st = Seat.objects.filter(seat_id = info)
    context['seat_status'] = st[0].state
    context['seat_department_name'] = st[0].department_name
    context['seat_shiftid'] = st[0].shiftid
    context['employee_id'] = "null"
    if(st[0].employee_id != "null"):
        ed = Employee.objects.filter(employee_id = st[0].employee_id)
        context['employee_id'] = ed[0].employee_id
        context['employee_designation'] = ed[0].designation_name
    return render(request, 'seatinfo.html', context)

def loadsvg(request):
    return render(request, 'towera.svg', {})
