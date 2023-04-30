from django import forms
from .models import Incident


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"



class DateTimeLocalField(forms.DateTimeField):
    # Set DATETIME_INPUT_FORMATS here because, if USE_L10N
    # is True, the locale-dictated format will be applied
    # instead of settings.DATETIME_INPUT_FORMATS.
    # See also:
    # https://developer.mozilla.org/en-US/docs/Web/HTML/Date_and_time_formats

    input_formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M"
    ]
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M",attrs={'class':'form-control'})


class IncidentEditForm(forms.ModelForm):

    date_time_from = DateTimeLocalField()
    date_time_from.label="Время пропадания"

    date_time_to = DateTimeLocalField()
    date_time_to.label="Время восстановления"
    date_time_to.required=False

    class Meta:
        model = Incident
        fields =  ['provider', 'channels', 'date_time_from', 'date_time_to', 'type', 'request', 'more_info', 'state' ]

        widgets={
            'provider':forms.Select(attrs={'class':'form-select'}),
            #'channels':forms.SelectMultiple(attrs={'class':'chained selectfilter','data-chainfield':'provider','data-url':'/chaining/filter/monitor/Channel/provider/monitor/Incident/channels','data-auto_choose':'false', 'name':'channels','data-field-name':'Список каналов','data-value':'[2]'}),
            #'channels':smart_selects.form_fields.ChainedSelectMultiple (attrs={'class':'form-control'}),
            'type':forms.Select(attrs={'class':'form-select'}),
            'request':forms.TextInput(attrs={'class':'form-control'}),
            'more_info':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'state':forms.Select(attrs={'class':'form-select'}),
        }


