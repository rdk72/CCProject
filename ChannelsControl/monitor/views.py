from django.shortcuts import render, redirect
from datetime import datetime, date, timedelta
from django.http import HttpResponse, HttpResponseRedirect
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
    template_name = 'monitor/order.html'
    context_object_name = 'incidents'
#    paginate_by = 4

    def dispatch(self, request, *args, **kwargs):
        try:
            self.from_date = date.fromisoformat(self.request.GET.get('trip-from'))
            self.to_date = date.fromisoformat(self.request.GET.get('trip-to'))

        except:
            now_day = datetime.today()
            self.from_date = now_day - timedelta(days=now_day.weekday())
            self.to_date = now_day + timedelta(days=6 - now_day.weekday())

        # call the view
        return super(Order, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Отчет по пропаданиям каналов связи'
        context['from_date'] = self.from_date.strftime('%Y-%m-%d')
        context['to_date'] = self.to_date.strftime('%Y-%m-%d')
        return context

    def get_queryset(self):

        return Incident.objects.filter(date_time_from__date__gte=self.from_date,date_time_from__date__lte=self.to_date,)|Incident.objects.filter(date_time_to__date__gte=self.from_date,date_time_to__date__lte=self.to_date,)|Incident.objects.filter(date_time_from__date__lte=self.from_date,date_time_to__date__gte=self.to_date,)|Incident.objects.filter(date_time_from__date__lte=self.from_date,date_time_to=None,)

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


def Stat(request):
    try:
        from_date = date.fromisoformat(request.GET.get('trip-from'))
        to_date = date.fromisoformat(request.GET.get('trip-to'))

    except:
        now_day = datetime.today()
        from_date = now_day - timedelta(days=now_day.weekday())
        to_date = now_day + timedelta(days=6 - now_day.weekday())

    incidents = Incident.objects.filter(date_time_from__date__gte=from_date,date_time_from__date__lte=to_date,)|Incident.objects.filter(date_time_to__date__gte=from_date,date_time_to__date__lte=to_date,)|Incident.objects.filter(date_time_from__date__lte=from_date,date_time_to__date__gte=to_date,)|Incident.objects.filter(date_time_from__date__lte=from_date,date_time_to=None,)
    result = dict()
    if len(incidents)>0:
        for incident in incidents:
            if incident.date_time_from<from_date:
                incident.date_time_from=from_date
            if incident.date_time_to>to_date or incident.date_time_to = None:
                incident.date_time_to=to_date
            result.
    else:
        pass



    return render(request, 'monitor/stat.html', {
        'title':"Статистика пропаданий каналов",
        'from_date':from_date.strftime('%Y-%m-%d'),
        'to_date':to_date.strftime('%Y-%m-%d'),
    })

