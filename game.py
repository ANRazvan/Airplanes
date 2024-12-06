import random

# from src2023.seminar.group917.Seminar_13 import RepoExceptions
# from src2023.seminar.group917.Seminar_13.RepoExceptions import OutsideOfBoundsError, RepositoryExceptions


class ComputerPlayer:
    def __init__(self, player_board, other_board):
        self.__own_board = player_board
        self.__other_player_board = other_board

    def place_plane(self):
        # place it on its own board
        try:
            row = random.randint(3, self.__own_board.size - 3)
            column = random.randint(3, self.__own_board.size - 3)
            orientation = random.randint(0, 1)
            self.__own_board.place_airplane(row, column, orientation)
            print("Computer placed airplane at:")
            print(row, column,orientation)

        except ValueError:
            self.place_plane()

    def hit(self):

        row = random.randint(0, self.__own_board.size - 1)
        column = random.randint(0, self.__own_board.size - 1)

        self.__other_player_board.hit(row, column)
        return row, column

