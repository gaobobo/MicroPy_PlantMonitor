from lib.HD44780_Driver.pcf8574_I2C_HAL import pcf8574_I2C_HAL
from lib.HD44780_Driver.lcd_1602_api import lcd_api
from machine import I2C
from framebuf import FrameBuffer, MONO_HLSB
from asyncio import sleep, CancelledError

class lcd_control:

    WIFI_ICON = bytes([
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00100000,
        0b00100000,
        0b00100000
    ])
    
    WIFI_CONNECTED_LOW_ICON = bytes([
        0b00000000,
        0b00000000,
        0b00100000,
        0b01010000,
        0b00000000,
        0b00100000,
        0b00100000,
        0b00100000
    ])
    
    WIFI_CONNECTED_HIGH_ICON = bytes([
        0b01110000,
        0b10001000,
        0b00100000,
        0b01010000,
        0b00000000,
        0b00100000,
        0b00100000,
        0b00100000
    ])
    
    WIFI_DISCONNECT_ICON = bytes([
        0b10001000,
        0b01010000,
        0b00100000,
        0b01010000,
        0b10001000,
        0b00100000,
        0b00100000,
        0b00100000
    ])
    
    UPLOADING_ICON = bytes([
        0b11111000,
        0b00000000,
        0b00100000,
        0b01110000,
        0b10101000,
        0b00100000,
        0b00100000,
        0b00100000
    ])
    
    TEMPERATURE_ICON = bytes([
        0b00000000,
        0b00100000,
        0b00100000,
        0b00100000,
        0b01110000,
        0b11111000,
        0b01110000,
        0b00000000
    ])
    
    CELSIUS_ICON = bytes([
        0b00011000,
        0b00011000,
        0b01100000,
        0b10010000,
        0b10000000,
        0b10010000,
        0b01100000,
        0b00000000
    ])
    
    PRESSURE_ICON = bytes([
        0b00000000,
        0b11111000,
        0b11111000,
        0b00000000,
        0b00100000,
        0b01110000,
        0b11111000,
        0b00000000
    ])
    
    PA_ICON = bytes([
        0b11100000,
        0b10010000,
        0b10010000,
        0b11100000,
        0b10010000,
        0b10101000,
        0b10111000,
        0b10101000
    ])
    
    MOISTURE_ICON = bytes([
        0b00000000,
        0b00100000,
        0b01110000,
        0b11111000,
        0b11111000,
        0b11111000,
        0b01110000,
        0b00000000
    ])
    
    board = None
    api = None
    
    def __init__(self, i2c:I2C, address:int=0x27):
        self.board = pcf8574_I2C_HAL(i2c, address)
        self.api = lcd_api(self.board)
        
        self.api.write_custom_char(FrameBuffer(bytearray(self.WIFI_ICON), 5, 8, MONO_HLSB), 0)
        self.api.write_custom_char(FrameBuffer(bytearray([0, 0, 0, 0, 0, 0, 0, 0]), 5, 8, MONO_HLSB), 1)
        self.api.write_custom_char(FrameBuffer(bytearray(self.TEMPERATURE_ICON), 5, 8, MONO_HLSB), 2)
        self.api.write_custom_char(FrameBuffer(bytearray(self.CELSIUS_ICON), 5, 8, MONO_HLSB), 3)
        self.api.write_custom_char(FrameBuffer(bytearray(self.PRESSURE_ICON), 5, 8, MONO_HLSB), 4)
        self.api.write_custom_char(FrameBuffer(bytearray(self.PA_ICON), 5, 8, MONO_HLSB), 5)
        self.api.write_custom_char(FrameBuffer(bytearray(self.MOISTURE_ICON), 5, 8, MONO_HLSB), 6)

        # | ============================================================================== |
        # | 1   | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
        # | ============================================================================== |
        # | 🌡️ | X  | X  | .  | X  | ℃  |    | ⊤  | X  | X  | X  | X  | Pa |    | ⬆  | 🛜 |
        # | 💧 | X  | X  | .  | X  | %  |    |    |    |    |    |    |    |    |    |    |
        # | ============================================================================== |
        self.api.clear()
        self.api.print_custom_char(2)
        self.api.print("    ")
        self.api.print_custom_char(3)
        self.api.print(" ")
        self.api.print_custom_char(4)
        self.api.print("    ")
        self.api.print_custom_char(5)
        self.api.print(" ")
        self.api.print_custom_char(1)
        self.api.print_custom_char(0)

        self.api.cursor_move_to(1, 0)
        self.api.print_custom_char(6)
        self.api.print("    %")

    async def async_animation_loading(self):
        try:
            self.api.clear()
            self.api.cursor_move_right()
            self.api.cursor_move_right()
            self.api.cursor_move_right()
            self.api.print("Loading")
            while True:
                await sleep(1)
                self.api.print(".")
                await sleep(1)
                self.api.print(".")
                await sleep(1)
                self.api.print(".")
                await sleep(1)
                self.api.cursor_move_left()
                self.api.cursor_move_left()
                self.api.cursor_move_left()
                self.api.print("   ")
                self.api.cursor_move_left()
                self.api.cursor_move_left()
                self.api.cursor_move_left()
        except CancelledError:
            self.api.clear()
    
    
    async def async_animation_wifi_connecting(self):
        try:
            while True:
                self.api.write_custom_char(FrameBuffer(bytearray(self.WIFI_ICON), 5, 8, MONO_HLSB), 0)
                await sleep(0.5)
                self.api.write_custom_char(FrameBuffer(bytearray(self.WIFI_CONNECTED_LOW_ICON), 5, 8, MONO_HLSB), 0)
                await sleep(0.5)
                self.api.write_custom_char(FrameBuffer(bytearray(self.WIFI_CONNECTED_HIGH_ICON), 5, 8, MONO_HLSB), 0)
                await sleep(0.5)
        except CancelledError:
            self.api.write_custom_char(FrameBuffer(bytearray(self.WIFI_ICON), 5, 8, MONO_HLSB), 0)
    
    
    async def async_animation_updating(self):
        try:
            self.api.write_custom_char(FrameBuffer(bytearray(self.UPLOADING_ICON), 5, 8, MONO_HLSB), 1)
            while True:
                for start in range(1, 8):
                    b = bytearray(self.UPLOADING_ICON[0:2])
    
                    for i in range(1, 8):
                        b.append(self.UPLOADING_ICON[j] if (j:=(start + i - 1)) < 8 else 0)
    
                    self.api.write_custom_char(FrameBuffer(b, 5, 8, MONO_HLSB), 1)
                    await sleep(0.5)
        except CancelledError:
            self.api.write_custom_char(FrameBuffer(bytearray([0, 0, 0, 0, 0, 0, 0, 0]), 5, 8, MONO_HLSB), 1)
    
    
        
    def update_temp(self, temp: float):
        self.api.cursor_move_to(0,1)
    
        if temp >= 9999:
            self.api.print("9999")
        elif temp <= -999:
            self.api.print("-999")
        else:
            self.api.print(f"{temp:.1f}    "[0:4])   # add space to clear value when digits not enough
    
    
    def update_pressure(self, pressure: int):
        self.api.cursor_move_to(0,8)
    
        if pressure >= 9999:
            self.api.print("9999")
        elif pressure <= -999:
            self.api.print("-999")
        else:
            self.api.print(f"{pressure}    "[0:4])   # add space to clear value when digits not enough
    
    
    def update_soil_moisture(self, moisture: float):
        self.api.cursor_move_to(1,1)
    
        if moisture >= 1:
            self.api.print("100 ")   # add space to clear value when digits not enough
        else:
            self.api.print(f"{(moisture * 100):.1f}    "[0:4])   # add space to clear value when digits not enough
    
    
    def update_wifi_level(self, level: bool|None):
        """
        :param level: bool|None
            True: HIGH
            False: LOW
            None: DISCONNECT
        """
        if level is None:
            self.api.write_custom_char(FrameBuffer(bytearray(self.WIFI_DISCONNECT_ICON), 5, 8, MONO_HLSB), 0)
        elif level:
            self.api.write_custom_char(FrameBuffer(bytearray(self.WIFI_CONNECTED_HIGH_ICON), 5, 8, MONO_HLSB), 0)
        else:
            self.api.write_custom_char(FrameBuffer(bytearray(self.WIFI_CONNECTED_LOW_ICON), 5, 8, MONO_HLSB), 0)