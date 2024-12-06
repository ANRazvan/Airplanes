from colorama import Fore, Style

import pygame
from board import PlayerBoard, ComputerBoard, GameOver
from game import ComputerPlayer

CELL_SIZE = 40  # Size of each cell in pixels
MARGIN = 5  # Space between cells
BOARD_SIZE = 15  # Number of rows/columns
SCREEN_SIZE = (BOARD_SIZE + 1) * (CELL_SIZE + MARGIN)  # Screen size

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Airplane Game")
font = pygame.font.SysFont("Arial", 20)

class Console:
    def __init__(self):
        self.__user_board = PlayerBoard()
        self.__computer_board = ComputerBoard()
        self.__computer_player = ComputerPlayer(self.__computer_board, self.__user_board)

    def __place_user_ship(self):
        try:
            print("Place ship:")
            row = int(input("Row:"))
            column = int(input("Column:"))
            orientation = int(input("Orientation (0 for horizontal, 1 for vertical):"))
            self.__user_board.place_airplane(row, column, orientation)

        except ValueError as e:
            print(Fore.RED + str(e) + Style.RESET_ALL)
            self.__place_user_ship()

    def print_current_game_state(self):
        #Moved to function & added colors
        print(Fore.YELLOW)
        print('The computer\'s board')
        print(self.__computer_board)
        print(Style.RESET_ALL)
        print(Fore.BLUE)
        print('The user board (my board):')
        print(self.__user_board)
        print(Style.RESET_ALL)

    def draw_board(self, board, hide_airplanes=False):
        screen.fill(WHITE)
        for row in range(1, board.size + 1):
            for col in range(1, board.size + 1):
                x = col * (CELL_SIZE + MARGIN)
                y = row * (CELL_SIZE + MARGIN)

                cell_value = board._board[row][col]
                color = GRAY  # Default color

                if cell_value == 'H':  # Hit
                    color = RED
                elif cell_value == 'O':  # Miss
                    color = BLUE
                elif cell_value == 'X' and not hide_airplanes:  # Airplane visible
                    color = GREEN

                # Draw cell rectangle
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

                # Draw border
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

                # Optionally render text
                if hide_airplanes and cell_value == 'X':
                    cell_value = ' '  # Hide airplanes
                if cell_value != ' ':
                    text = font.render(cell_value, True, BLACK)
                    screen.blit(text, (x + CELL_SIZE // 3, y + CELL_SIZE // 4))

    def start_game(self):

        self.__computer_player.place_plane()
        self.__place_user_ship()
        print("Initial boards:")
        self.print_current_game_state()
        human_player_turn = True
        #TO DO: eliminate duplicate code (e.g. exception catching)

        self.__user_board.place_airplane(5, 5, 0)
        self.__user_board.place_airplane(10, 10, 1)
        self.__user_board.hit(5, 5)
        self.__user_board.hit(6, 6)

        self.__computer_player.place_airplane(3, 3, 0)
        self.__computer_player.place_airplane(8, 8, 1)
        self.__computer_player.hit(3, 3)

        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw the boards
            self.draw_board(self.__user_board)  # For player's view
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        while True:
            if human_player_turn:
                print("Input coordinates for hit:")
                row = int(input("Row:"))
                column = int(input("Column:"))
                try:
                    self.__computer_board.hit(row, column)
                    human_player_turn = False
                    self.print_current_game_state()

                except GameOver as e:
                    print("Human has won the game.")
                    break
                except ValueError as e:
                    print(e)
            else:
                try:
                    computer_attempt = self.__computer_player.hit()
                    row, column = computer_attempt
                    print("Computer player attempting to hit:", row, column)
                    human_player_turn = True
                    self.print_current_game_state()

                except GameOver as e:
                    print("Computer has won the game.")
                    break
                except ValueError as e:
                    print(e)
