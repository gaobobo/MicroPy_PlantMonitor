# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under the MIT License, see LICENSE in repo's root

"""
**A HD44780 8pin example of pyboard**

This HAL use pyb native lib like pyb.Pin.
"""

from pyb import Pin
from .ABC_GPIO8_HAL import GPIO8_HAL

class pyb_GPIO8_HAL(GPIO8_HAL):

    def _init_pin_in(self, pin: Pin):
        pin.init(mode=Pin.IN)

    def _init_pin_out(self, pin: Pin):
        pin.init(mode=Pin.OUT_PP)

    def _write_to_pin(self, pin: Pin, is_high: bool):
        pin.high() if is_high else pin.low()

    def _read_from_pin(self, pin: Pin) -> int:
        return pin.value()

    def _delay(self, cycle: int):
        super()._delay(cycle)

    def __init__(self, RS:Pin, RW:Pin|None, E:Pin,
                 DB0:Pin, DB1:Pin, DB2:Pin, DB3:Pin,
                 DB4:Pin, DB5:Pin, DB6:Pin, DB7:Pin):
        super().__init__(RS, RW, E, DB0, DB1, DB2, DB3, DB4, DB5, DB6, DB7)
