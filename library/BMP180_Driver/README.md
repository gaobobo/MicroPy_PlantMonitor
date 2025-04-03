# BMP180_Driver

An MicroPython BMP180 Sensor driver.

BMP180 must use I²C BUS to communicate and must read calibration data to fix raw data.For how to read accurate data, 
refer to the [BMP180 Datasheet](https://cdn-shop.adafruit.com/datasheets/BST-BMP180-DS000-09.pdf).

## How to use

Construct an `machine.I2C` object and create an `BMP180Driver` object. Then use `BMP180Driver.get_temperature() `
or `BMP180Driver.get_pressure()` to get data. All data is fixed and accurate.

Example see at [`main.py` in MicroPy_PlantMonitor](https://github.com/gaobobo/MicroPy_PlantMonitor/blob/master/program/main.py#L21).