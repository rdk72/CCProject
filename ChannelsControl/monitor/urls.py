from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('incident/<int:pk>/', EditIncident.as_view(), name='edit_incident'),
    path('incident/add_incident/', AddIncident.as_view(), name='add_incident'),

]