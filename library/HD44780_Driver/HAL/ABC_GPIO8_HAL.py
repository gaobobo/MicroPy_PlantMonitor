# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under the MIT License, see LICENSE in repo's root

"""
**Hardware of GPIO4**

Extend this class to use RS, RW, E, DB0 ~ DB7 to communicate with hardware.
"""

from .ABC_Gener_HAL import General_HAL
from time import sleep_us, sleep_ms

class GPIO8_HAL(General_HAL):
    #TODO: complete 8pins HAL. Ref 4pins.
    # must at least below func.

    def __init__(self, RS:int, RW:int,
                   DB0:int, DB1:int, DB2:int, DB3:int,
                   DB4:int, DB5:int, DB6:int, DB7:int):
        pass

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
        pass


    def read_8bit(self, RS_level:int) -> int:
        pass

    def read(self, RS_level:int) -> int:
        pass
