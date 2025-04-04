import network_control as network
from network import WLAN, STA_IF
from lib.BMP180_Driver.BMP180_driver import BMP180Driver
from machine import I2C, Pin, ADC, unique_id
import lcd_control as lcd
from asyncio import sleep, run, create_task
from lib.HD44780_Driver.lcd_1602_api import lcd_api
from lib.HD44780_Driver.pcf8574_I2C_HAL import pcf8574_I2C_HAL
from umqtt.simple import MQTTClient
from binascii import hexlify

PASSWORD = "PASSWORD"
SSID = "SSID"
MQTT_BROKER_IP = "192.168.31.194"
MQTT_BROKER_PORT = 1883

api = lcd_api( pcf8574_I2C_HAL(I2C(scl=Pin(14), sda=Pin(2), freq=100000), 0x27) )
wlan = WLAN(STA_IF)


def get_temp_and_pressure() -> (float, int):
    bmp180 = BMP180Driver(I2C(scl=Pin(14), sda=Pin(2), freq=100000), 0x77)

    temperature = bmp180.get_temperature()
    pressure = bmp180.get_pressure(oversampling_mode=0)

    return temperature, pressure


def get_soil_moisture() -> float:
    # soil moisture sensor value need fixed
    offset_min = 150    # min value or in water, larger will be more close to 1
    offset_max = 250    # max value or in air, smaller will be more close to 0

    # raw data 0 is wet and 1 is dry
    result_fixed = 1 - ( (ADC(0).read() - offset_min) / (offset_max - offset_min) )

    # add max value limit
    return 0 if result_fixed <= 0 else 1 if result_fixed >= 1 else result_fixed

def update_data(temperature: float, pressure: int, moisture: float):
    lcd.update_temp(api, temperature)
    lcd.update_pressure(api, pressure)
    lcd.update_soil_moisture(api, moisture)


async def async_try_to_connect():
    animation_task =  create_task(lcd.async_animation_wifi_connecting(api))

    try:
        await network.async_connect(wlan, SSID, PASSWORD, 1)

    finally:
        animation_task.cancel()
        update_wifi_level()


def update_wifi_level():
    level = network.get_level(wlan)

    if level is None:
        lcd.update_wifi_level(api, None)

    elif level == 2:
        lcd.update_wifi_level(api, True)
    else:
        lcd.update_wifi_level(api, False)


async def async_upload_data(temperature: float, pressure: int, moisture: float):
    uploading_animate_task = create_task(lcd.async_animation_updating(api))
    DISCOVER_PAYLOAD = """{
    "dev": {
    "ids": "000000",
    "name": "MicroPython",
    "mf": "MicroPython",
    "mdl": "pyboard",
    "sw": "1.23.0",
    "sn": "000000",
    "hw": "1.0"
  },
  "o": {
    "name":"micropython",
    "sw": "1.0",
    "url": "https://github.com/gaobobo/MicroPy_PlantMonitor"
  },
  "cmps": {
    "temp_pyb": {
      "name": "Temperature/环境温度",
      "p": "sensor",
      "unit_of_measurement":"°C",
      "value_template":"{{ value_json.temperature | round(1) }}",
      "unique_id":"temp_pyb"
    },
    "pressure_pyb": {
      "name": "Pressure/大气压力",
      "p": "sensor",
      "unit_of_measurement":"Pa",
      "value_template":"{{ value_json.pressure }}",
      "unique_id":"pressure_pyb"
    },
    "soil_moisture_pyb": {
      "name": "soil moisture/土壤湿度",
      "p": "sensor",
      "unit_of_measurement":"%",
      "value_template":"{{ (value_json.soil_moisture * 100) | round(1) }}",
      "unique_id":"soil_moisture_pyb"
    }
  },
  "state_topic": "micropy/sensor",
  "qos": 0
}"""

    mqtt = MQTTClient(client_id=hexlify(unique_id()),
                      server=MQTT_BROKER_IP,
                      port=MQTT_BROKER_PORT)

    try:
        mqtt.connect()

        mqtt.publish(f"homeassistant/device/{hexlify(unique_id()).decode()}/config".encode(),
                     DISCOVER_PAYLOAD.encode())

        mqtt.publish("micropy/sensor".encode(),
                     f'{{"temperature":{temperature},"pressure":{pressure},"soil_moisture":{moisture}}}'.encode())

        await sleep(3)  # wait to avoid update too frequency to block the homeassistant IO

    finally:
        uploading_animate_task.cancel()
        mqtt.disconnect()



async def main():

    async def dummy_task() : await sleep(0)

    lcd.init_ui(api)

    network_connect_task = create_task(async_try_to_connect())
    upload_data_task = create_task(dummy_task())  # Create a dummy task to avoid error

    while True:
        temperature, pressure = get_temp_and_pressure()
        moisture = get_soil_moisture()
        update_data(temperature, pressure, moisture)

        if wlan.isconnected():
            update_wifi_level()
            if upload_data_task.done(): # if last uploading not finishing, continue.
                upload_data_task = create_task(async_upload_data(temperature, pressure, moisture))

        elif network_connect_task.done():   # new next connect task when the last connect task is done
            network_connect_task = create_task(async_try_to_connect())

        await sleep(10)


run(main())