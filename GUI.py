from colorama import Fore, Style

import pygame
from pygame.constants import MOUSEBUTTONDOWN

from board import PlayerBoard, ComputerBoard, GameOver
from game import ComputerPlayer


CELL_SIZE = 40  # Size of each cell in pixels
MARGIN = 5  # Space between cells
BOARD_SIZE = 15  # Number of rows/columns
SCREEN_SIZE = (BOARD_SIZE + 1) * (CELL_SIZE + MARGIN)  # Screen size
SCREEN_WIDTH = 2 * ((BOARD_SIZE + 1) * (CELL_SIZE + MARGIN))  # Two boards side by side
SCREEN_HEIGHT = (BOARD_SIZE + 1) * (CELL_SIZE + MARGIN)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# # Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
#
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Airplane Game")
font = pygame.font.SysFont("Arial", 20)
class GUI:
    def __init__(self):
        self.__user_board = PlayerBoard()
        self.__computer_board = ComputerBoard()
        self.__computer_player = ComputerPlayer(self.__computer_board, self.__user_board)
        self.current_orientation = 0  # 0 for horizontal, 1 for vertical

    def place_airplane(self, x, y):
        row = y // (CELL_SIZE + MARGIN)
        column = x // (CELL_SIZE + MARGIN)
        try:
            self.__user_board.place_airplane(row, column, self.current_orientation)
        except ValueError:
            print(Fore.RED + "Invalid position! Try again." + Style.RESET_ALL)

    def draw_board(self, board, x_offset=0, hide_airplanes=False):
        for row in range(1, board.size + 1):
            for col in range(1, board.size + 1):
                x = x_offset + col * (CELL_SIZE + MARGIN)
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
        self.__computer_player.place_plane()
        self.__computer_player.place_plane()
        human_player_turn = True

        clock = pygame.time.Clock()
        running = True
        userplanes = 0
        try:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    # Detect mouse click to place airplane
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        if userplanes < 3:
                            self.place_airplane(mouse_x, mouse_y)
                            userplanes += 1
                        else:
                            # Check if the click is within the computer's board area
                            if mouse_x >= SCREEN_WIDTH // 2:
                                adjusted_x = mouse_x - SCREEN_WIDTH // 2  # Adjust for board offset
                                row = mouse_y // (CELL_SIZE + MARGIN)
                                column = adjusted_x // (CELL_SIZE + MARGIN)
                                if 1 <= row <= BOARD_SIZE and 1 <= column <= BOARD_SIZE:
                                    try:
                                        self.__computer_board.hit(row, column)
                                        self.__computer_player.hit()
                                    except ValueError as e:
                                        print(Fore.RED + "Invalid hit position: " + str(e) + Style.RESET_ALL)
                                else:
                                    print(Fore.YELLOW + "Click out of bounds!" + Style.RESET_ALL)

                    # Change orientation with right click or key press
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.current_orientation = 1 - self.current_orientation  # Toggle orientation


                # Clear screen
                screen.fill(WHITE)

                # Draw the boards
                self.draw_board(self.__user_board, x_offset=0)  # User board on the left
                self.draw_board(self.__computer_board, x_offset=SCREEN_WIDTH // 2,
                                hide_airplanes=True)  # Computer board on the right

                # Update the display
                pygame.display.flip()
                clock.tick(60)

        except GameOver:
            print(Fore.GREEN + "Game over!" + Style.RESET_ALL)

        pygame.quit()

import pygame
from pygame.locals import *

# Constants for screen dimensions and colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Fonts for text
pygame.font.init()
font = pygame.font.SysFont("Arial", 30)


class GUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Airplane Game")
        self.clock = pygame.time.Clock()

        self.menu_screen = True
        self.game_screen = False
        self.game_over_screen = False

        # Add difficulty level to menu
        self.difficulty = 'Normal'

        self.__user_board = PlayerBoard()
        self.__computer_board = ComputerBoard()
        self.__computer_player = ComputerPlayer(self.__computer_board, self.__user_board)
        self.current_orientation = 0  # 0 for horizontal, 1 for vertical

    def place_airplane(self, x, y):
        row = y // (CELL_SIZE + MARGIN)
        column = x // (CELL_SIZE + MARGIN)
        # try:
        self.__user_board.place_airplane(row, column, self.current_orientation)
        # except ValueError:
        #     print(Fore.RED + "Invalid position! Try again." + Style.RESET_ALL)

    def draw_board(self, board, x_offset=0, hide_airplanes=False):
        for row in range(1, board.size + 1):
            for col in range(1, board.size + 1):
                x = x_offset + col * (CELL_SIZE + MARGIN)
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
        self.game_screen = True
        self.menu_screen = False
        self.__computer_player.place_plane()
        self.__computer_player.place_plane()
        self.__computer_player.place_plane()
        human_player_turn = True

        clock = pygame.time.Clock()
        running = True
        userplanes = 0
        try:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    # Detect mouse click to place airplane
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        if userplanes < 3:
                            try:
                                self.place_airplane(mouse_x, mouse_y)
                                userplanes += 1
                            except:
                                print(Fore.RED + "Invalid position! Try again." + Style.RESET_ALL)
                        else:
                            # Check if the click is within the computer's board area
                            if mouse_x >= SCREEN_WIDTH // 2:
                                adjusted_x = mouse_x - SCREEN_WIDTH // 2  # Adjust for board offset
                                row = mouse_y // (CELL_SIZE + MARGIN)
                                column = adjusted_x // (CELL_SIZE + MARGIN)
                                if 1 <= row <= BOARD_SIZE and 1 <= column <= BOARD_SIZE:
                                    try:
                                        self.__computer_board.hit(row, column)
                                        self.__computer_player.hit()
                                    except ValueError as e:
                                        print(Fore.RED + "Invalid hit position: " + str(e) + Style.RESET_ALL)
                                else:
                                    print(Fore.YELLOW + "Click out of bounds!" + Style.RESET_ALL)

                    # Change orientation with right click or key press
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.current_orientation = 1 - self.current_orientation  # Toggle orientation

                # Clear screen
                screen.fill(WHITE)

                # Draw the boards
                self.draw_board(self.__user_board, x_offset=0)  # User board on the left
                self.draw_board(self.__computer_board, x_offset=SCREEN_WIDTH // 2,
                                hide_airplanes=True)  # Computer board on the right

                # Update the display
                pygame.display.flip()
                clock.tick(60)

        except GameOver:
            print(Fore.GREEN + "Game over!" + Style.RESET_ALL)

        pygame.quit()
    def draw_button(self, text, x, y):
        pygame.draw.rect(self.screen, GREEN, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
        text_surface = font.render(text, True, BLACK)
        self.screen.blit(text_surface, (x + 30, y + 10))

    def menu(self):
        self.screen.fill(WHITE)

        # Draw the buttons for difficulty and start game
        self.draw_button("Start Game", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2)
        self.draw_button("Set Difficulty: " + self.difficulty, SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
                         SCREEN_HEIGHT // 2 + BUTTON_HEIGHT)

        pygame.display.flip()

    def game_over(self):
        self.screen.fill(WHITE)

        # Draw game over screen with buttons
        self.draw_button("Back to Menu", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2)
        self.draw_button("Play Again", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.draw_button("Exit", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTON_HEIGHT)

        pygame.display.flip()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                if self.menu_screen:
                    # Start Game Button
                    if (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 < mouse_x < SCREEN_WIDTH // 2 + BUTTON_WIDTH // 2 and
                            SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2 < mouse_y < SCREEN_HEIGHT // 2 + BUTTON_HEIGHT // 2):
                        self.start_game()
                        print("Start Game Button Clicked")

                    # Difficulty Button (here you can toggle difficulty)
                    if (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 < mouse_x < SCREEN_WIDTH // 2 + BUTTON_WIDTH // 2 and
                            SCREEN_HEIGHT // 2 + BUTTON_HEIGHT < mouse_y < SCREEN_HEIGHT // 2 + 2 * BUTTON_HEIGHT):
                        self.difficulty = 'Hard' if self.difficulty == 'Normal' else 'Normal'

                elif self.game_over_screen:
                    # Play Again Button
                    if (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 < mouse_x < SCREEN_WIDTH // 2 + BUTTON_WIDTH // 2 and
                            SCREEN_HEIGHT // 2 < mouse_y < SCREEN_HEIGHT // 2 + BUTTON_HEIGHT):
                        self.start_game()  # Restart the game

                    # Back to Menu Button
                    if (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 < mouse_x < SCREEN_WIDTH // 2 + BUTTON_WIDTH // 2 and
                            SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2 < mouse_y < SCREEN_HEIGHT // 2):
                        self.menu_screen = True
                        self.game_over_screen = False

                    # Exit Button
                    if (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 < mouse_x < SCREEN_WIDTH // 2 + BUTTON_WIDTH // 2 and
                            SCREEN_HEIGHT // 2 + BUTTON_HEIGHT < mouse_y < SCREEN_HEIGHT // 2 + 2 * BUTTON_HEIGHT):
                        pygame.quit()
                        exit()

    def update(self):
        # Update the game state here (this would be where your game logic goes)
        if self.game_screen:
            pass  # Update game state for when the game is active

    def draw(self):
        if self.menu_screen:
            self.menu()
        elif self.game_screen:
            # Draw game here
            pass
        elif self.game_over_screen:
            self.game_over()

    def main_loop(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)





