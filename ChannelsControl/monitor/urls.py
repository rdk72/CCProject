from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('history/', History.as_view(), name='history'),
    path('order/',  Order.as_view(), name='order'),
    path('incident/<int:incident_id>/', EditIncident.as_view(), name='incident'),
    path('incident/add_incident/', AddIncident.as_view(), name='add_incident'),
    path('incident/close/<int:incident_id>/', CloseRequest, name='add_incident'),

]