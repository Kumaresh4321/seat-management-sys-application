from django.shortcuts import render
from employeedashboard.views import displayemployee

# Create your views here.
def dashboard(request):
    context = displayemployee(request, request.user)
    return render(request, 'admin_dash.html', context)

def requests(request):
    context = displayemployee(request, request.user)
    return render(request, 'allot_req.html', context)
