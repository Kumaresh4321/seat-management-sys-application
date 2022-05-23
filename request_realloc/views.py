from django.shortcuts import render
from .forms import requestForm
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from .models import rel_request
from employeedashboard.models import Employee

# Create your views here.
def add_req(request):
    submitted = False
    if request.method == "POST":
        form = requestForm(request.POST)
        if form.is_valid():
            form.save()
            email_bod = 'YOOO!I WANT DEATH :)'
            q=form.cleaned_data['lh_id']
            lh=Employee.objects.get(employee_id=q)
            em=lh.email_id
            email_sub='Please accept or deny seat change request for '+em
            email = EmailMessage(
                email_sub,
                email_bod,
                'noreply@semycolon.com',
                [em],
            )
            email.send(fail_silently=False)
            return HttpResponseRedirect('add_req?submitted=True')

    else:
        form = requestForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'realloc_emp.html',{'form':form, 'submitted':submitted})
