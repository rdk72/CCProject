from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from .models import *

class Home(ListView):
    model = Incident
    template_name = 'monitor/index.html'
    context_object_name = 'incidents'
#    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Актуальные проблемы каналов связи'
        return context

    class EditIncident(DetailView):
        model = Incident
        context_object_name = 'incident_item'



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
