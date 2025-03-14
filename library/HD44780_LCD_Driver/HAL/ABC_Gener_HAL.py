# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under The MIT License, see LICENSE in repo's root

from abc import ABC, abstractmethod

class General_HAL (ABC):

    @abstractmethod
    def write(self, RS_level: int, DBs_level: int, delay_cycles:int = 1):
        pass

    @abstractmethod
    def read(self, RS_level:int) -> int:
        pass
