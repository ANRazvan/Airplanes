from texttable import Texttable


class GameOver(Exception):
    pass


class Board:
    def __init__(self, size=15):
        self.__size = size
        self._board = [[' ' for _ in range(self.__size + 1)] for _ in range(self.__size + 1)]
        self.__hits = 0

    @property
    def size(self):
        return self.__size

    # an airplane looks like this:
    """
        X
    X X X X X 
        X
      X X X
    """

    def place_airplane(self, row, column, orientation):
        """

        :param self:
        :param row: row index for head of the plane
        :param column: column index for head of the plane
        :param orientation: orientation = 0 means horizontal, orientation = 1 means vertical
        :return:
        """
        if orientation == 0:
            if row < 3 or row > self.size - 2 or column < 0 or column > self.size - 3:
                raise ValueError()
            # check if position is already occupied
            if self._board[row][column] != ' ':
                raise ValueError()
            if self._board[row][column + 1] != ' ':
                raise ValueError()
            if self._board[row - 1][column + 1] != ' ':
                raise ValueError()
            if self._board[row + 1][column + 1] != ' ':
                raise ValueError()
            if self._board[row - 2][column + 1] != ' ':
                raise ValueError()
            if self._board[row + 2][column + 1] != ' ':
                raise ValueError()
            if self._board[row][column + 2] != ' ':
                raise ValueError()
            if self._board[row][column + 3] != ' ':
                raise ValueError()
            if self._board[row - 1][column + 3] != ' ':
                raise ValueError()
            if self._board[row + 1][column + 3] != ' ':
                raise ValueError()

            self._board[row][column] = 'X'

            self._board[row][column + 1] = 'X'
            self._board[row - 1][column + 1] = 'X'
            self._board[row + 1][column + 1] = 'X'
            self._board[row - 2][column + 1] = 'X'
            self._board[row + 2][column + 1] = 'X'

            self._board[row][column + 2] = 'X'

            self._board[row][column + 3] = 'X'
            self._board[row - 1][column + 3] = 'X'
            self._board[row + 1][column + 3] = 'X'

        elif orientation == 1:
            if row < 0 or row > self.size - 3 or column < 3 or column > self.size - 2:
                raise ValueError()

            # check if position is already occupied
            if self._board[row][column] != ' ':
                raise ValueError()
            if self._board[row + 1][column] != ' ':
                raise ValueError()
            if self._board[row + 1][column - 1] != ' ':
                raise ValueError()
            if self._board[row + 1][column + 1] != ' ':
                raise ValueError()
            if self._board[row + 1][column - 2] != ' ':
                raise ValueError()
            if self._board[row + 1][column + 2] != ' ':
                raise ValueError()
            if self._board[row + 2][column] != ' ':
                raise ValueError()
            if self._board[row + 3][column] != ' ':
                raise ValueError()
            if self._board[row + 3][column - 1] != ' ':
                raise ValueError()
            if self._board[row + 3][column + 1] != ' ':
                raise ValueError()

            self._board[row][column] = 'X'
            self._board[row + 1][column] = 'X'
            self._board[row + 1][column - 1] = 'X'
            self._board[row + 1][column + 1] = 'X'
            self._board[row + 1][column - 2] = 'X'
            self._board[row + 1][column + 2] = 'X'

            self._board[row + 2][column] = 'X'

            self._board[row + 3][column] = 'X'
            self._board[row + 3][column - 1] = 'X'
            self._board[row + 3][column + 1] = 'X'

    def hit(self, row, column):
        """
        if  the cell is empty, it will be marked with 'O'
        if the cell is occupied by a plane, it will be marked with 'X'
        :param self:
        :param row: row index of the hit
        :param column: column index of the hit
        :return:
        """
        print(self._board[row][column])
        if self._board[row][column] == 'X':
            self.__hits += 1
            self._board[row][column] = 'H'
            if self.__hits == 30:
                raise GameOver()
        elif self._board[row][column] == ' ':
            self._board[row][column] = 'O'
        elif self._board[row][column] == 'H':
            print('You already hit this cell')


class PlayerBoard(Board):
    def __str__(self):
        table = Texttable()
        header = [' '] + [str(i) for i in range(1, self.size + 1)]
        table.header(header)

        for i in range(1, self.size + 1):
            row = [str(i)] + self._board[i][1:]
            table.add_row(row)

        return table.draw()


class ComputerBoard(Board):
    def __str__(self):
        table = Texttable()
        #indices of columns
        header = [' '] + [str(i) for i in range(1, self.size + 1)]
        table.header(header)

        for i in range(1, self.size + 1):
            row = self._board[i][1:]
            #Replaced the if-else, renamed
            row_with_boat_hidden = [' ' if cell == 'X' else cell for cell in row]
            #add index of row
            row = [str(i)] + row_with_boat_hidden
            table.add_row(row)

        return table.draw()
