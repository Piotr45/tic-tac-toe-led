#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import tty
import sys
import termios

from interface.led_matrix import *
from logic.game import *

board = [
        [0, -1, -1, -1],
        [1, 0, -1, -1],
        [1, 1, 0, -1],
        [1, 1, 1, 0]
]

CONVERTER = {
    '1': (0, 0), '2': (0, 1), '3': (0, 2), '4': (0, 3),
    'q': (1, 0), 'w': (1, 1), 'e': (1, 2), 'r': (1, 3),
    'a': (2, 0), 's': (2, 1), 'd': (2, 2), 'f': (2, 3),
    'z': (3, 0), 'x': (3, 1), 'c': (3, 2), 'v': (3, 3)
}

FILE_DESCRIPTOR = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)


def play_against_ai(device):
    game = TicTacToe(4, 3)
    turn = True
    display_texts(device, ["Start"])
    while True:
        if game.is_complete():
            is_win, player_id = game.is_win()
            if is_win:
                time.sleep(0.3)
                display_texts(device, [f"{'Player o' if player_id == 1 else 'AI'} wins!"])
            if player_id == 0:
                time.sleep(0.3)
                display_texts(device, ["Tie"])
            try:
                display_texts(device, ["q Quit to main menu.", "r Restart game."])
                _input = sys.stdin.read(1)[0]
                if _input == 'q':
                    break
                if _input == 'r':
                    game.restart_game()
                    turn = True
            except KeyError:
                pass
        else:
            try:
                if turn:
                    _input = sys.stdin.read(1)[0]
                    row, col = CONVERTER[_input]
                    while not game.is_valid_move(row, col):
                        print("Invalid move! Try again!")
                        _input = sys.stdin.read(1)[0]
                        row, col = CONVERTER[_input]
                    game.make_move(1, row, col)
                else:
                    val, ai_move = game.minmax(-1)
                    game.make_move(-1, ai_move[0], ai_move[1])
                turn = not turn
                display_game_board(board=game.board, device=device)
            except KeyError:
                pass
    return 


def play_local(device):
    game = TicTacToe(4, 3)
    turn = True
    display_texts(device, ["Start"])
    while True:
        if game.is_complete():
            is_win, player_id = game.is_win()
            if is_win:
                time.sleep(0.3)
                display_texts(device, [f"Player {'o' if player_id == 1 else 'x'} wins!"])
            if player_id == 0:
                time.sleep(0.3)
                display_texts(device, ["Tie"])
            try:
                display_texts(device, ["q Quit to main menu.", "r Restart game."])
                _input = sys.stdin.read(1)[0]
                if _input == 'q':
                    break
                if _input == 'r':
                    game.restart_game()
                    turn = True
            except KeyError:
                pass
        else:
            try:
                _input = sys.stdin.read(1)[0]
                row, col = CONVERTER[_input]
                while not game.is_valid_move(row, col):
                    print("Invalid move! Try again!")
                    _input = sys.stdin.read(1)[0]
                    row, col = CONVERTER[_input]
                if turn:
                    game.make_move(1, row, col)
                else:
                    game.make_move(-1, row, col)
                turn = not turn
                display_game_board(board=game.board, device=device)
            except KeyError:
                pass
    return 


def game_loop(device):
    while True:
        display_texts(device, ["1. Local", "2. AI", "3. Quit"])
        try:
            _input = sys.stdin.read(1)[0]
            if _input == '1':
                play_local(device)
            elif _input == '2':
                play_against_ai(device)
            elif _input == '3':
                break
        except KeyError:
            pass


if __name__ == '__main__':
    try:
        device = create_device()

        game_loop(device)
    except KeyboardInterrupt:
        pass
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, FILE_DESCRIPTOR)
