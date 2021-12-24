#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219

LED_MATRIX = {
    # Matrix 1
    0: (2, -1),
    1: (10, -1),
    2: (18, -1),
    3: (26, -1),
    # Matrix 2
    4: (25, 8),
    5: (17, 8),
    6: (9, 8),
    7: (1, 8),
    # Matrix 3
    8: (2, 15),
    9: (10, 15),
    10: (18, 15),
    11: (26, 15),
    # Matrix 4
    12: (25, 24),
    13: (17, 24),
    14: (9, 24),
    15: (1, 24),
}

SYMBOLS = {
    'x': chr(120),
    'o': chr(111)
}


def create_device() -> max7219:
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, height=32, width=32, block_orientation=-90,
                     rotate=0, blocks_arranged_in_reverse_order=False)
    print("Created device")
    device.contrast(64)
    return device


def display_symbol(draw, symbol, index, fill='white', font=proportional(SINCLAIR_FONT)) -> None:
    text(draw, LED_MATRIX[index], symbol, fill=fill, font=font)


def display_game_board(board, device) -> None:
    with canvas(device) as draw:
        for i, row in enumerate(board):
            for j, col_value in enumerate(row):
                if col_value == -1:
                    display_symbol(draw, SYMBOLS['x'], i*4+j)
                elif col_value == 1:
                    display_symbol(draw, SYMBOLS['o'], i*4+j)
