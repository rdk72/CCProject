from django import forms
from .models import Incident
import smart_selects.form_fields
class IncidentEditForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields =  ['provider', 'channels', 'date_time_from', 'date_time_to', 'type', 'request', 'more_info', 'state' ]


        widgets={
            'provider':forms.Select(attrs={'class':'form-control'}),
            #'channels':forms.SelectMultiple(attrs={'class':'chained selectfilter','data-chainfield':'provider','data-url':'/chaining/filter/monitor/Channel/provider/monitor/Incident/channels','data-auto_choose':'false', 'name':'channels','data-field-name':'Список каналов','data-value':'[2]'}),
            #'channels':smart_selects.form_fields.ChainedSelectMultiple (attrs={'class':'form-control'}),
            'date_time_from':forms.DateTimeInput(attrs={'class':'form-control'}),
        }



