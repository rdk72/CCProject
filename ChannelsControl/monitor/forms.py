from django import forms
from .models import Incident

class DateTimeInput(forms.DateInput):
    input_type = 'datetime'

class IncidentEditForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields =  ['provider', 'channels', 'date_time_from', 'date_time_to', 'type', 'request', 'more_info', 'state' ]

        date_time_from = forms.DateTimeField(required=False, widget=DateInput(attrs={'type': 'datetime-local'}),
                                         initial=datetime.date.today(), localize=True)

        widgets={
            'provider':forms.Select(attrs={'class':'form-control'}),
            #'channels':forms.SelectMultiple(attrs={'class':'chained selectfilter','data-chainfield':'provider','data-url':'/chaining/filter/monitor/Channel/provider/monitor/Incident/channels','data-auto_choose':'false', 'name':'channels','data-field-name':'Список каналов','data-value':'[2]'}),
            #'channels':smart_selects.form_fields.ChainedSelectMultiple (attrs={'class':'form-control'}),
            #'date_time_from':DateTimeInput(),
            'date_time_to':forms.DateTimeInput(attrs={'class':'form-control'}),
            'type':forms.Select(attrs={'class':'form-control'}),
            'request':forms.TextInput(attrs={'class':'form-control'}),
            'more_info':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'state':forms.Select(attrs={'class':'form-control'}),
        }


