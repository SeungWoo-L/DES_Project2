import asyncio
from pydbus import SessionBus

bus = SessionBus()

class DbusData:
    def __init__(self):
        self._dbus = bus.get("com.example.CanData", "/com/example/CanData/Data")
        self._current_speed = -1
        self._current_rpm = 0
        self._current_battery = 100
        self._current_throttle = 1
        self._current_gear = "OFF"

    def update(self, speed, rpm, battery, gear):
        self._current_speed = speed
        self._current_rpm = rpm
        self._current_battery -= 1
        self._current_throttle -= 0.1
        if(dbus_data._current_speed == 0):
            dbus_data._current_gear = "P"
        elif(dbus_data._current_speed > 0 and dbus_data._current_throttle > -0.038):
            dbus_data._current_gear = "D"
        elif(dbus_data._current_speed > 0 and dbus_data._current_throttle <= -0.038):
            dbus_data._current_gear = "R"
        else:
            dbus_data._current_gear = "OFF"

        print(f"Sending RPM: {self._current_rpm}, Speed: {self._current_speed}, Battery: {self._current_battery}, Throttle: {self._current_throttle}, Gear: {self._current_gear}")
        
        self._dbus.setData(speed, rpm, battery, gear)

async def send_data_incrementally(dbus_data):
    while True:
        # Incrementally increase speed and rpm by 5
        if(dbus_data._current_speed >= 111):
            dbus_data._current_speed = -1

        if(dbus_data._current_battery <= 0):
            dbus_data._current_battery = 100
        
        if(dbus_data._current_throttle <= -1):
            dbus_data._current_throttle = 1

        dbus_data.update(dbus_data._current_speed + 1, dbus_data._current_rpm + 1, 
                         dbus_data._current_battery, dbus_data._current_gear)
        
        # Sleep for a second
        await asyncio.sleep(0.3)

dbus_data = DbusData()

# Start the asyncio main loop
asyncio.run(send_data_incrementally(dbus_data))

