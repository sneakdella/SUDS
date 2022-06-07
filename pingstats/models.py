from django.db import models

# Create your models here.

# The device class defines the devices that will be monitored.
class Device(models.Model):
    device_name = models.CharField(max_length=200)
    ip_address = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.device_name

    def get_device_name(self):
        return self.device_name 

    def get_ip_address(self):
        return self.ip_address

    def get_status(self):
        return self.status

class Event(models.Model):
    event_type = models.CharField(max_length=200)
    event_description = models.CharField(max_length=200)
    event_severity_level = models.CharField(max_length=200)
    event_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_description
    
    def get_event_type(self):
        return self.event_type
    
    def get_event_description(self):
        return self.event_description
    
    def get_event_severity_level(self):
        return self.event_severity_level

    def get_event_timestamp(self):
        return self.event_timestamp