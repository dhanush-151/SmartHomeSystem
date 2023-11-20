import unittest
from  .src.smart_home_system import SmartHomeHub, ConcreteDeviceFactory, DeviceProxy


class TestSmartHomeSystem(unittest.TestCase):
    def setUp(self):
        self.factory = ConcreteDeviceFactory()
        self.hub = SmartHomeHub()

    def test_turn_on_device(self):
        light = self.factory.create_device(1, 'light')
        self.hub.add_device(DeviceProxy(light))

        self.hub.turn_on_device(1)
        self.assertEqual(light.get_status(), "Light 1 is on.")

    def test_turn_off_device(self):
        thermostat = self.factory.create_device(2, 'thermostat', temperature=70)
        self.hub.add_device(DeviceProxy(thermostat))

        self.hub.turn_off_device(2)
        self.assertEqual(thermostat.get_status(), "Thermostat is set to 70 degrees.")

    def test_set_schedule(self):
        door = self.factory.create_device(3, 'door')
        self.hub.add_device(DeviceProxy(door))

        self.hub.set_schedule(3, "06:00", "Turn On")
        self.assertEqual(self.hub.scheduled_tasks, [{'device': 3, 'time': "06:00", 'command': "Turn On"}])

    def test_add_trigger(self):
        light = self.factory.create_device(1, 'light')
        self.hub.add_device(DeviceProxy(light))

        self.hub.add_trigger("temperature > 75", "turn_off_device(1)")
        self.assertEqual(self.hub.automated_triggers, [{'condition': "temperature > 75", 'action': "turn_off_device(1)"}])

    def test_add_dynamic_device(self):
        new_device = self.factory.create_device(4, 'light')
        self.hub.add_dynamic_device(DeviceProxy(new_device))

        self.assertEqual(len(self.hub.devices), 1)

    def test_remove_dynamic_device(self):
        light = self.factory.create_device(1, 'light')
        self.hub.add_device(DeviceProxy(light))

        self.hub.remove_dynamic_device(1)
        self.assertEqual(len(self.hub.devices), 0)

    def test_dynamic_changes_after_commands(self):
        light = self.factory.create_device(1, 'light')
        thermostat = self.factory.create_device(2, 'thermostat', temperature=70)
        self.hub.add_device(DeviceProxy(light))
        self.hub.add_device(DeviceProxy(thermostat))
    
        self.hub.turn_on_device(1)
        self.hub.set_schedule(2, "06:00", "Turn On")
        self.hub.add_trigger("temperature > 75", "turn_off_device(1)")
    
        new_device = self.factory.create_device(4, 'light')
        self.hub.add_dynamic_device(DeviceProxy(new_device))
        self.hub.remove_dynamic_device(2)
    
        # Ensure the status report includes changes without considering the order
        expected_status = [
            "Light 1 is on.",
            "Light 4 is off."
        ]
    
        status_report = [device.get_status() for device in self.hub.devices]
        for expected in expected_status:
            self.assertIn(expected, status_report)
