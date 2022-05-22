from django.shortcuts import render
from .forms import requestForm
from django.http import HttpResponseRedirect

# Create your views here.
def add_req(request):
    submitted = False
    if request.method == "POST":
        form = requestForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('add_req?submitted=True')

    else:
        form = requestForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'realloc_emp.html',{'form':form, 'submitted':submitted})
