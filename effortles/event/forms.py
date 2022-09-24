from attr import fields
from django import forms
from .models import Event


class EventForm(forms.ModelForm):

    date = forms.DateField(
            widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Event
        fields = ['created_by', 'event_name', 'date', 'amount']
