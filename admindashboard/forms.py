from django import forms
from django.forms import ModelForm
from seats.models import Seat

class allocateForm(ModelForm):
    class Meta:
        model = Seat
        fields = ('employee_id','shiftid','floor_number', 'tower_id', 'seat_number')