from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'admin_dash.html')

def requests(request):
    return render(request, 'allot_req.html')
