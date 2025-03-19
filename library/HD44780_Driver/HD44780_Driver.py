# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under The MIT License, see LICENSE in repo's root

from .instruction.instruction_const import *
from .HAL.ABC_Gener_HAL import General_HAL

class HD44780_Driver:

    board:General_HAL = None

    def __init__(self, board:General_HAL) -> None:
        """
        :param board: A HAL extend object from General_HAL object.
        """
        self.board = board


    def clear_display(self) -> None:
        """Clear Display Data RAM and set Address Counter to 0."""
        self.board.write(RS_level=0,
                         DBs_level=LCD_CLEAR,
                         delay_cycles=42)   # need 1.52ms in typical frequency

    def return_home(self) -> None:
        """set Address Counter to 0."""
        self.board.write(RS_level=0,
                         DBs_level=LCD_TO_HOME,
                         delay_cycles=42)    # need 1.52ms in typical frequency

    def entry_mode_set(self, cursor_increment:bool = True, display_shift:bool = False) -> None:
        """Control action when read or write.
        :param cursor_increment: True is move cursor from left to right when read or write, false is not move.
        :param display_shift: True is enabled scroll content(stay the cursor's position), false is disabled.
        """
        instruction = (LCD_ENTRY_MODE_
                       + (LCD_ENTRY_MODE_CURSOR_INCREMENT
                           if cursor_increment
                           else LCD_ENTRY_MODE_CURSOR_DECREMENT)
                       + (LCD_ENTRY_MODE_SHIFT if display_shift else 0)
                       )

        self.board.write(RS_level=0,
                         DBs_level= instruction)

    def display_control(self, display_on:bool=True, cursor_on=True, cursor_blink:bool=True) -> None:
        """Control display on or off and cursor display.
        :param display_on: True is turn on the display, false is off.
        :param cursor_on: True is enabled cursor, false is disabled.
        :param cursor_blink: True is enabled blink for cursor, false is disabled."""
        instruction = (LCD_DISPLAY_
                       + (LCD_DISPLAY_ON
                          if display_on
                          else LCD_DISPLAY_OFF)
                       + (LCD_DISPLAY_CURSOR_ON
                          if cursor_on
                          else LCD_DISPLAY_CURSOR_OFF)
                       + (LCD_DISPLAY_BLINK if cursor_blink else 0)
                       )

        self.board.write(RS_level=0,
                         DBs_level= instruction)

    def cursor_or_display_shift(self, move_cursor:bool, move_right:bool) -> None:
        """Move cursor right but keep Display Data RAM.
        :param move_cursor: True is move cursor, False is move display content.
        :param move_right: True is move right, False is left."""
        instruction = (LCD_SHIFT_
                       + (LCD_SHIFT_CURSOR
                          if move_cursor
                          else LCD_SHIFT_DISPLAY)
                       + (LCD_SHIFT_RIGHT
                          if move_right
                          else LCD_SHIFT_LEFT)
                       )

        self.board.write(RS_level=0,
                         DBs_level= instruction)

    def function_set(self, is_length_8bit:bool, is_display_2lines:bool, is_font_5x10dot:bool) -> None:
        """
        Init display mode.
        :param is_length_8bit: True is 8bit, False is 4bit.
        :param is_display_2lines: True is 2 lines, False is 1 line. 5x10 dot only support 1 line and will as 1 line.
        :param is_font_5x10dot: True is 5x10 dots font, False is 5x8 dots.
        """
        instruction = (LCD_FUNCTION_
                       + (LCD_FUNCTION_8BIT
                          if is_length_8bit
                          else LCD_FUNCTION_4BIT)
                       + (LCD_FUNCTION_2LINE
                          if is_display_2lines
                          else LCD_FUNCTION_1LINE)
                       + (LCD_FUNCTION_5x10DOT
                          if is_font_5x10dot
                          else LCD_FUNCTION_5x8DOT)
                       )

        self.board.write(RS_level=0,
                         DBs_level= instruction)

    def set_cg_ram(self, address: int) -> None:
        """Sets Address Counter to the Character Generator RAM address.
        :param address: address to set.
        """
        instruction = SET_CGRAM_ADDRESS__ + address
        self.board.write(RS_level=0,
                         DBs_level= instruction)

    def set_dd_ram(self, address: int) -> None:
        """
        **To set address counter SET_DDRAM_ADDRESS or SET_CGRAM_ADDRESS**
        :param address: address to set.
        """
        instruction = SET_DDRAM_ADDRESS__ + address
        self.board.write(RS_level=0,
                         DBs_level= instruction)

    def read_busy_flag_and_address(self) -> (bool, int):
        """
        **Get busy-flag and address counter**
        :return: (busy_flag, address), busy_flag is True means inner operating now and False is
        ready to accept instruction. address is current Address Counter, which is read depending on
        last SET_CGRAM_ADDRESS or SET_DDRAM_ADDRESS ran.
        """
        data = self.board.read(RS_level=0)
        busy_flag = bool(data & 0x80)
        address = data << 1
        return busy_flag, address

    def write_data_to_ram(self, data: int) -> None:
        """
        ** Write to CGRAM or DDRAM. **  Write to witch register is depend on witch Register Address last
        set in WriteToCommandRegister.
        :param data: data to write.
        """
        self.board.write(RS_level=1, DBs_level=data)

    def read_data_from_ram(self) -> int:
        """**Read data from CGRAM or DDRAM.** Read witch register is depend on witch Register Address last
        set in WriteToCommandRegister.
        :return: data read"""
        return self.board.read(RS_level=1)