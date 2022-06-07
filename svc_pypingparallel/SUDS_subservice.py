import json
import requests
import concurrent.futures
import subprocess
import time

while True:
    # Pulls the json data using requests
    r = requests.get('http://127.0.0.1:8000/api/')

    # List of Device Objects from the Device Class
    deviceObjList = []

    # Define Class Object JSON data will dump into
    class Device():
        def __init__(self, dev_id, device_name, ip_address, status):
            self.dev_id = dev_id
            self.device_name = device_name
            self.ip_address = ip_address
            self.status = status
            self.change_detected = "NO"
        
        def __str__(self):
            just_return_string = (self.device_name + self.ip_address)
            return (just_return_string)
        
        def dev_id(self):
            return(self.dev_id)

        def device_name(self):
            return (self.device_name)
        
        def ip_address(self):
            return(self.ip_address)

        def status(self):
            return(self.status)
        
        def get_change_detected(self):
            return(self.change_detected)

        def set_status(self, new_status):
            self.status = new_status
            self.change_detected = "YES"

    # Begin dumping JSON into the class, the JSON data is returned in a dict, but the devices are dumped under a list named "object" which has another dictionary.
    json_results = r.json()
    for item in json_results['items']:
        new_device_obj = []
        for key in item:
            new_device_obj.append(item[key])
        deviceObjList.append(Device(new_device_obj[0], new_device_obj[1], new_device_obj[2], new_device_obj[3]))

    # This is the ping command, it takes the ID and IP Address of an object, checks if the IP up or down via the ping subprocess. Returns ID and STATUS
    # If the device is unreachable, Ping status is DOWN
    # If the device is reachable, Ping status is UP
    # If the subprocess closes with Exit Code 1, Ping status Is DOWN
    def do_ping(ip_address, dev_id):
        result = subprocess.run(["ping","-n","1", ip_address], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        final_result = ""
        if result.returncode == 0:
            if ("unreachable" in str(result.stdout)):
                final_result = "DOWN"
            else:
                final_result = "UP"
        elif result.returncode == 1:
            final_result = "DOWN"
        return (dev_id, final_result)

    # This will perform do_ping() in a multi-threaded process so we aren't waiting for a million years.
    # It will then loop through the original deviceObjList and look for it's original ID and see if the device status matches
    # If the device status matches, I.E. UP == UP or DOWN == DOWN, no change will be made to the object, if it does not match, it will change the status
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for result in executor.map(do_ping, [device.ip_address for device in deviceObjList], [device.dev_id for device in deviceObjList]):
            result_id = result[0]
            result_status = result[1]
            for device in deviceObjList:
                if (result_id == device.dev_id) and (result_status != device.status):
                    device.set_status(result_status)

    # For the grand finale, we will then take the device id, look it up via the API, and post the latest status of a device.
    # It will then check if each device had it's ping status change, if it did, it logs it as an event. Either green or critical.
    for device in deviceObjList:
        patch_url = f'http://127.0.0.1:8000/api/update-status/{device.dev_id}'
        json_payload = {'status':f'{device.status}'}
        head = {'Content-Type':'application/json'}
        patch_request = requests.patch(patch_url, json=json_payload)
        print(patch_request)
        if device.get_change_detected() == "YES":
            custom_severity_level = ""
            if device.status == "DOWN":
                custom_severity_level = "Critical"
            else:
                custom_severity_level = "Green"
            event_post_url = f'http://127.0.0.1:8000/api/event/'
            event_json_payload = {
                'event_type': 'Status change',
                'event_description': f'{device.device_name} is {device.status}',
                'event_severity_level': f'{custom_severity_level}'
            }
            head = {'Content-Type':'application/json'}
            patch_request = requests.post(event_post_url, json=event_json_payload)

    time.sleep(60)