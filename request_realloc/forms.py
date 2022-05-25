from django import forms
from django.forms import ModelForm
from .models import rel_request

class requestForm(ModelForm):
    class Meta:
        model = rel_request
        fields = ('lh_name','lh_id','dh_name','dh_id','reason')

        widgets = {
            'lh_name': forms.TextInput(attrs={'class':'form-control text-center', 'placeholder':'Line Head\'s Name'}),
            'lh_id': forms.TextInput(attrs={'class':'form-control text-center', 'placeholder':'Line Head\'s ID'}),
            'dh_name':forms.TextInput(attrs={'class':'form-control text-center', 'placeholder':'Dept Head\'s Name'}),
            'dh_id':forms.TextInput(attrs={'class':'form-control text-center', 'placeholder':'Dept Head\'s ID'}),
            'reason':forms.Textarea(attrs={'class':'form-control text-center', 'placeholder':'Reason', 'rows':'10'}),
        }
