from django.contrib import admin

# Register your models here.

from . models import Device, Event

admin.site.register(Device)
admin.site.register(Event)