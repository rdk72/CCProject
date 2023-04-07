from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)

class Provider(models.Model):
    name = models.CharField(max_length=100)
    contacts = models.CharField(max_length=100, blank=True)

class Channel(models.Model):
    city_a = models.ForeignKey(City, on_delete=models.CASCADE, related_name='channel_city_a')
    city_b = models.ForeignKey(City, on_delete=models.CASCADE, related_name='channel_city_b')
    address_a = models.CharField(max_length=300, blank=True)
    address_b = models.CharField(max_length=300, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    CHANNEL_TYPES = (
        ('L2', 'L2 type channel'),
        ('L3', 'L3 type channel'),
        ('S', 'Satellite type channel'),
        ('O', 'Other type channel'),
    )
    type = models.CharField(max_length=2, choices=CHANNEL_TYPES, default="O")
    bandwith = models.PositiveIntegerField(default=0)
    contract_number = models.CharField(max_length=100, blank=True)
    more_info = models.CharField(max_length=400, blank=True)

class Incident(models.Model):
    channels = models.ManyToManyField(Channel, verbose_name="list of channels")
    date_time_from = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    date_time_to = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    STATE_TYPES = (
        ('I', 'In process'),
        ('C', 'Incident closed'),
    )
    state = models.CharField(max_length=1, choices=STATE_TYPES, default="I")
    request = models.CharField(max_length=100, blank=True)




# Create your models here.
