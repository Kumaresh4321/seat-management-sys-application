from django import forms
from .models import Request
from django.db.models import fields

# Create your models here.
class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = '__all__'



    #line_head_name = forms.CharField(label = 'Line Head Name',
    #widget=forms.TextInput(attrs={'placeholder':'Line Head Name'}))
    #line_head_id = forms.CharField(label = 'Line Head ID',
    #widget=forms.TextInput (attrs={'placeholder':'Line Head ID'}))
    #dept_head_name = forms.CharField(label = 'Department Head Name',
    #widget=forms.TextInput (attrs={'placeholder':'Department Head Name'}))
    #dept_head_id = forms.CharField(label = 'Department Head ID',
    #widget=forms.TextInput (attrs={'placeholder':'Department Head ID'}))
    #req_reason = forms.CharField(label = 'Reason for request',
    #widget=forms.Textarea(attrs={'placeholder':'Reason for request'}))
