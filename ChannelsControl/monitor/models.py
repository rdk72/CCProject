from django.db import models
from django.urls import reverse
from smart_selects.db_fields import ChainedManyToManyField


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

class Provider(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    contacts = models.CharField(max_length=100, blank=True, verbose_name='Контакты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Оператор'
        verbose_name_plural = 'Операторы'
        ordering = ['name']

class Channel(models.Model):
    city_a = models.ForeignKey(City, on_delete=models.CASCADE, related_name='channel_city_a', verbose_name='Населенный пункт в точке А')
    city_b = models.ForeignKey(City, on_delete=models.CASCADE, related_name='channel_city_b', verbose_name='Населенный пункт в точке B')
    address_a = models.CharField(max_length=300, blank=True, verbose_name='Адрес подключения в точке А')
    address_b = models.CharField(max_length=300, blank=True, verbose_name='Адрес подключения в точке B')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name='Оператор')
    CHANNEL_TYPES = (
        ('L2', 'L2 type channel'),
        ('L3', 'L3 type channel'),
        ('S', 'Satellite type channel'),
        ('O', 'Other type channel'),
    )
    type = models.CharField(max_length=2, choices=CHANNEL_TYPES, default="O", verbose_name='Тип канала')
    bandwith = models.PositiveIntegerField(default=0, verbose_name='Ширина канала')
    contract_number = models.CharField(max_length=100, blank=True, verbose_name='Номер договора')
    more_info = models.CharField(max_length=400, blank=True, verbose_name='Дополнительная информация')

    def __str__(self):
        #return str(self.provider) + " " + str(self.city_a) +" - " + str(self.city_b)
        return str(self.city_a) +" - " + str(self.city_b)

    class Meta:
        verbose_name = 'Канал связи'
        verbose_name_plural = 'Каналы связи'
        ordering = ['provider']



class Incident(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name='Оператор')
    #channels = models.ManyToManyField(Channel, verbose_name="Список каналов")
    channels = ChainedManyToManyField(
        Channel,
        horizontal=True,
        verbose_name='Список каналов',
        chained_field="provider",
        chained_model_field="provider"
    )
    date_time_from = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, verbose_name="Время пропадания")
    date_time_to = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name="Время восстановления")
    STATE_TYPES = (
        ('I', 'Проблема актуальна'),
        ('C', 'Проблема закрыта'),
    )
    state = models.CharField(max_length=1, choices=STATE_TYPES, default="I", verbose_name="Статус")
    INCIDENT_TYPES = (
        ('U', 'Нестабильная работа'),
        ('L', 'Потеря пакетов'),
        ('F', 'Полное отсутствие'),
    )
    type = models.CharField(max_length=1, choices=INCIDENT_TYPES, default="F", verbose_name="Тип проблемы")
    request = models.CharField(max_length=100, blank=True, verbose_name="Номер заявки")
    REQUEST_TYPES = (
        ('N', 'Заявка не заводилась'),
        ('O', 'Заявка открыта'),
        ('C', 'Заявка закрыта'),
    )
    request_state = models.CharField(max_length=1, choices=REQUEST_TYPES, default="N", verbose_name="Статус заявки")
    more_info = models.CharField(max_length=400, blank=True, verbose_name='Примечание')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return str(self.date_time_from)

    def get_absolute_url(self):
        return reverse("incident", kwargs={"incident_id": self.pk})

    class Meta:
        verbose_name = 'Пропадание канала связи'
        verbose_name_plural = 'Пропадания каналов связи'
        ordering = ['-date_time_from']


# Create your models here.
