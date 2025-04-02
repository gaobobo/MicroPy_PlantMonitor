# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under the MIT License, see LICENSE in repo's root

"""
**A I2C HAL example**

This is an example as PCF8574 which P4~P7 are DB4~DB7 of the 1602 LCD, P3 is backlight,
P2 is E Pin, P1 is RW Pin, P0 is RS Pin.
"""

from machine import I2C
from time import sleep_us
from .ABC_I2C_HAL import I2C_HAL

class pcf8574_I2C_HAL(I2C_HAL):

    def _delay(self, cycle: int):
        super()._delay(cycle)

    def __init__(self, i2c:I2C, address:int) -> None:
        super().__init__(i2c, address)

    def read_4bit_i2c(self, RS_level: int, delay_cycles: int = 10) -> int:

        data = ( 1 << 3                         # 3 bit is Background light
                 # | 0 << 2                     # 2 bit is E Pin
                 | 1 << 1                       # 1 bit is RW Pin
                 | 1 if RS_level else 0         # 0 bit is RS Pin
                 # | 0x00                       # 7~4 bit is DB7, DB6, DB5, DB4
                 )

        self.pins["I2C"].writeto(self.address,
                                 (data | 0x04).to_bytes(1)) # set E pin HIGH

        # I2C Controller will block before finish process, meaning not to need sleep_us() to pulse E
        # pin.
        # sleep_us(1)

        self.pins["I2C"].writeto(self.address,
                                 data.to_bytes(1)) # set E pin LOW

        self._delay(delay_cycles)

        sleep_us(4) # need max 4μs to output from PCF8574

        return (self.pins["I2C"].readfrom(self.address, 1)) >> 4


    def write_4bit_i2c(self, RS_level:int, DBs_level:int, delay_cycles:int = 10, BG_level:int = 1) -> None:

        data = ( ((DBs_level & 0x0F) << 4)        # 7~4 bit is DB7, DB6, DB5, DB4
                 | ((1 << 3) if BG_level else 0)  # 3 bit is Background light
                 # | (0 << 2)                     # 2 bit is E Pin
                 # | (0 << 1)                     # 1 bit is RW Pin
                 | (1 if RS_level else 0)         # 0 bit is RS Pin
                 )

        self.pins["I2C"].writeto(self.address,
                                 (data | 0x04).to_bytes(1)) # set E pin HIGH

        # I2C Controller will block before finish process, meaning not to need sleep_us() to pulse E
        # pin.
        # sleep_us(1)

        self.pins["I2C"].writeto(self.address,
                                 data.to_bytes(1)) # set E pin LOW

        self._delay(delay_cycles)