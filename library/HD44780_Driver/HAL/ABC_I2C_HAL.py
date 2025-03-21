# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under the MIT License, see LICENSE in repo's root

"""
**Hardware of I2C**

Extend this class to use RS, RW, E, DB0 ~ DB7 to communicate with hardware.
"""

from .ABC_Gener_HAL import General_HAL
from machine import I2C
from time import sleep_us, sleep_ms


class GPIO8_HAL(General_HAL):

    def _delay(self, cycle:int):
        """
        **Delay time by cycle**

        The HD44780U's typical frequency is 270kHz, means about 3.7 microseconds per clock cycle.
        However, the frequency maybe from 190kHZ to 350kHz. Override this function to fit your
        actual frequency if needed.
        :param cycle: Delay cycles
        """

        sleep_us(4 * cycle)

    pins:dict[str, any] = None
    """**I2C object**{"I2C": I2CObject}"""

    address:int = None

    def __init__(self, i2c:I2C, address:int) -> None:
        self.pins = {"I2C": i2c}
        self.address = address


    def init_manually(self):
        """
        **Initialization by instructions in 8pins**

        Inner reset circuit will work if the power conditions correctly,
        but if not that must reset manually by instructions.
        """
        sleep_ms(40)    # wait for more than 40ms after Vcc to 2.7V

        self.write(DBs_level=0b00110000, delay_cycles=0)

        sleep_ms(5)  # wait for more than 4.1ms

        self.write(DBs_level=0b00110000, delay_cycles=0)

        sleep_us(100)  # wait more than 100μs

        self.write(DBs_level=0b00110000, delay_cycles=10)


    def write(self, DBs_level: int, delay_cycles:int = 10, RS_level: int = None):

        if RS_level is None:
            raise RuntimeError('This I2C device only support write to DDRAM.')

        self.pins["I2C"].writeto(self.address, DBs_level)
        self._delay(delay_cycles)

    def read(self, RS_level:int, delay_cycles:int = 10) -> int:
        raise RuntimeError("This I2C device only support write.")