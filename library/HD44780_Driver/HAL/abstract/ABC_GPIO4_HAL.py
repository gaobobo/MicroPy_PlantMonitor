# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under The MIT License, see LICENSE in repo's root

from machine import Pin
from time import sleep_us, sleep_ms
from .ABC_Gener_HAL import General_HAL

class GPIO4_HAL(General_HAL):

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

        The HD44780U's typical frequency is 270kHz, means about 37 microseconds per clock cycle.
        However, the frequency maybe from 190kHZ to 350KHz. Override this function to fit your
        actual frequency if needed.
        :param cycle: Delay cycles
        """

        sleep_us(37 * cycle)

    pins:dict[str, any] = None
    """**Pins from RS, RW, E and DB4~DB7** {PinName: PinObject}"""



    def __init__(self, RS, RW, E, DB4, DB5, DB6, DB7):
        """
        **Init class** Must be called using super().__init__()

        :param RS: Register select pin
        :param RW: Read or write pin. None is GND. If only write, this pin is optional and set it to None.
        :param E: Enable pin mode
        :param DB4: Data trans pin in 4bit and 8bit
        :param DB5: Data trans pin in 4bit and 8bit
        :param DB6: Data trans pin in 4bit and 8bit
        :param DB7: Data trans pin in 4bit and 8bit
        """
        self.pins = {
            'RS': RS,
            'RW': RW,
            'E': E,
            'DB4': DB4,
            'DB5': DB5,
            'DB6': DB6,
            'DB7': DB7
        }

    def init_manually(self) -> None:
        """
        **Initialization by instructions in 4pins**

        Inner reset circuit will work if the power conditions correctly,
        but if not that must reset manually by instructions.
        """
        sleep_ms(40)  # wait more than 40ms after Vcc to 2.7V

        self.write_4bit(RS_level=0,
                         DB7_level=0,
                         DB6_level=0,
                         DB5_level=1,
                         DB4_level=1,
                         delay_cycles=0)

        sleep_ms(5)  # wait more than 4.1ms

        self.write_4bit(RS_level=0,
                         DB7_level=0,
                         DB6_level=0,
                         DB5_level=1,
                         DB4_level=1,
                         delay_cycles=0)

        sleep_us(100)  # wait more than 100μs

        self.write_4bit(RS_level=0,
                         DB7_level=0,
                         DB6_level=0,
                         DB5_level=1,
                         DB4_level=1,
                         delay_cycles=1)

        self.write_4bit(RS_level=0,
                         DB7_level=0,
                         DB6_level=0,
                         DB5_level=1,
                         DB4_level=0,
                         delay_cycles=1)

    def write_4bit(self, RS_level:int, DB7_level:int, DB6_level:int, DB5_level:int, DB4_level:int,
                   delay_cycles:int = 0):
        """
        **Write instructions to GPIO**

        :param delay_cycles: Delay cycles
        :param RS_level: RS pin level. 0 is LOW, otherwise is HIGH
        :param DB7_level: DB7 pin level. 0 is LOW, otherwise is HIGH
        :param DB6_level: DB6 pin level. 0 is LOW, otherwise is HIGH
        :param DB5_level: DB5 pin level. 0 is LOW, otherwise is HIGH
        :param DB4_level: DB4 pin level. 0 is LOW, otherwise is HIGH
        """

        self._init_pin_out(self.pins['RS'])
        self._write_to_pin(self.pins['RS'], bool(RS_level))

        if self.pins['RW'] is not None:
            self._init_pin_out(self.pins['RW'])
            self._write_to_pin(self.pins['RW'], False)

        self._init_pin_out(self.pins['E'])
        self._write_to_pin(self.pins['E'], False)

        self._init_pin_out(self.pins['DB4'])
        self._write_to_pin(self.pins['DB4'], bool(DB4_level))

        self._init_pin_out(self.pins['DB5'])
        self._write_to_pin(self.pins['DB5'], bool(DB5_level))

        self._init_pin_out(self.pins['DB6'])
        self._write_to_pin(self.pins['DB6'], bool(DB6_level))

        self._init_pin_out(self.pins['DB7'])
        self._write_to_pin(self.pins['DB7'], bool(DB7_level))

        sleep_us(1)    # need 25ns to rise or down
        self._write_to_pin(self.pins['E'], True)
        sleep_us(1)    # Min 450ns time for high level to be detected
        self._write_to_pin(self.pins['E'], False)

        self._delay(delay_cycles)   # wait finish command


    def write(self, RS_level: int, DBs_level: int, delay_cycles:int = 1):
        """
        **Write instructions to GPIO**

        Send twice although only 4 bit. To send only once, use self.write_4bit().
        :param RS_level: RS pin level. 0 is LOW, otherwise is HIGH
        :param DBs_level: A 8bit int number composed of DB pins' level, from low bit DB0 to high bit DB7.
        :param delay_cycles: Delay cycles
        """
        if DBs_level > 0xFF:
            raise RuntimeError('DBs_level > 0xFF. Must be 8bit.')

        self.write_4bit(RS_level=RS_level,
                        DB7_level=DBs_level & 0x80,
                        DB6_level=DBs_level & 0x40,
                        DB5_level=DBs_level & 0x20,
                        DB4_level=DBs_level & 0x10,
                        delay_cycles=1
                        )

        self.write_4bit(RS_level=RS_level,
                        DB7_level=DBs_level & 0x08,
                        DB6_level=DBs_level & 0x04,
                        DB5_level=DBs_level & 0x02,
                        DB4_level=DBs_level & 0x01,
                        delay_cycles=delay_cycles
                        )

    def read_4bit(self, RS_level:int, delay_cycles:int = 1) -> int:
        """
        **Read 4bit data from DB4~DB7**

        :param delay_cycles: Delay cycles
        :param RS_level: RS pin level. 0 is LOW, otherwise is HIGH
        :return: A 4bit int number read. From DB4 to DB7.
        """

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
        data += (self._read_from_pin(pin) << (i - 1) for i, (pin) in enumerate(self.pins.values()[3:]))

        return data


    def read(self, RS_level:int) -> int:
        """
        **Read data from DB pins**

        Read twice although only 4 pins. To read only once, use self.read_4bit().
        :param RS_level: RS pin level. 0 is LOW, otherwise is HIGH
        :return: A 8bit int number read. From DB0 to DB7
        """
        data = 0
        data += self.read_4bit(RS_level) << 4

        data += self.read_4bit(RS_level)

        return data