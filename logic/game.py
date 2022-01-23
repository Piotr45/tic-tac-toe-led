import numpy as np


class TicTacToe:
    def __init__(self, size=4, max_depth=3) -> None:
        self.__board_size = size
        self.board = np.zeros((self.__board_size, self.__board_size))
        self.__max_depth = max_depth
        self.__available_moves = []

    def restart_board(self) -> None:
        self.board = np.zeros(self.__board_size)

    def restart_game(self) -> None:
        self.restart_board()

    def is_valid_move(self, row_number, col_number) -> bool:
        return self.board[row_number][col_number] == 0

    def get_available_moves(self):
        self.__available_moves = []
        for i in range(self.__board_size):
            for j in range(self.__board_size):
                if self.board[i][j] == 0:
                    self.__available_moves.append((i, j))
        return self.__available_moves

    def make_move(self, player, row_number, col_number) -> None:
        if self.is_valid_move(row_number, col_number):
            self.board[row_number][col_number] = player
        else:
            print("Invalid Move")

    def is_complete(self):
        if 0 not in self.board:
            return True
        is_win, winner = self.is_win()
        if is_win:
            return True
        return False

    def is_win(self) -> (bool, int):
        indexes = np.arange(0, self.__board_size)
        for index in range(self.__board_size):
            if np.sum(self.board[index]) == self.__board_size or \
              np.sum(self.board[:, index]) == self.__board_size:
                return True, 1
            if np.sum(self.board[index]) == -self.__board_size or \
              np.sum(self.board[:, index]) == -self.__board_size:
                return True, -1
            if np.sum(self.board[indexes, indexes]) == self.__board_size or \
                np.sum(self.board[indexes, indexes[::-1]]) == self.__board_size:
                return True, 1
            if np.sum(self.board[indexes, indexes]) == -self.__board_size or \
                np.sum(self.board[indexes, indexes[::-1]]) == -self.__board_size:
                return True, -1
        return False, 0

    def minmax(self, player, depth=0):
        if player == 1:
          best_score = -10
        else:
          best_score = 10

        if self.is_complete():
          is_win, winner = self.is_win()
          if winner == -1:
            return -10 + depth, None
          elif winner == 0:
            return 0, None
          elif winner == 1:
            return 10 - depth, None

        best_move = self.get_available_moves()[0]

        for move in self.get_available_moves():
            if depth >= self.__max_depth:
                return best_score, best_move
            
            self.board[move[0], move[1]] = player
            val, _ = self.minmax(-player, depth + 1)
            self.board[move[0], move[1]] = 0
            
            if player == 1:
                if val > best_score:
                    best_score = val
                    best_move = move
            else:
                if val < best_score:
                    best_score = val
                    best_move = move
        return best_score, best_move
