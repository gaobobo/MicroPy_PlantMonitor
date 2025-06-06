# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under the MIT License, see LICENSE in repo's root

"""
**Apis for 1602 Dot Matrix Display with HD44780**

This program will call HD44780_Drivers' functions. Before using you
need to achieve your own board's Hardware Abstract Layer in ./HAL,
for example see ./HAL/pyb_GPIO4_HAL.py.
"""

from .HD44780_Driver import HD44780_Driver, General_HAL
from framebuf import FrameBuffer

# For only ASCII chars, declare char_set as empty dict
char_set = {}

# For Japanese HD44780, import below
# from .char_sets.japanese import char_set

# For European HD44780, import below
# from .char_sets.european import char_set

# For customized HD44780, fill char_set.custom and import below
# from .char_sets.custom import char_set


class lcd_api:
    """
    **Apis for 1602 Dot Matrix Display with HD44780**

    For operating hardware directly, use lcd_api.board or lcd_api.driver.
    """

    board:General_HAL = None
    driver:HD44780_Driver = None

    _cursor_enable:bool = False
    _cursor_blink:bool = False
    _display_on:bool = True
    _cursor_offset = 0
    _display_offset = 0

    def __init__(self, board:General_HAL) -> None:
        """
        **Constructor of Apis**

        :param board: A General_HAL object. This should be extended from the ABC_*_HAL class.
        Example see ./HAL/pyb_GPIO4_HAL.py.
        """
        self.board = board
        self.board.init_manually()

        self.driver = HD44780_Driver(self.board)
        self.driver.function_set(is_length_8bit= len(self.board.pins) == 11,   # use 8 bit
                                 is_display_2lines=True,
                                 is_font_5x10dot=False)
        self.turn_on_display_or_off(False)
        self.driver.clear_display()
        self.entry_mode_setting(True, False)
        self.driver.display_control(self._display_on, self._cursor_enable, self._cursor_blink)
        self.turn_on_display_or_off(True)


    def turn_on_display_or_off(self, is_on: bool|None=None) -> None:
        """
        **Control display or off**

        NOTICE: This is NOT control background-light. Background-light is independently controlling
        by other pins. If I2C board used, use ABC_I2C_HAL.write_4bit_i2c(**args, BG_level)
        :param is_on: Turn on display or off. True is on and False is off, None is switching between
         on and off.
        """
        self._display_on = not self._display_on if is_on is None else is_on
        self.driver.display_control(self._display_on, self._cursor_enable, self._cursor_blink)

    def enable_cursor_or_disable(self, is_enable: bool|None=None) -> None:
        """
        **Enable cursor or not**
        :param is_enable: Enable cursor or disable. True is enabled and False is disabled. None is
         switching between enable and not disable.
        """
        self._cursor_enable = not self._cursor_enable if is_enable is None else is_enable
        self.driver.display_control(self._display_on, self._cursor_enable, self._cursor_blink)

    def enable_blink_or_disable(self, is_enable: bool|None=None) -> None:
        """
        **Enable blinking cursor or disable**
        :param is_enable:  Enable blink or disable. True is enabled and False is disabled. None is
        switching between enable and disable.
        """
        self._cursor_blink = not self._cursor_blink if is_enable is None else is_enable
        self.driver.display_control(self._display_on, self._cursor_enable, self._cursor_blink)

    def clear(self) -> None:
        """
        **Clear screen**
        NOTE: No need move cursor to home.
        """
        self.driver.clear_display()
        self._cursor_offset = 0
        self._display_offset = 0

    def cursor_to_home(self) -> None:
        """
        **Move cursor to home**
        """
        self.driver.return_home()
        self._cursor_offset = 0
        self._display_offset = 0

    def cursor_move_left(self) -> None:
        """
        **Move cursor one char to the left**
        """
        self.driver.cursor_or_display_shift(True, False)
        self._cursor_offset -= 1 if self._cursor_offset >= 0 else 0


    def cursor_move_right(self, auto_return:bool = False) -> None:
        """
        **Move cursor one char to the right**
        :param auto_return: If move next line when cursor to line end. The end is 16 chars and
        NOT 40 chars. True is enabled and False is disabled.
        """
        self.driver.cursor_or_display_shift(True, True)
        self._cursor_offset += 1 if self._cursor_offset <= 80 else 0
        if auto_return and self._cursor_offset == 16:
            self.cursor_move_to(1, 0)

    def content_move_left(self) -> None:
        """
        **Move content one char to the left**
        NOTICE: Move content will also move cursor's position. For example, move the cursor to home after
        moving content, the cursor won't move to the first char position and it'll offset with the content.
        """
        self.driver.cursor_or_display_shift(False, False)
        self._display_offset -= 1

    def content_move_right(self) -> None:
        """
        **Move content one char to the right**
        """
        self.driver.cursor_or_display_shift(False, True)
        self._display_offset += 1

    def cursor_move_to(self, row:int, col:int) -> None:
        """
        **Move cursor to specific position**
        :param row: Move to which line. Strat from 0. Max is 1
        :param col: Move to which column. Strat from 0. Max is 39.
        """
        if row not in [0, 1] :
            raise IndexError("Row must is 0 or 1.")
        elif col >= 40:
            raise IndexError("every line max 39 chars. First one is 0.")
        else:
            address = 0x40 * row + col

        self.driver.set_dd_ram(address)
        self._cursor_offset = row * 40 + col

    def cursor_return(self) -> None:
        """
        **Move cursor back after writing or reading the CGRAM.
        """
        self.cursor_move_to((self._cursor_offset // 40),
                            self._cursor_offset % 40)


    def cursor_move_up(self) -> None:
        """
        **Move cursor to last line**
        """
        self._cursor_offset -= 40 if self._cursor_offset > 40 else 0
        self.cursor_return()

    def cursor_move_down(self) -> None:
        """
        **Move cursor to next line**
        """
        self._cursor_offset += 40 if self._cursor_offset < 40 else 0
        self.cursor_return()

    def entry_mode_setting(self, cursor_increment:bool, is_scroll_content:bool) -> None:
        """
        **Set cursor and content behavior while typing**
        :param cursor_increment: True is move right after typing and False is left.
        :param is_scroll_content: True is move content after typing and False is not.
        """
        self.driver.entry_mode_set(cursor_increment, is_scroll_content)

    def print_char(self, char:int) -> None:
        """
        **Print char**
        :param char: char's code in ROM.
        """
        self.driver.write_data_to_ram(char)

    def write_custom_char(self, char:FrameBuffer, index:int) -> None:
        """
        **Write custom char to ram**
        :param char: A 5*8 FrameBuffer object of custom char.
        :param index: Index to write to CGRAM, only 8 custom chars supported. Start
        from 0, Max is 7.
        """
        if index not in range(0, 8):
            raise RuntimeError("Index out of range. Index must be between 0 and 7")

        for i in range(0, 8):
            self.driver.set_cg_ram( (index << 3) + i )

            char_single_line = 0
            char_single_line += char.pixel(0, i) << 4
            char_single_line += char.pixel(1, i) << 3
            char_single_line += char.pixel(2, i) << 2
            char_single_line += char.pixel(3, i) << 1
            char_single_line += char.pixel(4, i)

            self.driver.write_data_to_ram(0b000 + char_single_line)

        self.cursor_return()  # set DDRAM address before write


    def print_custom_char(self, index:int, auto_return:bool = False) -> None:
        """
        **Print custom char to ram**
        :param index: Custom char's index in ram. Start from 0, Max is 7.
        :param auto_return: If move next line when cursor to line end. The end is 16 chars and
        NOT 40 chars. True is enabled and False is disabled.
        """
        if index not in range(0, 8):
            raise RuntimeError("Index out of range. Index must be between 0 and 7")

        if auto_return and self._cursor_offset == 16:
            self.cursor_move_to(1, 0)

        self.cursor_return()  # set DDRAM address before write
        self.driver.write_data_to_ram(0b000 + index)
        self._cursor_offset += 1


    def print(self, content:str, auto_return:bool = False) -> None:
        """
        **Print a string**
        :param content: String to be printed.
        :param auto_return: If move next line when cursor to line end. The end is 16 chars and
        NOT 40 chars. True is enabled and False is disabled.
        """
        for char in content:
            if auto_return and self._cursor_offset == 15:
                self.cursor_move_to(1, 0)

            if (0x7D >= ord(char) >= 0x20
                    and ord(char) != 0x5C): # Same as ASCII, exclude /(0x5C) and ~(0x7E)
                self.print_char(ord(char))

            elif char in char_set.keys():
                self.print_char(char_set[char])

            else:
                raise RuntimeError(f"Unknown char: {char}")

            self._cursor_offset += 1


    def is_busy(self) -> bool:
        """
        **Read HD44780's busy status**
        :return: True is busy and False is prepared to receive instruction.
        """
        busy, _ = self.driver.read_busy_flag_and_address()
        return not busy

    def ram_counter(self) -> int:
        """
        **Get address counter's data**
        :return: Data of address counter.
        """
        _, add = self.driver.read_busy_flag_and_address()
        return add

    def ram_data(self) -> int:
        """
        **Get RAM data**
        :return: Data of RAM.
        """
        return self.driver.read_data_from_ram()