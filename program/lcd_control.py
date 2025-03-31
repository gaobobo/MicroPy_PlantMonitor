import asyncio

from lib.HD44780_Driver.pcf8574_I2C_HAL import pcf8574_I2C_HAL
from lib.HD44780_Driver.lcd_1602_api import lcd_api
from machine import I2C, Pin
from asyncio import sleep
from framebuf import FrameBuffer, MONO_HLSB

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

board = pcf8574_I2C_HAL(I2C(scl=Pin(14), sda=Pin(2), freq=100000), 0x27)
api = lcd_api(board)

async def async_animation_loading():
    try:
        api.clear()
        api.cursor_move_right()
        api.cursor_move_right()
        api.cursor_move_right()
        api.print("Loading")
        while True:
            await sleep(1)
            api.print(".")
            await sleep(1)
            api.print(".")
            await sleep(1)
            api.print(".")
            await sleep(1)
            api.cursor_move_left()
            api.cursor_move_left()
            api.cursor_move_left()
            api.print("   ")
            api.cursor_move_left()
            api.cursor_move_left()
            api.cursor_move_left()
    except asyncio.CancelledError:
        api.clear()


async def async_animation_wifi_connecting():
    try:
        while True:
            api.write_custom_char(FrameBuffer(bytearray(WIFI_ICON), 5, 8, MONO_HLSB), 0)
            await sleep(0.5)
            api.write_custom_char(FrameBuffer(bytearray(WIFI_CONNECTED_LOW_ICON), 5, 8, MONO_HLSB), 0)
            await sleep(0.5)
            api.write_custom_char(FrameBuffer(bytearray(WIFI_CONNECTED_HIGH_ICON), 5, 8, MONO_HLSB), 0)
            await sleep(0.5)
    except asyncio.CancelledError:
        api.write_custom_char(FrameBuffer(bytearray(WIFI_ICON), 5, 8, MONO_HLSB), 0)


async def async_animation_updating():
    try:
        api.write_custom_char(FrameBuffer(bytearray(UPLOADING_ICON), 5, 8, MONO_HLSB), 1)
        while True:
            for start in range(1, 8):
                b = bytearray(UPLOADING_ICON[0:2])

                for i in range(1, 8):
                    b.append(UPLOADING_ICON[j] if (j:=(start + i - 1)) < 8 else 0)

                api.write_custom_char(FrameBuffer(b, 5, 8, MONO_HLSB), 1)
                await sleep(0.5)
    except asyncio.CancelledError:
        api.write_custom_char(FrameBuffer(bytearray([0, 0, 0, 0, 0, 0, 0, 0]), 5, 8, MONO_HLSB), 1)


def init_UI():
    api.write_custom_char(FrameBuffer(bytearray(WIFI_ICON), 5, 8, MONO_HLSB), 0)
    api.write_custom_char(FrameBuffer(bytearray([0, 0, 0, 0, 0, 0, 0, 0]), 5, 8, MONO_HLSB), 1)
    api.write_custom_char(FrameBuffer(bytearray(TEMPERATURE_ICON), 5, 8, MONO_HLSB), 2)
    api.write_custom_char(FrameBuffer(bytearray(CELSIUS_ICON), 5, 8, MONO_HLSB), 3)
    api.write_custom_char(FrameBuffer(bytearray(PRESSURE_ICON), 5, 8, MONO_HLSB), 4)
    api.write_custom_char(FrameBuffer(bytearray(PA_ICON), 5, 8, MONO_HLSB), 5)
    api.write_custom_char(FrameBuffer(bytearray(MOISTURE_ICON), 5, 8, MONO_HLSB), 6)

    # | ============================================================================== |
    # | 1   | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
    # | ============================================================================== |
    # | 🌡️ | X  | X  | .  | X  | ℃  |    | ⊤  | X  | X  | X  | X  | Pa |    | ⬆  | 🛜 |
    # | 💧 | X  | X  | .  | X  | %  |    |    |    |    |    |    |    |    |    |    |
    # | ============================================================================== |
    api.clear()
    api.print_custom_char(2)
    api.print("    ")
    api.print_custom_char(3)
    api.print(" ")
    api.print_custom_char(4)
    api.print("    ")
    api.print_custom_char(5)
    api.print(" ")
    api.print_custom_char(1)
    api.print_custom_char(0)

    api.cursor_move_to(1, 0)
    api.print_custom_char(6)
    api.print("    %")

def update_temp(temp: float):
    api.cursor_move_to(0,1)

    if temp >= 9999:
        api.print("9999")
    elif temp <= -999:
        api.print("-999")
    else:
        api.print(f"{temp:.1f}    "[0:4])   # add space to clear value when digits not enough


def update_pressure(pressure: int):
    api.cursor_move_to(0,8)

    if pressure >= 9999:
        api.print("9999")
    elif pressure <= -999:
        api.print("-999")
    else:
        api.print(f"{pressure}    "[0:4])   # add space to clear value when digits not enough


def update_soil_moisture(moisture: float):
    api.cursor_move_to(1,1)

    if moisture >= 1:
        api.print("100 ")   # add space to clear value when digits not enough
    else:
        api.print(f"{(moisture * 100):.1f}    "[0:4])   # add space to clear value when digits not enough


def update_wifi_level(level: bool|None):
    """
    :param level: bool|None
        True: HIGH
        False: LOW
        None: DISCONNECT
    """
    if level is None:
        api.write_custom_char(FrameBuffer(bytearray(WIFI_DISCONNECT_ICON), 5, 8, MONO_HLSB), 0)
    elif level:
        api.write_custom_char(FrameBuffer(bytearray(WIFI_CONNECTED_HIGH_ICON), 5, 8, MONO_HLSB), 0)
    else:
        api.write_custom_char(FrameBuffer(bytearray(WIFI_CONNECTED_LOW_ICON), 5, 8, MONO_HLSB), 0)