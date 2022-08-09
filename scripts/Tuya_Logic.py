import colorsys
import pprint
import tinytuya
from scripts.epic_utils import getSettings

pp = pprint.PrettyPrinter(indent=4)

class CloudBulb:
    def __init__(self, id, cloud):
        self.id = id
        
        self.cloud = cloud
        
    
        
        
        
    def weezer(self):
        self.setColor(((24,155,204)))
        
    def switch(self, state: bool):
        commands = {
            'commands': [{
                'code': 'switch_led',
                'value': state
            }]
        }
        
        self._sendCommands(commands)
        
    def setWhite(self):
        commands = {
            'commands': [{
                'code': 'work_mode',
                'value': 'white'
            }]
        }
        
        self._sendCommands(commands)
    
    def reset(self):
        commands = {
            'commands': [
                {
                    'code': 'switch_led',
                    'value': True
                },
                {
                    'code': 'work_mode',
                    'value': 'white'
                },
                {
                    'code': 'bright_value',
                    'value': 255
                },
                {
                    'code': 'temp_value',
                    'value': 255
                }
            ]
        }
        
        self._sendCommands(commands)
    
    def setColor(self, rgb):
        hsv = colorsys.rgb_to_hsv(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
        hsv = (hsv[0] * 360, hsv[1] * 255, hsv[2] * 255)
        
        commands = {
            'commands': [
                {
                    'code': 'work_mode',
                    'value': 'white'
                },
                {
                    'code': 'colour_data',
                    'value': {
                        "h": hsv[0],
                        "s": hsv[1],
                        "v": hsv[2]
                    }
                }
            ]
        }
        
        self._sendCommands(commands)
    
    def _sendCommands(self, commands):
        print("Sending command")
        result = self.cloud.sendcommand(self.id, commands)
        print('Result: ' + str(result))



class DeviceManager:
    def __init__(self):
        
        print("Begin Device Manager setup")
        
        try:
            settings = getSettings()["Tuya"]
        except FileNotFoundError:
            print("Settings.yaml not found")
        
        self.cloud = tinytuya.Cloud(
            apiRegion=settings["apiRegion"],
            apiKey=settings["apiKey"],
            apiSecret=settings["apiSecret"],
            apiDeviceID=settings["apiDeviceID"]
            
        )

        print("Cloud connection established")
        
        self.cDevices = self.cloud.getdevices()
        
        self.devices = {}
        print("Setting up bulb devices")
        for device in self.cDevices:
            self.devices[device['name']] = CloudBulb(id = device['id'], cloud = self.cloud)
        print("Completed device manager setup")
    
    def getDevice(self, name):
        try:
            return self.devices[name]
        except KeyError:
            return None
    
    def listDevices(self):
        for device in self.devices:
            print(device)
            
        return [device for _ in self.devices]
    
    def resetAll(self):
        for device in self.devices.values():
            device.reset()

# tv = CloudBulb('07200423bcddc205e0ef')

# #tv.switch(False)
# #time.sleep(1)
# #tv.switch(True)

# dm = DeviceManager()

# dm.resetAll()
