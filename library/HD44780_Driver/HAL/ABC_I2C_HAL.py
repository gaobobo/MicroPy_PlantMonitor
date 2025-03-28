# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under the MIT License, see LICENSE in repo's root

"""
**Hardware of I2C**

Extend this class to use I2C to communicate with hardware.
"""

from .ABC_Gener_HAL import General_HAL
from machine import I2C
from time import sleep_us, sleep_ms


class I2C_HAL(General_HAL):

    # @abstractmethod
    def _delay(self, cycle:int) -> None:
        """
        **Delay time by cycle**

        The HD44780U's typical frequency is 270kHz means about 3.7 microseconds per clock cycle.
        However, the frequency maybe from 190kHZ to 350kHz. Override this function to fit actual frequency.
        :param cycle: Delay cycles
        """

        sleep_us(4 * cycle)

    pins:dict[str, any] = None
    """**I2C object in a dictionary**{"I2C": I2CObject}"""

    address:int = None

    def __init__(self, i2c:I2C, address:int) -> None:
        self.pins = {"I2C": i2c}
        self.address = address
        self.pins['I2C'].writeto(self.address, (0x08).to_bytes(1))


    def init_manually(self) -> None:
        """
        **Initialization HD44780 in 4pin mode**

        Inner reset circuit will work if the power conditions correctly, if not sure that always init manually
        before run.
        """
        sleep_ms(40)  # wait more than 40ms after Vcc to 2.7V

        self.write_4bit_i2c(RS_level=0, DBs_level=0b0011, delay_cycles=0)

        sleep_ms(5)  # wait more than 4.1ms

        self.write_4bit_i2c(RS_level=0, DBs_level=0b0011, delay_cycles=0)

        sleep_us(100)  # wait more than 100μs

        self.write_4bit_i2c(RS_level=0, DBs_level=0b0011, delay_cycles=10)

        self.write_4bit_i2c(RS_level=0, DBs_level=0b0010, delay_cycles=10)


    def write_4bit_i2c(self, RS_level:int, DBs_level:int, delay_cycles:int = 10, BG_level:int = 1) -> None:
        """
        **Write instructions to GPIO**

        NOTE: Every I2C board may have difference of pin defined. Reference to factory's information.
        This func is an example as PCF8574 which P4~P7 are DB4~DB7 of the 1602 LCD, P3 is backlight,
        P2 is E Pin, P1 is RW Pin, P0 is RS Pin.
        :param RS_level: RS pin level. 0 is LOW, otherwise is HIGH
        :param DBs_level: DB Pins level. From high bit DB7 to low bit DB0.
        :param delay_cycles: Delay cycles
        :param BG_level: Background control. 0 is close, otherwise is on
        """

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


    def write(self, RS_level: int, DBs_level: int, delay_cycles:int = 10 ):
        """
        **Write instructions to I2C**

        NOTE: Send 8bit although only 4 bit. To send only once or 4bit, use self.write_4bit_i2c().
        :param RS_level: RS pin level. 0 is LOW, otherwise is HIGH
        :param DBs_level: A 8bit int number composed of DB pins' level, from high bit DB7 to low bit DB0.
        :param delay_cycles: Delay cycles
        """

        self.write_4bit_i2c(RS_level, DBs_level >> 4, 10)
        self.write_4bit_i2c(RS_level, DBs_level & 0x0F, delay_cycles)

    def read_4bit_i2c(self, RS_level: int, delay_cycles: int = 10) -> int:
        """
        **Read 4bit data from DB4~DB7**

        NOTE: Every I2C board may have difference of pin defined. Reference to factory's information.
        This func is an example as PCF8574 which P4~P7 are DB4~DB7 of the 1602 LCD, P3 is backlight,
        P2 is E Pin, P1 is RW Pin, P0 is RS Pin.
        :param delay_cycles: Delay cycles
        :param RS_level: RS pin level. 0 is LOW, otherwise is HIGH
        :return: A 4bit int number read. From high bit DB7 to low bit DB4.
        """

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


    def read(self, RS_level:int, delay_cycles:int = 10) -> int:
        """
        **Read data from DB pins**

        NOTE: Read 8bit although only 4 pins. To read only once or 4bit, use self.read_4bit().
        :param RS_level: RS pin level. 0 is LOW, otherwise is HIGH
        :return: A 8bit int number read. From high bit DB7 to low bit DB0
        :param delay_cycles: Delay cycles
        """
        data = 0
        data += self.read_4bit_i2c(RS_level, 1) << 4

        data += self.read_4bit_i2c(RS_level, delay_cycles)

        return data