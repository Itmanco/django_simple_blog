from django import forms
from .models import UpcomingEvent
from bootstrap_datepicker_plus.widgets import DatePickerInput


class EventForm(forms.ModelForm):
    class Meta:
        model = UpcomingEvent
        fields = ('message', 'event_start_at', 'group')

        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control'}),
            'event_start_at': DatePickerInput(options={"format": "MM/DD/YYYY"}, attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['message'].label = ""