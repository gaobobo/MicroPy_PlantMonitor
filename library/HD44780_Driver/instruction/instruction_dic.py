# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under the MIT License, see LICENSE in repo's root

"""
**A instruction list of HD44780**


All instruction is pre-calculate and just use like

    >>> HD44780_Instruction['LCD_ENTRY_MODE_CURSOR_INCREMENT']
    0x06

"""

HD44780_Instruction = {
    'WriteToCmdReg': {
        """Write to IR or Instruction Register"""
        
        "RS": 0,
        "RW": 0,
        
        "LCD_CLEAR": 0x01,
        "LCD_TO_HOME": 0x02,

        "LCD_ENTRY_MODE_CURSOR_INCREMENT": 0x06,
        "LCD_ENTRY_MODE_CURSOR_DECREMENT": 0x04,
        "LCD_ENTRY_MODE_CURSOR_INCREMENT_SHIFT": 0x07,
        "LCD_ENTRY_MODE_CURSOR_DECREMENT_SHIFT": 0x05,


        "LCD_DISPLAY_ON_CURSOR_ON": 0x0E,
        "LCD_DISPLAY_ON_CURSOR_ON_BLINK": 0x0F,
        "LCD_DISPLAY_ON_CURSOR_OFF": 0x0C,
        # "LCD_DISPLAY_ON_CURSOR_OFF_BLINK": 0x0D,
        # "LCD_DISPLAY_OFF_CURSOR_ON": 0x0A,
        # "LCD_DISPLAY_OFF_CURSOR_ON_BLINK": 0x0B,
        "LCD_DISPLAY_OFF_CURSOR_OFF": 0x08,
        # LCD_DISPLAY_OFF_CURSOR_OFF_BLINK = 0x09


        "LCD_SHIFT_CURSOR_SHIFT_RIGHT": 0x14,
        "LCD_SHIFT_CURSOR_SHIFT_LEFT": 0x10,
        "LCD_SHIFT_DISPLAY_SHIFT_RIGHT": 0x1C,
        "LCD_SHIFT_DISPLAY_SHIFT_LEFT": 0x18,


        "LCD_FUNCTION_4BIT_1LINE_5x8DOT": 0x20,
        "LCD_FUNCTION_4BIT_1LINE_5x10DOT": 0x24,

        "LCD_FUNCTION_4BIT_2LINE_5x8DOT": 0x28,
        # "LCD_FUNCTION_4BIT_2LINE_5x10DOT": 0x2C,

        "LCD_FUNCTION_8BIT_1LINE_5x8DOT": 0x30,
        "LCD_FUNCTION_8BIT_1LINE_5x10DOT": 0x34,

        "LCD_FUNCTION_8BIT_2LINE_5x8DOT": 0x38,
        # "LCD_FUNCTION_8BIT_2LINE_5x10DOT": 0x3C,


        "SET_CGRAM_ADDRESS_": 0x40,
        "SET_DDRAM_ADDRESS_": 0x80,
    },

    "ReadFromCmdReg": {
        "RS": 0,
        "RW": 1,
    },

    "WriteToDataReg": {
        "RS": 1,
        "RW": 0,
    },

    "ReadFromDataReg": {
        "RS": 1,
        "RW": 1,
    }
}
