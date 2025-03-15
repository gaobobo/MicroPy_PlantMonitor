# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under The MIT License, see LICENSE in repo's root

from pyb import Pin
from .abstract.ABC_GPIO4_HAL import GPIO4_HAL

class pyb_GPIO4_HAL(GPIO4_HAL):

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

    def __init__(self, RS:Pin, RW:Pin|None,
                 E:Pin, DB4:Pin, DB5:Pin, DB6:Pin, DB7:Pin):
        super().__init__(RS, RW, E, DB4, DB5, DB6, DB7)
