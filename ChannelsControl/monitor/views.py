from django.shortcuts import render

from django.http import HttpResponse



def index(request):
    #incidents = Incidents.objects.all()
    context={'title':'Актуальные проблемы каналов'}
    return render(request, 'monitor/index.html', context=context)
