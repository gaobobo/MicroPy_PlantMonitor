from .ABC_Gener_HAL import General_HAL

class GPIO8_HAL(General_HAL):
    #TODO: complete 8pins HAL. Ref 4pins.
    # must at least below func.

    def __init__(self, RS:int, RW:int,
                   DB0:int, DB1:int, DB2:int, DB3:int,
                   DB4:int, DB5:int, DB6:int, DB7:int):
        pass

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
