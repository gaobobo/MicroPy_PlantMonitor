# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under The MIT License, see LICENSE in repo's root



"""
**The HD44780's Instruction Set**

Only contain what data to send to or receive from IO pins, not how to send or receive.

For more info see "`Hitachi HD44780 LCD controller <https://en.wikipedia.org/wiki/Hitachi_HD44780_LCD_controller>`_".
"""



class WriteToCommandRegister:
    """
    **Write to IR or Instrction Register**

    Start with "_" is inner member and **add(+)** them to get command, like::

        class cmd(WriteToCommandRegister):
            def __init__(self):
                print(bin(
                        self._LCD_DISPLAY_ON
                      + self._LCD_DISPLAY_CURSOR_ON
                      + self._LCD_DISPLAY_CURSOR_BLINK))

    Output is:

        >>> cmd()
        0b1111
        >>> print(bin(WriteToCommandRegister().LCD_DISPLAY_ON_CURSOR_ON_BLINK))
        0b1111
    """

    # ====================RS and RW Pin=======================

    RS = 0
    """**RS Pin.** Register select, 0 is command and 1 is data. """

    RW = 0
    """**RW Pin.** Read or write, 0 is write and 1 is read. Mostly we only write in, 
    so RW Pin connecting to ground is common."""

    # ===================Basic Command========================

    LCD_CLEAR = 0x01
    """Clear Display Data RAM and set Address Counter to 0.
    
    **Note:** Clear display needs 1.52 ms to run."""


    LCD_CURSOR_TO_HOME = 0x02
    """set Address Counter to 0.
    
    **Note:** Move cursor to home needs 1.52ms"""

    # ====================Type Mode============================

    LCD_ENTRY_MODE_CURSOR_MOVE_RIGHT = 0x06
    """Move cursor from left to right when read or write."""
    LCD_ENTRY_MODE_CURSOR_MOVE_LEFT = 0x04
    """Move cursor from right to left when read or write."""
    LCD_ENTRY_MODE_CURSOR_MOVE_RIGHT_SHIFT = 0x07
    """Move cursor from left to right when read or write and scroll content(stay the cursor's position)."""
    LCD_ENTRY_MODE_CURSOR_MOVE_LEFT_SHIFT = 0x05
    """Move cursor from right to left when read or write and scroll content(stay the cursor's position)."""

    _LCD_ENTRY_MODE_CURSOR_MOVE_LEFT = 0x04
    """Move cursor(type char) from left to right when read or write."""
    _LCD_ENTRY_MODE_CURSOR_MOVE_RIGHT = 0x06
    """Move cursor(type char) from right to left when read or write."""
    _LCD_ENTRY_MODE_SHIFT = 0x01
    """Enable scroll content(stay the cursor's position)"""

    # =================Display Settings========================

    LCD_DISPLAY_ON_CURSOR_ON = 0x0E
    """Turn display on and show cursor."""
    LCD_DISPLAY_ON_CURSOR_ON_BLINK = 0x0F
    """Turn display on and show blink cursor."""

    LCD_DISPLAY_ON_CURSOR_OFF = 0x0C
    """Turn display on and hide cursor."""
    # LCD_DISPLAY_ON_CURSOR_OFF_BLINK = 0x0D
    """Turn display on and hide cursor. "_BLINK" is unmeaning, just default when bit operate."""

    # LCD_DISPLAY_OFF_CURSOR_ON = 0x0A
    """Turn display off. "_CURSOR_ON" is unmeaning, just default bit operate."""
    # LCD_DISPLAY_OFF_CURSOR_ON_BLINK = 0x0B
    """Turn display off. "_CURSOR_ON" and "_BLINK" are unmeaning, just default bit operate."""

    LCD_DISPLAY_OFF_CURSOR_OFF = 0x08
    """Turn display off. "_CURSOR_OFF" is unmeaning, just default bit operate."""
    # LCD_DISPLAY_OFF_CURSOR_OFF_BLINK = 0x09
    """Turn display off. "_CURSOR_OFF" and "_BLINK" are unmeaning, just default bit operate."""

    _LCD_DISPLAY_ON = 0x0C
    """Turn display on."""
    _LCD_DISPLAY_OFF = 0x08
    """Turn display off. """
    _LCD_DISPLAY_CURSOR_ON = 0x02
    """ Show cursor."""
    _LCD_DISPLAY_CURSOR_OFF = 0x00
    """Hide cursor."""
    _LCD_DISPLAY_CURSOR_BLINK = 0x01
    """Enable blink cursor."""

    # ==============Cursor and Content Move===================

    LCD_SHIFT_CURSOR_MOVE_RIGHT = 0x14
    """Move cursor right but keep Display Data RAM."""
    LCD_SHIFT_CURSOR_MOVE_LEFT = 0x10
    """Move cursor left but keep Display Data RAM."""
    LCD_SHIFT_DISPLAY_MOVE_RIGHT = 0x1C
    """Move cursor and content right but keep Display Data RAM."""
    LCD_SHIFT_DISPLAY_MOVE_LEFT = 0x18
    """Move cursor and content left but keep Display Data RAM."""

    _LCD_SHIFT_CURSOR_ = 0x10
    """Move cursor but keep Display Data RAM."""
    _LCD_SHIFT_DISPLAY_ = 0x18
    """Move content but keep Display Data RAM."""
    _LCD_SHIFT_MOVE_LEFT = 0x04
    """Move left."""
    _LCD_SHIFT_MOVE_RIGHT = 0x00
    """Move right."""

    # ===================Basic Settings========================

    LCD_FUNCTION_4bit_1line_5x8dot = 0x20
    """Set 4bit interface(D4, D5, D6, D7), display is 1 line and 5x8 dots."""
    LCD_FUNCTION_4bit_1line_5x10dot = 0x24
    """Set 4bit interface(D4, D5, D6, D7), display is 1 line and 5x10 dots."""

    LCD_FUNCTION_4bit_2line_5x8dot = 0x28
    """Set 4bit interface(D4, D5, D6, D7), display is 2 lines and 5x8 dots."""
    # LCD_FUNCTION_4bit_2line_5x10dot = 0x2C
    """Set 4bit interface(D4, D5, D6, D7), 2 lines unsupported 5x10 dots and will ignore "_2line"."""

    LCD_FUNCTION_8bit_1line_5x8dot = 0x30
    """Set 8bit interface(D0 ~ D7), display is 1 line and 5x8 dots."""
    LCD_FUNCTION_8bit_1line_5x10dot = 0x34
    """Set 8bit interface(D0 ~ D7), display is 1 line and 5x10 dots."""

    LCD_FUNCTION_8bit_2line_5x8dot = 0x38
    """Set 8bit interface(D0 ~ D7), display is 2 lines and 5x8 dots."""
    # LCD_FUNCTION_8bitc_5x10dot = 0x3C
    """Set 8bit interface(D0 ~ D7), 2 lines unsupported 5x10 dots and will ignore "_2line"."""

    _LCD_FUNCTION_4bit = 0x20
    """4bit interface(D4, D5, D6, D7)"""
    _LCD_FUNCTION_8bit = 0x48
    """8bit interface(D0, D1, D2, D3, D4, D5, D6, D7)"""
    _LCD_FUNCTION_1line = 0x00
    """1 line display."""
    _LCD_FUNCTION_2line = 0x08
    """2 line display. **Unsupported 5x10 dots and ignore when 5x10 dots.**"""
    _LCD_FUNCTION_5x8dot = 0x00
    """5x8 dots display."""
    _LCD_FUNCTION_5x10dot = 0x02
    """5x10 dots display."""

    # ===================Data Write========================

    SET_CGRAM_ADDRESS = 0x40
    """Sets Address Counter to the Character Generator RAM address. Default is head or 0x00. 
    
    **Note:** D0, D1 are unchanged, the address is only start from D2. """


    SET_DDRAM_ADDRESS = 0x80
    """Sets Address Counter to the Display Data RAM start address. Default is head or 0x00.
    
    **Note:** D0 is unchanged, the address is only start from D1. """



    def __init__(self, CGRAM_ADDRESS_offset: int = 0, DDRAM_ADDRESS_offset: int = 0):
        """
        **To offset SET_DDRAM_ADDRESS and SET_CGRAM_ADDRESS**

        Not return any, use SET_CGRAM_ADDRESS or SET_DDRAM_ADDRESS to get actual command.
        :param CGRAM_ADDRESS_offset: Character generator RAM start address. Default is head or 0x00.
        :param CGRAM_ADDRESS_offset: Display data RAM start address. Default is head or 0x00.
        """
        self.SET_CGRAM_ADDRESS += CGRAM_ADDRESS_offset
        self.SET_DDRAM_ADDRESS += DDRAM_ADDRESS_offset




class ReadFromCommandRegister:
    """
    **Get busy-flag and address counter**

    The HD44780U's typical frequency is 270kHz, means about 37 microseconds per clock cycle.
    However, the frequency maybe from 190kHZ to 350KHz.

    Most commands only need 1 clock cycle or 37 μs, exclude:

    - wait more than 15ms to raise voltage if Vcc in not enough, then you need set entry mode 3 times:

        - first, entry mode set since launch needs more than 4.1 ms
        - second, entry mode set since launch needs more than 100 μs
        - third entry mode

    - clear display needs 1.52 ms
    - move cursor to home needs 1.52ms
    - read busy-flag and address counter needs 0μs
    """


    RS = 0
    """**RS Pin.** Register select, 0 is command and 1 is data. """

    RW = 1
    """**RW Pin.** Read or write, 0 is write and 1 is read. Mostly we only write in, 
    so RW Pin connecting to ground is common."""



    data: int = None
    """Received raw data from pins."""
    busy_flag: int = None
    """**Read BF.** 0 is ready to receive command, 1 is internally operating now."""
    address: int = None
    """Address Counter's data."""



    def __init__(self, data:int):
        self.data = data
        self.busy_flag = data >> 6
        self.address = data ^ (self.busy_flag << 6)



class WriteToDataRegister:
    """
    ** Write to CGRAM or DDRAM. **  Write to witch register is depend on witch Register Address last
    set in WriteToCommandRegister.
    """


    RS = 1
    """**RS Pin.** Register select, 0 is command and 1 is data. """

    RW = 0
    """**RW Pin.** Read or write, 0 is write and 1 is read. Mostly we only write in, 
    so RW Pin connecting to ground is common."""

    data: int = None
    """Data to write."""


    def __init__(self, data:int):
        self.data = data



class ReadFromDataRegister:
    """
    **Read data from CGRAM or DDRAM.** Read witch register is depend on witch Register Address last
    set in WriteToCommandRegister.

    **Notice:** Only after reading or writing, the Address Counter has been updated. So read twice and
    use the second result.
    """


    RS = 1
    """**RS Pin.** Register select, 0 is command and 1 is data. """

    RW = 1
    """**RW Pin.** Read or write, 0 is write and 1 is read. Mostly we only write in, 
    so RW Pin connecting to ground is common."""

    data: int = None
    """Data from CGRAM or DDRAM."""

    def __init__(self, data:int):
        self.data = data