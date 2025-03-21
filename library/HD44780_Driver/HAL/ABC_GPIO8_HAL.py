# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under the MIT License, see LICENSE in repo's root

"""
**Hardware of GPIO4**

Extend this class to use RS, RW, E, DB0 ~ DB7 to communicate with hardware.
"""
from machine import Pin
from time import sleep_us, sleep_ms
from .ABC_Gener_HAL import General_HAL
from math import ceil

class GPIO8_HAL(General_HAL):

    def _init_pin_in(self, pin:Pin):
        """
        **Init pin to INPUT mode**

        This function used machine.Pin lib, and you could use super()._init_pin_in() to call.
        For specific lib like pyb.Pin, you must achieve yourself.
        :param pin: pin to initialize
        """
        pin.init(mode=Pin.IN)

    def _init_pin_out(self, pin:Pin):
        """
        **Init pin to OUTPUT mode**

        This function used machine.Pin lib, and you could use super()._init_pin_in() to call.
        For specific lib like pyb.Pin, you must achieve yourself.
        :param pin: pin to initialize
        """
        pin.init(mode=Pin.OUT)

    def _write_to_pin(self, pin:Pin, is_high:bool):
        """
        **Set pin to high or low in OUTPUT mode**

        This function used machine.Pin lib, and you could use super()._init_pin_in() to call.
        For specific lib like pyb.Pin, you must achieve yourself.
        :param pin: pin to set
        :param is_high: false is LOW, true is HIGH
        """
        pin.on() if is_high else pin.off()

    def _read_from_pin(self, pin:Pin) -> int:
        """
        **Read level from pin in INPUT mode**

        This function used machine.Pin lib, and you could use super()._init_pin_in() to call.
        For specific lib like pyb.Pin, you must achieve yourself.
        :param pin: pin to read
        :return: pin's value
        """
        return pin.value()

    def _delay(self, cycle:int):
        """
        **Delay time by cycle**

        The HD44780U's typical frequency is 270kHz, means about 3.7 microseconds per clock cycle.
        However, the frequency maybe from 190kHZ to 350kHz. Override this function to fit your
        actual frequency if needed.
        :param cycle: Delay cycles
        """

        sleep_us(ceil(3.7 * cycle))

    pins:dict[str, any] = None
    """**Pins from RS, RW, E and DB4~DB7** {PinName: PinObject}"""

    def __init__(self, RS, RW, E,
                 DB0, DB1, DB2, DB3, DB4, DB5, DB6, DB7) -> None:

        self.pins = {
            'RS': RS,
            'RW': RW,
            'E': E,
            'DB0': DB0,
            'DB1': DB1,
            'DB2': DB2,
            'DB3': DB3,
            'DB4': DB4,
            'DB5': DB5,
            'DB6': DB6,
            'DB7': DB7
        }

    def init_manually(self) -> None:
        """
        **Initialization by instructions in 8pins**

        Inner reset circuit will work if the power conditions correctly,
        but if not that must reset manually by instructions.
        """
        sleep_ms(40)    # wait for more than 40ms after Vcc to 2.7V

        self.write_8bit(RS_level=0,
                         DB7_level=0,
                         DB6_level=0,
                         DB5_level=1,
                         DB4_level=1,
                         DB3_level=0, DB2_level=0, DB1_level=0, DB0_level=0, #  DB0~DB3 are ignored
                         delay_cycles=0)

        sleep_ms(5)   # wait for more than 4.1ms

        self.write_8bit(RS_level=0,
                         DB7_level=0,
                         DB6_level=0,
                         DB5_level=1,
                         DB4_level=1,
                         DB3_level=0, DB2_level=0, DB1_level=0, DB0_level=0, #  DB0~DB3 are ignored
                         delay_cycles=0)

        sleep_us(100)   # wait more than 100μs

        self.write_8bit(RS_level=0,
                         DB7_level=0,
                         DB6_level=0,
                         DB5_level=1,
                         DB4_level=1,
                         DB3_level=0, DB2_level=0, DB1_level=0, DB0_level=0, #  DB0~DB3 are ignored
                         delay_cycles=1)


    def write_8bit(self, RS_level:int,
                   DB0_level:int, DB1_level:int, DB2_level:int, DB3_level:int,
                   DB4_level:int, DB5_level:int, DB6_level:int, DB7_level:int,
                   delay_cycles:int = 1):
        pass

    def write(self, RS_level: int, DBs_level: int, delay_cycles:int = 1):
        if DBs_level > 0xFF:
            raise RuntimeError('DBs_level > 0xFF. Must be 8bit.')

        self.write_8bit(RS_level=RS_level,
                        DB7_level=DBs_level & 0x80,
                        DB6_level=DBs_level & 0x40,
                        DB5_level=DBs_level & 0x20,
                        DB4_level=DBs_level & 0x10,
                        DB3_level=DBs_level & 0x08,
                        DB2_level=DBs_level & 0x04,
                        DB1_level=DBs_level & 0x02,
                        DB0_level=DBs_level & 0x01,
                        delay_cycles=delay_cycles
                        )



    def read_8bit(self, RS_level:int, delay_cycles:int = 10) -> int:
        if self.pins['RW'] is None: raise RuntimeError('RW pin is None but try to read.')

        self._init_pin_out(self.pins['RS'])
        self._write_to_pin(self.pins['RS'], bool(RS_level))

        self._init_pin_out(self.pins['RW'])
        self._write_to_pin(self.pins['RW'], True)

        self._init_pin_out(self.pins['E'])
        self._write_to_pin(self.pins['E'], False)

        self._init_pin_in(self.pins['DB4'])
        self._init_pin_in(self.pins['DB5'])
        self._init_pin_in(self.pins['DB6'])
        self._init_pin_in(self.pins['DB7'])

        sleep_us(1)  # need 25ns to rise or down
        self._write_to_pin(self.pins['E'], True)
        sleep_us(1)  # Min 450ns time for high level of E pin to be detected
        self._write_to_pin(self.pins['E'], False)

        self._delay(delay_cycles)  # wait finish command

        data = 0
        data += self.pins["DB7"].value() << 7
        data += self.pins["DB6"].value() << 6
        data += self.pins["DB5"].value() << 5
        data += self.pins["DB4"].value() << 4
        data += self.pins["DB3"].value() << 3
        data += self.pins["DB2"].value() << 2
        data += self.pins["DB1"].value() << 1
        data += self.pins["DB0"].value()

        return data


    def read(self, RS_level:int, delay_cycles:int = 10) -> int:

        return self.read_8bit(RS_level, delay_cycles)
