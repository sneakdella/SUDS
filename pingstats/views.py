from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Device, Event
from django.template import loader

"""
API
"""
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.views import View
import json

@login_required
def home(request):
    current_user = request.user
    dev_objects_list = Device.objects.all()
    ping_status_down_switch = "FALSE"

    DEVICES_DOWN = dev_objects_list.filter(status="DOWN").count()
    DEVICES_UP = dev_objects_list.filter(status="UP").count()
    TOTAL_DEVICES = dev_objects_list.count()
    PERCENT_UP = str(round(((int(DEVICES_UP)/int(TOTAL_DEVICES))*100)))+"%"

    for specific_device in range(len(dev_objects_list)):
        if dev_objects_list[specific_device].status == "DOWN":
            ping_status_down_switch = "TRUE"

    recent_events_list = Event.objects.all().order_by('-id')[:10]
    
    
    context = {
        'dev_objects_list': dev_objects_list,
        'ping_status_down_switch': ping_status_down_switch,
        'recent_events_list': recent_events_list,
        'DEVICES_DOWN': DEVICES_DOWN,
        'DEVICES_UP': DEVICES_UP,
        'TOTAL_DEVICES': TOTAL_DEVICES,
        'PERCENT_UP': PERCENT_UP,
        'current_user': current_user
    }
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))

@login_required
def event(request):
    current_user = request.user
    events_object_list = Event.objects.all().order_by('-id')
    context = {
        'event_objects_list': events_object_list,
        'current_user': current_user
    }
    template = loader.get_template('events.html')
    return HttpResponse(template.render(context, request))

@login_required
def listDevices(request):
    current_user = request.user
    dev_objects_list = Device.objects.all().order_by("device_name")
    context = {
        'dev_objects_list': dev_objects_list,
        'current_user': current_user
    }
    template = loader.get_template('device_list.html')
    return HttpResponse(template.render(context, request))

@login_required
def about(request):
    current_user = request.user
    context = {
        'current_user': current_user
    }
    template = loader.get_template('about.html')
    return HttpResponse(template.render(context, request))

@method_decorator(csrf_exempt, name="dispatch")
class APIReceiver(View):
    def post(self, request):
        
        data = json.loads(request.body.decode("utf-8"))
        d_name = data.get('device_name')
        d_ip_address= data.get('ip_address')
        d_status = data.get('status')

        device_data = {
            'device_name': d_name,
            'ip_address': d_ip_address,
            'status': d_status,
        }

        new_device = Device.objects.create(**device_data)

        data = {
            "message": f"New device added to pingstats model db: {new_device.id}"
        }
        return JsonResponse(data, status=201)
    
    def get(self, request):
        items_count = Device.objects.count()
        items = Device.objects.all()
        items_data = []
        for item in items:
            items_data.append({
                'id': item.id,
                'device_name': item.device_name,
                'ip_address': item.ip_address,
                'status': item.status,
            })
        data = {
            'items': items_data,
            'count': items_count,
        }
        return JsonResponse(data)

    def patch(self, request, dev_id):
        data = json.loads(request.body.decode("utf-8"))
        specificDevice = Device.objects.get(id=dev_id)
        specificDevice.status = data['status']
        specificDevice.save()

        data = {
            'message': f'Device ID: {specificDevice.id} set to {specificDevice.status}'
        }

        return JsonResponse(data)

@method_decorator(csrf_exempt, name="dispatch")
class APIEventReciever(View):
    def post(self, request):
        
        data = json.loads(request.body.decode("utf-8"))
        e_type = data.get('event_type')
        e_description= data.get('event_description')
        e_severity = data.get('event_severity_level')

        event_data = {
            'event_type': e_type,
            'event_description': e_description,
            'event_severity_level': e_severity,
        }

        new_event = Event.objects.create(**event_data)

        data = {
            "message": f"Event {new_event.id} created and logged."
        }
        return JsonResponse(data, status=201)