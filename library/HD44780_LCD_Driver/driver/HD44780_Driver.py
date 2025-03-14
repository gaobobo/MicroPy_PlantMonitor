from dis import Instruction

from HD44780_Instruct import HD44780_instruction_set as instruction_set
from ..HAL.ABC_Gener_HAL import General_HAL
from ..HAL.ABC_GPIO4_HAL import GPIO4_HAL
from ..HAL.ABC_GPIO8_HAL import GPIO8_HAL
from time import sleep_us, sleep_ms

class HD44780_Driver:

    @staticmethod
    def init_manually_4pin(board: GPIO4_HAL):
        """
        **Initialization by instructions in 4pins**

        Inner reset circuit will work if the power conditions correctly,
        but if not that must reset manually by instructions.
        :param board: extend from GPIO4_HAL object.
        """
        sleep_ms(40)    # wait more than 40ms after Vcc to 2.7V

        board.write_4bit(RS_level=0,
                         RW_level=0,
                         DB7_level=0,
                         DB6_level=0,
                         DB5_level=1,
                         DB4_level=1,
                         delay_cycles=0)

        sleep_ms(4.1)   # wait more than 4.1ms

        board.write_4bit(RS_level=0,
                         RW_level=0,
                         DB7_level=0,
                         DB6_level=0,
                         DB5_level=1,
                         DB4_level=1,
                         delay_cycles=0)

        sleep_us(100)   # wait more than 100μs

        board.write_4bit(RS_level=0,
                         RW_level=0,
                         DB7_level=0,
                         DB6_level=0,
                         DB5_level=1,
                         DB4_level=1,
                         delay_cycles=1)


    @staticmethod
    def init_manually_8pin(board: GPIO8_HAL):
        """
        **Initialization by instructions in 8pins**

        Inner reset circuit will work if the power conditions correctly,
        but if not that must reset manually by instructions.
        :param board: extend from GPIO8_HAL object.
        """
        sleep_ms(40)    # wait for more than 40ms after Vcc to 2.7V

        board.write_8bit(RS_level=0,
                         RW_level=0,
                         DB7_level=0,
                         DB6_level=0,
                         DB5_level=1,
                         DB4_level=1,
                         DB3_level=0, DB2_level=0, DB1_level=0, DB0_level=0, #  DB0~DB3 are ignored
                         delay_cycles=0)

        sleep_ms(4.1)   # wait for more than 4.1ms

        board.write_8bit(RS_level=0,
                         RW_level=0,
                         DB7_level=0,
                         DB6_level=0,
                         DB5_level=1,
                         DB4_level=1,
                         DB3_level=0, DB2_level=0, DB1_level=0, DB0_level=0, #  DB0~DB3 are ignored
                         delay_cycles=0)

        sleep_us(100)   # wait more than 100μs

        board.write_8bit(RS_level=0,
                         RW_level=0,
                         DB7_level=0,
                         DB6_level=0,
                         DB5_level=1,
                         DB4_level=1,
                         DB3_level=0, DB2_level=0, DB1_level=0, DB0_level=0, #  DB0~DB3 are ignored
                         delay_cycles=1)


    board:General_HAL = None

    def __init__(self, board:General_HAL):
        self.board = board


    def clear_display(self):
        self.board.write(RS_level=instruction_set.WriteToCmdReg.RS,
                         DBs_level=instruction_set.WriteToCmdReg.LCD_CLEAR,
                         delay_cycles=42)   # need 1.52ms in typical frequency

    def return_home(self):
        self.board.write(RS_level=instruction_set.WriteToCmdReg.RS,
                         DBs_level=instruction_set.WriteToCmdReg.LCD_TO_HOME,
                         delay_cycles=42)    # need 1.52ms in typical frequency

    def entry_mode_set(self, cursor_increment:bool = True, display_shift:bool = False):

        instruction = (instruction_set.WriteToCmdReg._LCD_ENTRY_MODE
                       + (instruction_set.WriteToCmdReg._LCD_ENTRY_MODE_CURSOR_MOVE_LEFT
                           if cursor_increment
                           else instruction_set.WriteToCmdReg._LCD_ENTRY_MODE_CURSOR_MOVE_RIGHT)
                       + (instruction_set.WriteToCmdReg._LCD_ENTRY_MODE_SHIFT if display_shift else 0)
                       )

        self.board.write(RS_level=instruction_set.WriteToCmdReg.RS,
                         DBs_level= instruction)

    def display_control(self, display_on:bool=True, cursor_on=True, cursor_blink:bool=True):
        instruction = (instruction_set.WriteToCmdReg._LCD_DISPLAY
                      + (instruction_set.WriteToCmdReg._LCD_DISPLAY_ON
                          if display_on
                          else instruction_set.WriteToCmdReg._LCD_DISPLAY_OFF)
                      + (instruction_set.WriteToCmdReg._LCD_DISPLAY_CURSOR_ON
                          if cursor_on
                          else instruction_set.WriteToCmdReg._LCD_DISPLAY_CURSOR_OFF)
                      + (instruction_set.WriteToCmdReg._LCD_DISPLAY_CURSOR_BLINK if cursor_blink else 0)
                      )

        self.board.write(RS_level=instruction_set.WriteToCmdReg.RS,
                         DBs_level= instruction)

    def cursor_or_display_shift(self, move_cursor:bool, move_right:bool):
        instruction = (instruction_set.WriteToCmdReg._LCD_SHIFT
                       + (instruction_set.WriteToCmdReg._LCD_SHIFT_CURSOR
                          if move_cursor
                          else instruction_set.WriteToCmdReg._LCD_SHIFT_DISPLAY)
                       + (instruction_set.WriteToCmdReg._LCD_SHIFT_MOVE_RIGHT
                          if move_right
                          else instruction_set.WriteToCmdReg._LCD_SHIFT_MOVE_LEFT)
                       )

        self.board.write(RS_level=instruction_set.WriteToCmdReg.RS,
                         DBs_level= instruction)

    def function_set(self, length_8bit:bool, display_2lines:bool, font_5x10dot:bool):
        """

        :param length_8bit: True is 8bit, False is 4bit.
        :param display_2lines: True is 2 lines, False is 1 line. 5x10 dot only support 1 line and will as 1 line.
        :param font_5x10dot: True is 5x10 dots font, False is 5x8 dots.
        """
        instruction = (instruction_set.WriteToCmdReg._LCD_FUNCTION
                       + (instruction_set.WriteToCmdReg._LCD_FUNCTION_8bit
                          if length_8bit
                          else instruction_set.WriteToCmdReg._LCD_FUNCTION_4bit)
                       + (instruction_set.WriteToCmdReg._LCD_FUNCTION_2line
                          if display_2lines
                          else instruction_set.WriteToCmdReg._LCD_FUNCTION_1line)
                       + (instruction_set.WriteToCmdReg._LCD_FUNCTION_5x10dot
                          if font_5x10dot
                          else instruction_set.WriteToCmdReg._LCD_FUNCTION_5x8dot)
                       )

        self.board.write(RS_level=instruction_set.WriteToCmdReg.RS,
                         DBs_level= instruction)

    def set_cg_ram(self, address: int):
        instruction = instruction_set.WriteToCmdReg(address).SET_CGRAM_ADDRESS
        self.board.write(RS_level=instruction_set.WriteToCmdReg.RS,
                         DBs_level= instruction)

    def set_dd_ram(self, address: int):
        instruction = instruction_set.WriteToCmdReg(address).SET_DDRAM_ADDRESS
        self.board.write(RS_level=instruction_set.WriteToCmdReg.RS,
                         DBs_level= instruction)

    def read_busy_flag_and_address(self) -> (bool, int):
        """

        :return: (busy_flag, address), busy_flag is True means inner operating now and False is
        ready to accept instruction. address is current Address Counter, which is read depending on
        last SET_CGRAM_ADDRESS or SET_DDRAM_ADDRESS ran.
        """
        data = instruction_set.ReadFromCmdReg(self.board.read(RS_level=0))
        return bool(data.busy_flag), data.address

    def write_data_to_ram(self, data: int):
        self.board.write(RS_level=1, DBs_level=data)

    def read_data_from_ram(self):
        return self.board.read(RS_level=1)