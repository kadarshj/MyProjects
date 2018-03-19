from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from account.models import User
from .models import Events

class EventsForm(forms.ModelForm):
    eventdate = forms.DateField(widget = forms.SelectDateWidget)

    class Meta:
        model = Events
        fields = ['events_type', 'description', 'date','price' ,'total_seats', 'eventdate' , 'cover_logo']
