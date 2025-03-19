# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under The MIT License, see LICENSE in repo's root

from micropython import const

LCD_CLEAR = const(0x01)
LCD_TO_HOME = const(0x02)


LCD_ENTRY_MODE_ = const(0x04)
LCD_ENTRY_MODE_CURSOR_DECREMENT = const(0x00)
LCD_ENTRY_MODE_CURSOR_INCREMENT = const(0x02)
LCD_ENTRY_MODE_SHIFT = const(0x01)


LCD_DISPLAY_ = const(0x08)
LCD_DISPLAY_ON = const(0x04)
LCD_DISPLAY_OFF = const(0x00)
LCD_DISPLAY_CURSOR_ON = const(0x02)
LCD_DISPLAY_CURSOR_OFF = const(0x00)
LCD_DISPLAY_BLINK = const(0x01)


LCD_SHIFT_ = const(0x10)
LCD_SHIFT_CURSOR = const(0x00)
LCD_SHIFT_DISPLAY = const(0x08)
LCD_SHIFT_RIGHT = const(0x04)
LCD_SHIFT_LEFT = const(0x00)


LCD_FUNCTION_ = const(0x20)
LCD_FUNCTION_4BIT = const(0x00)
LCD_FUNCTION_8BIT = const(0x10)
LCD_FUNCTION_1LINE = const(0x00)
LCD_FUNCTION_2LINE = const(0x08)
LCD_FUNCTION_5x8DOT = const(0x00)
LCD_FUNCTION_5x10DOT = const(0x02)


SET_CGRAM_ADDRESS__ = const(0x40)
SET_DDRAM_ADDRESS__ = const(0x80)