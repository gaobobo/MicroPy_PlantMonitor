from time import sleep_ms
from machine import I2C
from struct import unpack

class BMP180Driver:

    OVERSAMPLING_1_TIME = 0
    OVERSAMPLING_2_TIMES = 1
    OVERSAMPLING_4_TIMES = 2
    OVERSAMPLING_8_TIMES = 3

    i2c:I2C = None
    address:int = None

    _AC1:int = 0
    _AC2:int = 0
    _AC3:int = 0
    _AC4:int = 0
    _AC5:int = 0
    _AC6:int = 0
    _B1:int = 0
    _B2:int = 0
    _MB:int = 0
    _MC:int = 0
    _MD:int = 0

    def __init__(self, i2c, address):
        """

        :param i2c:
        :param address:
        """
        self.i2c = i2c
        self.address = address
        self._get_cal_param()


    def _get_cal_param(self):
        raw_data = self.i2c.readfrom_mem(self.address, 0xAA,22) # All reg is neighbour

        # cannot use int.from_bytes(), because micropy doesn't achieve signed argument. Instead of
        # struct.unpack().
        self._AC1 = unpack(">h", raw_data[0:2])[0]
        self._AC2 = unpack(">h", raw_data[2:4])[0]
        self._AC3 = unpack(">h", raw_data[4:6])[0]
        self._AC4 = unpack(">h", raw_data[6:8])[0]
        self._AC5 = unpack(">h", raw_data[8:10])[0]
        self._AC6 = unpack(">h", raw_data[10:12])[0]
        self._B1 = unpack(">h", raw_data[12:14])[0]
        self._B2 = unpack(">h", raw_data[14:16])[0]
        self._MB = unpack(">h", raw_data[16:18])[0]
        self._MC = unpack(">h", raw_data[18:20])[0]
        self._MD = unpack(">h", raw_data[20:22])[0]


    def _read_uncompensated_temp(self) -> int:
        self.i2c.writeto_mem(self.address, 0xF4, (0x2E).to_bytes(1))
        sleep_ms(5) # wait 4.5ms to process

        return unpack(">h", self.i2c.readfrom_mem(self.address, 0xF6, 2))[0]

    def _read_uncompensated_pressure(self, over_sample_setting_flag: int):

        self.i2c.writeto_mem(self.address,
                             0xF4,
                             (0x34 | (over_sample_setting_flag << 6) ).to_bytes(1))

        # |-----|-----------------------|------------------|
        # | oss | Max conversation time | sampling time(s) |
        # |  0  |        4.5ms          |        1         |
        # |  1  |        7.5ms          |        2         |
        # |  2  |       13.5ms          |        4         |
        # |  3  |       25.5ms          |        8         |
        # |-----|-----------------------|------------------|
        sleep_time_ms = [5, 8, 14, 26]
        sleep_ms(sleep_time_ms[over_sample_setting_flag])

        byte_data = self.i2c.readfrom_mem(self.address, 0xF6, 3)

        return unpack(">h", byte_data)[0] >> (8 - over_sample_setting_flag)


    def get_temperature(self):
        UT = self._read_uncompensated_temp()


        X1 = ((UT - self._AC6) * self._AC5) >> 15
        X2 = (self._MC << 11) // (X1 + self._MD)
        T = (X1 + X2 + 8) >> 4
        return T / 10


    def get_pressure(self, oversampling_mode: int):
        UT = self._read_uncompensated_temp()
        UP = self._read_uncompensated_pressure(oversampling_mode)

        # calculate B6
        X1 = ((UT - self._AC6) * self._AC5) >> 15
        X2 = (self._MC << 11) // (X1 + self._MD)
        B6 = X1 + X2 - 4000

        # calculate B3
        X1 = (self._B2 * (B6 * B6) >> 12) >> 11
        X2 = (self._AC2 * B6) >> 11
        B3 = ( ((self._AC1 * 4 + X1 + X2) << oversampling_mode) + 2 ) >> 2

        # calculate B7
        X1 = (self._AC3 * B6) >> 13
        X2 = ( self._B1 * ((B6 * B6) >> 12) ) >> 16
        X3 = ( (X1 + X2) + 2 ) >> 2
        B4 = ( self._AC4 * (X3 + 32768) ) >> 15
        B7 = (UP - B3) * (50000 >> oversampling_mode)

        # calculate p
        if B7 < 0x80000000: p = (B7 << 1) // B4
        else: p = (B7 // B4) << 1

        X1 = ( (p >> 8) * (p >> 8) * 3038 ) >> 16
        X2 = (-7357 * p) >> 16
        return ( p + (X1 + X2 + 3791) ) >> 4


