from abc import ABC, abstractmethod
from datetime import datetime, timedelta


# Device Interface
class Device(ABC):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def get_status(self):
        pass

# Concrete Light Device
class Light(Device):
    def __init__(self, device_id):
        self.device_id = device_id
        self.status = 'off'

    def turn_on(self):
        self.status = 'on'

    def turn_off(self):
        self.status = 'off'

    def get_status(self):
        return f"Light {self.device_id} is {self.status}."

# Concrete Thermostat Device
class Thermostat(Device):
    def __init__(self, device_id, temperature):
        self.device_id = device_id
        self.temperature = temperature

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    def get_status(self):
        return f"Thermostat is set to {self.temperature} degrees."

# Concrete Door Lock Device
class DoorLock(Device):
    def __init__(self, device_id):
        self.device_id = device_id
        self.status = 'locked'

    def turn_on(self):
        self.status = 'locked'

    def turn_off(self):
        self.status = 'unlocked'

    def get_status(self):
        return f"Door is {self.status}."

# Device Factory
class DeviceFactory(ABC):
    @abstractmethod
    def create_device(self, device_id):
        pass

# Concrete Device Factory
class ConcreteDeviceFactory(DeviceFactory):
    def create_device(self, device_id, device_type, **kwargs):
        if device_type == 'light':
            return Light(device_id)
        elif device_type == 'thermostat':
            return Thermostat(device_id, kwargs.get('temperature', 70))
        elif device_type == 'door':
            return DoorLock(device_id)
        else:
            raise ValueError(f"Invalid device type: {device_type}")

# Proxy Pattern
class DeviceProxy(Device):
    def __init__(self, device):
        self.device = device

    def turn_on(self):
        print("Accessing device...")
        self.device.turn_on()

    def turn_off(self):
        print("Accessing device...")
        self.device.turn_off()

    def get_status(self):
        print("Accessing device...")
        return self.device.get_status()
    # Ensure that device_id is accessible through the proxy
    @property
    def device_id(self):
        return self.device.device_id if hasattr(self.device, 'device_id') else None

# Observer Pattern
class SmartHomeHub:
    def __init__(self):
        self.devices = []
        self.scheduled_tasks = []
        self.automated_triggers = []

    def add_device(self, device):
        self.devices.append(device)

    def remove_device(self, device):
        self.devices.remove(device)

    def turn_on_device(self, device_id):
        for device in self.devices:
            if device.device_id == device_id:
                device.turn_on()
                break

    def turn_off_device(self, device_id):
        for device in self.devices:
            if device.device_id == device_id:
                device.turn_off()
                break

    def set_schedule(self, device_id, time, command):
        self.scheduled_tasks.append({'device': device_id, 'time': time, 'command': command})

    def add_trigger(self, condition, action):
        self.automated_triggers.append({'condition': condition, 'action': action})
    
    # Dynamically add a device to the system
    def add_dynamic_device(self, device):
        self.devices.append(device)

    # Dynamically remove a device from the system
    def remove_dynamic_device(self, device_id):
        for device in self.devices:
            if device.device_id == device_id:
                self.devices.remove(device)
                break
