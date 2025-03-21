# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under the MIT License, see LICENSE in repo's root

class General_HAL :

    pins:dict[str, any]

    def init_manually(self):
        pass

    def write(self, RS_level: int, DBs_level: int, delay_cycles:int = 10):
        pass

    def read(self, RS_level:int, delay_cycles:int = 10) -> int:
        pass
