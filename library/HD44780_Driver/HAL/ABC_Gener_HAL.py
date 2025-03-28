# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under the MIT License, see LICENSE in repo's root

"""
**Base class of HAL**

Should extend from ABC_GPIO4_HAL, ABC_GPIO8_HAL and ABC_I2C_HAL, unless need another bus protocol.
"""

class General_HAL :

    pins:dict[str, any]

    def init_manually(self):
        pass

    def write(self, RS_level: int, DBs_level: int, delay_cycles:int = 10):
        pass

    def read(self, RS_level:int, delay_cycles:int = 10) -> int:
        pass
