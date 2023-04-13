from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('incident/<int:incident_id>/', EditIncident.as_view(), name='incident'),
    path('incident/add_incident/', AddIncident.as_view(), name='add_incident'),

]