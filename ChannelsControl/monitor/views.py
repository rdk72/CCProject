from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import *
from .forms import *

class Home(ListView):
    model = Incident
    template_name = 'monitor/index.html'
    context_object_name = 'incidents'
#    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Актуальные проблемы каналов связи'
        return context

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
