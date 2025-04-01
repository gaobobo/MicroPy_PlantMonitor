# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under the MIT License, see LICENSE in repo's root

"""
**HAL of GPIO4**

Extend this class to use RS, RW, E, DB4, DB5, DB6, DB7 pins to communicate with HD44780.
"""

from machine import Pin
from time import sleep_us, sleep_ms
from .ABC_Gener_HAL import General_HAL

class GPIO4_HAL(General_HAL):

    # @abstractmethod
    def _init_pin_in(self, pin:Pin) -> None:
        """
        **Init pin to INPUT mode**

        This function used machine.Pin lib. For specific lib like pyb.Pin, override this function.
        :param pin: pin to initialize
        """
        pin.init(mode=Pin.IN)

    # @abstractmethod
    def _init_pin_out(self, pin:Pin) -> None:
        """
        **Init pin to OUTPUT mode**

        This function used machine.Pin lib. For specific lib like pyb.Pin, override this function.
        :param pin: pin to initialize
        """
        pin.init(mode=Pin.OUT)

    # @abstractmethod
    def _write_to_pin(self, pin:Pin, is_high:bool) -> None:
        """
        **Set pin to high or low in OUTPUT mode**

        This function used machine.Pin lib. For specific lib like pyb.Pin, override this function.
        :param pin: pin to set
        :param is_high: false is LOW, true is HIGH
        """
        pin.on() if is_high else pin.off()

    # @abstractmethod
    def _read_from_pin(self, pin:Pin) -> int:
        """
        **Read level from pin in INPUT mode**

        This function used machine.Pin lib. For specific lib like pyb.Pin, override this function.
        :param pin: pin to read
        :return: pin's value
        """
        return pin.value()

    # @abstractmethod
    def _delay(self, cycle:int):
        """
        **Delay time by cycle**

        The HD44780U's typical frequency is 270kHz means about 3.7 microseconds per clock cycle.
        However, the frequency maybe from 190kHZ to 350kHz. Override this function to fit actual frequency.
        :param cycle: Delay cycles
        """

        sleep_us(4 * cycle)

    pins:dict[str, any] = None
    """**A dictionary of RS, RW, E and DB4~DB7** {PinName: PinObject}"""



    def __init__(self, RS, RW, E,
                 DB4, DB5, DB6, DB7) -> None:
        """
        **Constructor of HAL**

        :param RS: Register select pin
        :param RW: Read or write pin. None is GND. If only write, this pin is optional and set it to None.
        :param E: Enable pin
        :param DB4: Data trans pin in 4bit and 8bit mode
        :param DB5: Data trans pin in 4bit and 8bit mode
        :param DB6: Data trans pin in 4bit and 8bit mode
        :param DB7: Data trans pin in 4bit and 8bit mode
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
        **Initialization HD44780 in 4pin mode**

        Inner reset circuit will work if the power conditions correctly, if not sure that always init manually
        before run.
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
                         delay_cycles=10)

        self.write_4bit(RS_level=0,
                         DB7_level=0,
                         DB6_level=0,
                         DB5_level=1,
                         DB4_level=0,
                         delay_cycles=10)

    def write_4bit(self, RS_level:int, DB7_level:int, DB6_level:int, DB5_level:int, DB4_level:int,
                   delay_cycles:int = 10):
        """
        **Write instructions to GPIO**

        :param RS_level: RS pin level. 0 is LOW, otherwise is HIGH
        :param DB7_level: DB7 pin level. 0 is LOW, otherwise is HIGH
        :param DB6_level: DB6 pin level. 0 is LOW, otherwise is HIGH
        :param DB5_level: DB5 pin level. 0 is LOW, otherwise is HIGH
        :param DB4_level: DB4 pin level. 0 is LOW, otherwise is HIGH
        :param delay_cycles: Delay cycles
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


    def write(self, RS_level: int, DBs_level: int, delay_cycles:int = 10):
        """
        **Write instructions to GPIO**

        NOTE: Send 8bit although only 4 bit. To send only once or 4bit, use self.write_4bit().
        :param RS_level: RS pin level. 0 is LOW, otherwise is HIGH
        :param DBs_level: A 8bit int number composed of DB pins' level, from high bit DB7 to low bit DB0.
        :param delay_cycles: Delay cycles
        """

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

    def read_4bit(self, RS_level:int, delay_cycles:int = 10) -> int:
        """
        **Read 4bit data from DB4~DB7**

        :param delay_cycles: Delay cycles
        :param RS_level: RS pin level. 0 is LOW, otherwise is HIGH
        :return: A 4bit int number read. From high bit DB7 to low bit DB4.
        """

        if self.pins['RW'] is None: raise TypeError('RW pin is None but try to read.')

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
        data += self.pins["DB7"].value() << 3
        data += self.pins["DB6"].value() << 2
        data += self.pins["DB5"].value() << 1
        data += self.pins["DB4"].value()

        return data


    def read(self, RS_level:int, delay_cycles:int = 10) -> int:
        """
        **Read data from DB pins**

        NOTE: Read 8bit although only 4 pins. To read only once or 4bit, use self.read_4bit().
        :param RS_level: RS pin level. 0 is LOW, otherwise is HIGH
        :return: A 8bit int number read. From high bit DB7 to low bit DB0
        :param delay_cycles: Delay cycles
        """
        data = 0
        data += self.read_4bit(RS_level, 1) << 4

        data += self.read_4bit(RS_level, delay_cycles)

        return data