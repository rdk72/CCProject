from django.shortcuts import render, redirect
from datetime import datetime, date, time
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import *
from .forms import *

def CloseRequest(request,incident_id):
    inc_state = bool(request.GET.get("change_inc_state", False))
    if inc_state:
        Incident.objects.filter(pk=incident_id).update(request_state='C',state='C')
    else:
        Incident.objects.filter(pk=incident_id).update(request_state='C')
    return redirect('home')


class Home(ListView):
    model = Incident
    template_name = 'monitor/index.html'
    context_object_name = 'incidents'
#    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Актуальные проблемы каналов связи'
        return context

    def get_queryset(self):
        return Incident.objects.filter(state="I")

class History(ListView):
    model = Incident
    template_name = 'monitor/index.html'
    context_object_name = 'incidents'
#    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'История проблем каналов связи'
        return context

class Order(ListView):
    model = Incident
    template_name = 'monitor/index.html'
    context_object_name = 'incidents'
#    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Отчет по пропаданиям каналов связи'
        return context

    def get_queryset(self):
        return Incident.objects.filter(state="I",date_time_from__date__gte=date(2023, 5, 1),date_time_to__date__lte=date(2023, 5, 2),)

class EditIncident(UpdateView):
    model = Incident
    #fields = ['provider', 'channels', 'date_time_from', 'date_time_to', 'type', 'request', 'more_info', 'state']
    form_class = IncidentEditForm
    context_object_name = 'incident_item'
    template_name = 'monitor/incident.html'
    pk_url_kwarg = 'incident_id'

    def get_success_url(self):
        return reverse("home")



class AddIncident(CreateView):
 #       form_class = NewsForm
    template_name = 'news/add_incident.html'
        # success_url = reverse_lazy('home')
        # login_url = '/admin/'
    raise_exception = True

#def index(request):
    #incidents = Incidents.objects.all()
#    context={'title':'Актуальные проблемы каналов'}
 #   return render(request, 'monitor/index.html', context=context)
