from django.shortcuts import render, redirect
from datetime import datetime, date, timedelta, time
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import *
from .forms import *
import zoneinfo
from django.db.models import Q


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
    model = Incident
    template_name = 'monitor/add_incident.html'
    form_class = IncidentEditForm
    #fields = ['provider', 'channels', 'date_time_from', 'date_time_to', 'state', 'type',  'request', 'request_state', 'more_info']
        # success_url = reverse_lazy('home')
        # login_url = '/admin/'
    raise_exception = True

#класс для хранения элементов статистики (каналов)
class StatItem:
    def __init__(self, chan_name, provider_name, duration=0, count=0):
        self.duration = duration
        self.count = count
        self.chan_name = chan_name
        self.provider_name = provider_name

    def add(self,duration):
        self.duration += duration
        self.count += 1

def Stat(request):
    try:
        #получили date_time в get параметрах
        from_date_time = datetime.fromisoformat(request.GET.get('trip-from'))
        to_date_time = datetime.fromisoformat(request.GET.get('trip-to'))

    except:
        now_day = datetime.today()
        from_date_time = now_day - timedelta(days=now_day.weekday())
        from_date_time=from_date_time.replace(hour=0, minute=0)
        to_date_time = now_day + timedelta(days=7 - now_day.weekday())
        to_date_time=to_date_time.replace(hour=0, minute=0)

    try:
        #получили provider в get параметрах
        provider = int(request.GET.get('provider'))
    except:
        provider = 0


    # устанавливаем метку часового пояса
    from_date_time = from_date_time.replace(tzinfo=zoneinfo.ZoneInfo("UTC"))
    to_date_time = to_date_time.replace(tzinfo=zoneinfo.ZoneInfo("UTC"))


    if provider:
        incidents = Incident.objects.filter(
            Q(provider__pk=provider) &
            (Q(date_time_from__date__gte=from_date_time, date_time_from__date__lte=to_date_time) |
            Q(date_time_to__date__gte=from_date_time, date_time_to__date__lte=to_date_time, ) |
            Q(date_time_from__date__lte=from_date_time, date_time_to__date__gte=to_date_time, ) |
            Q(date_time_from__date__lte=from_date_time, date_time_to=None, )))

    else:
        incidents = Incident.objects.filter(
            Q(date_time_from__date__gte=from_date_time, date_time_from__date__lte=to_date_time) |
            Q(date_time_to__date__gte=from_date_time, date_time_to__date__lte=to_date_time, ) |
            Q(date_time_from__date__lte=from_date_time, date_time_to__date__gte=to_date_time, ) |
            Q(date_time_from__date__lte=from_date_time, date_time_to=None, ))

    result = dict()
    if len(incidents)>0:
        for incident in incidents:
            if incident.date_time_from < from_date_time:
                incident.date_time_from = from_date_time
            if incident.date_time_to is None:   #если канал(ы) не восстановился
                incident.date_time_to = to_date_time
            elif incident.date_time_to > to_date_time: #если канал восстановился позднее рассматриваемого интервала
                incident.date_time_to = to_date_time

            for channel in incident.channels.all():
                result.setdefault(channel.pk, StatItem(channel.__str__(),channel.provider)).add(incident.date_time_to.timestamp()-incident.date_time_from.timestamp())
    else:
        pass

    #выполняем сортировку по суммарной продолжительности пропадания канала
    sorted_tuple = sorted(result.items(), key=lambda x: -x[1].duration) #x[0] pk канала, x[1] StatItem канала
    result = dict(sorted_tuple)

    #формируем список операторов для заполнения select'а
    providers = Provider.objects.all()

    return render(request, 'monitor/stat.html', {
        'title':"Статистика пропаданий каналов",
        'from_date_time':from_date_time.strftime('%Y-%m-%dT%H:%M'),
        'to_date_time':to_date_time.strftime('%Y-%m-%dT%H:%M'),
        'StatItems':result,
        'providers':providers,
        'provider_selected':provider,
    })

