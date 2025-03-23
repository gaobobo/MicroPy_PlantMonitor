# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under the MIT License, see LICENSE in repo's root

"""
**A I2C HAL example**

This is an example as PCF8574 which P4~P7 are DB4~DB7 of the 1602 LCD, P3 is backlight,
P2 is E Pin, P1 is RW Pin, P0 is RS Pin.
"""

from machine import I2C
from .ABC_I2C_HAL import I2C_HAL

class pyb_I2C_HAL(I2C_HAL):

    def _delay(self, cycle: int):
        super()._delay(cycle)

    def __init__(self, i2c:I2C, address:int) -> None:
        super().__init__(i2c, address)
