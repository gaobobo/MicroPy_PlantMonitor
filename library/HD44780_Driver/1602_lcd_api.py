# Copyright (c) Gao Shibo. All rights reserved.
# Licensed under The MIT License, see LICENSE in repo's root
# Licensed under the MIT License, see LICENSE in repo's root

from .HAL.ABC_Gener_HAL import General_HAL
from .HD44780_Driver import HD44780_Driver
from framebuf import FrameBuffer

# For only ASCII char display(exclude \ and ~), import below and keep char_set.custom empty
from .char_sets.custom import char_set

# For Japanese HD44780, import below
# from .char_sets.japanese import char_set

# For European HD44780, import below
# from .char_sets.european import char_set

# For customized HD44780, fill char_set.custom and import below
# from .char_sets.custom import char_set


class lcd_api:

    board:General_HAL = None
    driver:HD44780_Driver = None

    cursor_enable:bool = False
    cursor_blink:bool = False
    display_on:bool = True
    cursor_offset = 0
    display_offset = 0

    def __init__(self, board:General_HAL) -> None:
        self.board = board
        self.board.init_manually()

        self.driver = HD44780_Driver(self.board)
        self.driver.function_set(is_length_8bit=len(self.board.pins)==11   # use 8 bit
                                                or len(self.board.pins)==2,    #use I2C Bus
                                 is_display_2lines=True,
                                 is_font_5x10dot=False)
        self.driver.display_control(self.display_on, self.cursor_enable, self.cursor_blink)
        self.driver.clear_display()

    def turn_on_display_or_off(self, is_on: bool|None=None) -> None:
        self.display_on = not self.display_on if is_on is None else is_on
        self.driver.display_control(self.display_on, self.cursor_enable, self.cursor_blink )

    def enable_cursor_or_disable(self, is_enable: bool|None=None) -> None:
        self.cursor_enable = not self.cursor_enable if is_enable is None else is_enable
        self.driver.display_control(self.display_on, self.cursor_enable, self.cursor_blink)

    def enable_blink_or_disable(self, is_enable: bool|None=None) -> None:
        self.cursor_blink = not self.cursor_blink if is_enable is None else is_enable
        self.driver.display_control(self.display_on, self.cursor_enable, self.cursor_blink)

    def clear(self) -> None:
        self.driver.clear_display()
        self.cursor_offset = 0
        self.display_offset = 0

    def cursor_to_home(self) -> None:
        self.driver.return_home()
        self.cursor_offset = 0
        self.display_offset = 0

    def cursor_move_left(self) -> None:
        self.driver.cursor_or_display_shift(True, False)
        self.cursor_offset -= 1 if self.cursor_offset >= 0 else 0


    def cursor_move_right(self, auto_return:bool = False) -> None:
        self.driver.cursor_or_display_shift(True, True)
        self.cursor_offset += 1 if self.cursor_offset <= 80 else 0
        if auto_return and self.cursor_offset == 16:
            self.cursor_move_to(1, 0)

    def content_move_left(self) -> None:
        self.driver.cursor_or_display_shift(False, False)
        self.display_offset -= 1

    def content_move_right(self) -> None:
        self.driver.cursor_or_display_shift(False, True)
        self.display_offset += 1

    def cursor_move_to(self, row:int, col:int) -> None:
        if row not in [0, 1] :
            raise RuntimeError("Row must is 0 or 1.")
        elif col >= 40:
            raise RuntimeError("every line max 39 chars. First one is 0.")
        else:
            address = 0x40 * row + col

        self.driver.set_dd_ram(address)
        self.cursor_offset = row * 40 + col

    def cursor_return(self) -> None:
        self.cursor_move_to( (self.cursor_offset // 40),
                            self.cursor_offset % 40 )


    def cursor_move_up(self) -> None:
        self.cursor_offset -= 40 if self.cursor_offset > 40 else 0
        self.cursor_return()

    def cursor_move_down(self) -> None:
        self.cursor_offset += 40 if self.cursor_offset < 40 else 0
        self.cursor_return()

    def entry_mode_setting(self, is_from_to_right:bool, is_scroll_content:bool) -> None:
        self.driver.entry_mode_set(is_from_to_right, is_scroll_content)

    def print_char(self, char:int) -> None:
        self.driver.write_data_to_ram(char)

    def write_custom_char(self, char:FrameBuffer, index:int) -> None:
        if index not in range(0, 8):
            raise RuntimeError("Index out of range. Index must be between 0 and 7")

        for i in range(0, 8):
            self.driver.set_cg_ram(index + i)

            char_single_line = 0
            char_single_line += char.pixel(0, i) << 4
            char_single_line += char.pixel(1, i) << 3
            char_single_line += char.pixel(2, i) << 2
            char_single_line += char.pixel(3, i) << 1
            char_single_line += char.pixel(4, i)

            self.driver.write_data_to_ram(0b000 + char_single_line)

        self.cursor_return()  # set DDRAM address before write


    def print_custom_char(self, index:int, auto_return:bool = False) -> None:
        if index not in range(0, 8):
            raise RuntimeError("Index out of range. Index must be between 0 and 7")

        if auto_return and self.cursor_offset == 16:
            self.cursor_move_to(1, 0)

        self.cursor_return()  # set DDRAM address before write
        self.driver.write_data_to_ram(0b000 + index)
        self.cursor_offset += 1


    def print(self, content:str, auto_return:bool = False) -> None:
        for char in content:
            if auto_return and self.cursor_offset == 15:
                self.cursor_move_to(1, 0)

            if (0x7D >= ord(char) >= 0x20
                    and ord(char) != 0x5C): # Same as ASCII, exclude /(0x5C) and ~(0x7E)
                self.print_char(ord(char))

            elif char in char_set.keys():
                self.print_char(char_set[char])

            else:
                raise RuntimeError(f"Unknown char: {char}")

            self.cursor_offset += 1


    def is_busy(self) -> bool:
        busy,add = self.driver.read_busy_flag_and_address()
        return busy

    def ram_counter(self) -> bool:
        busy, add = self.driver.read_busy_flag_and_address()
        return add

    def ram_data(self) -> int:
        return self.driver.read_data_from_ram()