# Importing Pygame
import pygame
from pygame.locals import *


# Initializing Pygame
pygame.init()
pygame.font.init()

# Screen
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h - 60
screen = pygame.display.set_mode((screen_width, screen_height))

# Title
pygame.display.set_caption("TicTacToe Warfare")

# Font
font1 = pygame.font.Font(None, 50)
font2 = pygame.font.SysFont("Times New Roman",100)
font3 = pygame.font.Font(None, 75)
font_color = (255, 255, 255)

# Board
board_length = min(screen.get_width(), screen.get_height()) * 0.9
board_x = (screen_width - board_length) // 2
board_y = (screen_height - board_length) // 2
board_line_thickness = 10

# Cells
cell_length = board_length // 3

# Reduction factor for sub-boards
reduction_factor = 0.8

# Sub-Board
sub_board_length = cell_length * reduction_factor
sub_board_win = [[False for i in range(3)] for i in range(3)]

# Sub-Cells
sub_cell_length = sub_board_length // 3
sub_cell_line_thickness = 2

# Teams
team1_mem = ["symbol1", "symbol3"]
team2_mem = ["symbol2", "symbol4"]

# To check if a sub cell is being highlighted
highlighted_sub_cell = None

# Defining colour constants
Background_Colour = (230, 204, 153)
Highlight_Colour = (240, 240, 240, 100)  # Light gray with transparency
Sub_Board_Colour = (0, 0, 0)
Board_Colour = (0, 0, 0)

# Power-Up images
nuke_image = pygame.image.load("nuke.png")
missile_image = pygame.image.load("missile.png")
nuke_image_scaled = pygame.transform.smoothscale(nuke_image, (sub_cell_length*2, sub_cell_length*2))
missile_image_scaled = pygame.transform.smoothscale(missile_image,(sub_cell_length*2, sub_cell_length*2))

# Team win images
team1_image = pygame.image.load("one.png")
team2_image = pygame.image.load("two.png")

# Player Symbols
symbol1_image = pygame.image.load("x.png")
symbol1_image = pygame.transform.smoothscale(symbol1_image, (sub_cell_length, sub_cell_length))
symbol2_image = pygame.image.load("o.png")
symbol2_image = pygame.transform.smoothscale(symbol2_image, (sub_cell_length, sub_cell_length))
symbol3_image = pygame.image.load("plus.png")
symbol3_image = pygame.transform.smoothscale(symbol3_image, (sub_cell_length, sub_cell_length))
symbol4_image = pygame.image.load("square.png")
symbol4_image = pygame.transform.smoothscale(symbol4_image, (sub_cell_length, sub_cell_length))

# Symbol reductions
symbol_size = sub_cell_length * 0.8


# Player Symbols scaled
symbol1_image_scaled = pygame.transform.smoothscale(symbol1_image, (symbol_size, symbol_size))
symbol2_image_scaled = pygame.transform.smoothscale(symbol2_image, (symbol_size, symbol_size))
symbol3_image_scaled = pygame.transform.smoothscale(symbol3_image, (symbol_size, symbol_size))
symbol4_image_scaled = pygame.transform.smoothscale(symbol4_image, (symbol_size, symbol_size))

# offset to align symbols to respective subcells
symbol_offset = (sub_cell_length - symbol_size) // 2
symbol2_offset = (cell_length + sub_cell_length*3) // 11

# Player Board win symbols
symbol1_board_win = pygame.transform.smoothscale(symbol1_image, (int(sub_cell_length*3), int(sub_cell_length*3)))
symbol2_board_win = pygame.transform.smoothscale(symbol2_image, (int(sub_cell_length*3), int(sub_cell_length*3)))
symbol3_board_win = pygame.transform.smoothscale(symbol3_image, (int(sub_cell_length*3), int(sub_cell_length*3)))
symbol4_board_win = pygame.transform.smoothscale(symbol4_image, (int(sub_cell_length*3), int(sub_cell_length*3)))

# Team win symbols
team1_win = pygame.transform.smoothscale(team1_image, (int(cell_length*3), int(cell_length*3)))
team2_win = pygame.transform.smoothscale(team2_image, (int(cell_length*3), int(cell_length*3)))


# Initialize the state of each cell
cell_states = [[None for i in range(3)] for i in range(3)]
sub_cell_states = [[[[None for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]
previous_x_state = [[None for i in range(3)] for i in range(3)]
previous_y_state = [[None for i in range(3)] for i in range(3)]
previous_plus_state = [[None for i in range(3)] for i in range(3)]
previous_square_state = [[None for i in range(3)] for i in range(3)]

# Team information
team1 = {
    "name": "Team 1",
    "nuke": 0,
    "missile": 0
}

team2 = {
    "name": "Team 2",
    "nuke": 0,
    "missile": 0
}

running = 0

current_symbol = symbol1_image_scaled  # Start with symbol1
turn_count = 1

# To keep track of last placed subboard for each symbol
turn_x = [[[[None for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]
turn_y = [[[[None for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]
turn_plus = [[[[None for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]
turn_square = [[[[None for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]

# To switch between symbol placing and power ups
place_mode = "Symbol"

# Menu Screen
def menu_screen():
    global running
    while True:
        screen.fill(Background_Colour)  # Fill the screen with black color

        title_text = font2.render("Tic Tac Toe Warfare", True, (0, 0, 0))
        title_text_rect = title_text.get_rect(center=(screen_width // 2, 50))
        screen.blit(title_text, title_text_rect)

        button_width = 200
        button_height = 50

        # Create a "Pass & Play" button
        button1_x = (screen_width - button_width) // 2
        button1_y = (screen_height - button_height) // 2
        pygame.draw.rect(screen, Background_Colour, (button1_x, button1_y, button_width, button_height))
        button1_text = font3.render("Pass & Play", True, font_color)
        button1_text_rect = button1_text.get_rect(center=(button1_x + button_width // 2, button1_y + button_height // 2))
        screen.blit(button1_text, button1_text_rect)

        # Create Join Button
        button2_x = (screen_width - button_width) // 2
        button2_y = (screen_height + (button_height*2)) // 2
        pygame.draw.rect(screen, Background_Colour, (button2_x, button2_y, button_width, button_height))
        button2_text = font3.render("Join", True, font_color)
        button2_text_rect = button2_text.get_rect(
            center=(button2_x + button_width // 2, button2_y + button_height // 2))
        screen.blit(button2_text, button2_text_rect)

        # Create Create Button
        button3_x = (screen_width - button_width) // 2
        button3_y = (screen_height + (button_height*5)) // 2
        pygame.draw.rect(screen, Background_Colour, (button3_x, button3_y, button_width, button_height))
        button3_text = font3.render("Create", True, font_color)
        button3_text_rect = button3_text.get_rect(
            center=(button3_x + button_width // 2, button3_y + button_height // 2))
        screen.blit(button3_text, button3_text_rect)

        pygame.display.flip()  # Update the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                if button1_x <= mouse_x <= button1_x + button_width and button1_y <= mouse_y <= button1_y + button_height:
                    running = 1
                    return  # Return from the menu screen function to start the game
                elif button2_x <= mouse_x <= button2_x + button_width and button2_y <= mouse_y <= button2_y + button_height:
                    running = 2
                    return
                elif button3_x <= mouse_x <= button3_x + button_width and button3_y <= mouse_y <= button3_y + button_height:
                    running = 3
                    return


def draw_board(board_x, board_y, board_length, cell_length,
               sub_board_length, sub_cell_length, board_line_thickness,
               sub_cell_line_thickness):
    for i in range(1, 3):
        pygame.draw.line(
            screen,
            Board_Colour,
            (board_x + i * cell_length, board_y),
            (board_x + i * cell_length, board_y + board_length),
            board_line_thickness,
        )

        pygame.draw.line(
            screen,
            Board_Colour,
            (board_x, board_y + i * cell_length),
            (board_x + board_length, board_y + i * cell_length),
            board_line_thickness,
        )

    for cell_row in range(3):
        for cell_col in range(3):
            sub_board_x = board_x + cell_col * cell_length + (cell_length - sub_board_length) // 2
            sub_board_y = board_y + cell_row * cell_length + (cell_length - sub_board_length) // 2

            for i in range(1, 3):
                pygame.draw.line(
                    screen,
                    Sub_Board_Colour,
                    (sub_board_x + i * sub_cell_length, sub_board_y),
                    (sub_board_x + i * sub_cell_length, sub_board_y + sub_board_length),
                    sub_cell_line_thickness,
                )

                pygame.draw.line(
                    screen,
                    Sub_Board_Colour,
                    (sub_board_x, sub_board_y + i * sub_cell_length),
                    (sub_board_x + sub_board_length, sub_board_y + i * sub_cell_length),
                    sub_cell_line_thickness,
                )

            for sub_cell_row in range(3):
                for sub_cell_col in range(3):
                    sub_board_cell_x = sub_board_x + sub_cell_col * sub_cell_length
                    sub_board_cell_y = sub_board_y + sub_cell_row * sub_cell_length

                    if (
                            sub_cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] == symbol1_image_scaled
                            and (cell_col, cell_row, sub_cell_col, sub_cell_row) != highlighted_sub_cell
                    ):
                        screen.blit(symbol1_image_scaled,
                                    (sub_board_cell_x + symbol_offset, sub_board_cell_y + symbol_offset))
                    elif (
                            sub_cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] == symbol2_image_scaled
                            and (cell_col, cell_row, sub_cell_col, sub_cell_row) != highlighted_sub_cell
                    ):
                        screen.blit(symbol2_image_scaled,
                                    (sub_board_cell_x + symbol_offset, sub_board_cell_y + symbol_offset))
                    elif (
                            sub_cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] == symbol3_image_scaled
                            and (cell_col, cell_row, sub_cell_col, sub_cell_row) != highlighted_sub_cell
                    ):
                        screen.blit(symbol3_image_scaled,
                                    (sub_board_cell_x + symbol_offset, sub_board_cell_y + symbol_offset))
                    elif (
                            sub_cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] == symbol4_image_scaled
                            and (cell_col, cell_row, sub_cell_col, sub_cell_row) != highlighted_sub_cell
                    ):
                        screen.blit(symbol4_image_scaled,
                                    (sub_board_cell_x + symbol_offset, sub_board_cell_y + symbol_offset))

                    if (cell_col, cell_row, sub_cell_col, sub_cell_row) == highlighted_sub_cell:
                        pygame.draw.rect(
                            screen,
                            Highlight_Colour,
                            pygame.Rect(
                                sub_board_cell_x,
                                sub_board_cell_y,
                                sub_cell_length,
                                sub_cell_length,
                            ),
                        )

def board_pos(mouse_x, mouse_y, board_x, board_y, board_length, cell_length,
              place_mode, sub_cell_states, sub_board_win):
    highlighted_sub_cell = None
    if board_x <= mouse_x <= board_x + board_length and board_y <= mouse_y <= board_y + board_length:
        cell_col = int((mouse_x - board_x) // cell_length)
        cell_row = int((mouse_y - board_y) // cell_length)
        sub_board_x = board_x + cell_col * cell_length + (cell_length - sub_board_length) // 2
        sub_board_y = board_y + cell_row * cell_length + (cell_length - sub_board_length) // 2

        sub_cell_col = int(
            (mouse_x - board_x - cell_col * cell_length - (cell_length - sub_board_length) // 2) // sub_cell_length
        )
        sub_cell_row = int(
            (mouse_y - board_y - cell_row * cell_length - (cell_length - sub_board_length) // 2) // sub_cell_length
        )

        if place_mode == "Symbol":
            if (
                    0 <= sub_cell_col < 3
                    and 0 <= sub_cell_row < 3
                    and sub_cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] is None
                    and not sub_board_win[cell_row][cell_col]  # Check if sub-board is already won
            ):
                highlighted_sub_cell = (cell_col, cell_row, sub_cell_col, sub_cell_row)
        else:
            if (
                    0 <= sub_cell_col < 3
                    and 0 <= sub_cell_row < 3
                    and sub_cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] is not None
                    and not sub_board_win[cell_row][cell_col]  # Check if sub-board is already won
            ):
                highlighted_sub_cell = (cell_col, cell_row, sub_cell_col, sub_cell_row)

# Rendering place mode and symbol counter
def render_place_mode(current_symbol):
    # Render place_mode text
    current_symbol = pygame.transform.smoothscale(current_symbol, (symbol_size - 15, symbol_size - 15))
    place_mode_text = font1.render("Place Mode: " + place_mode, True, font_color)
    place_mode_rect = place_mode_text.get_rect()

    place_mode_rect.topleft = (screen_width // 4.0, 10)

    screen.blit(place_mode_text, place_mode_rect)

    turn_text = font1.render("Current Symbol: ", True, font_color)
    turn_text_rect = turn_text.get_rect()

    turn_text_rect.topleft = (screen_width // 2, 10)
    screen.blit(turn_text, turn_text_rect)

    symbol_rect = current_symbol.get_rect()
    symbol_rect.topleft = (turn_text_rect.right + 10, 10)
    screen.blit(current_symbol, symbol_rect)

# Rendering Icons and team text
def render_icons(text, x, y, nuke_count, missile_count, symbol1, symbol2, align='left'):
    text_surface = font1.render(text, True, font_color)
    text_rect = text_surface.get_rect()

    if align == 'left':
        text_rect.topleft = (x, y)
    elif align == 'right':
        text_rect.topright = (x, y)

    screen.blit(text_surface, text_rect)

    # Position symbol1
    symbol1_rect = symbol1.get_rect()
    if align == 'left':
        symbol1_rect.topleft = (text_rect.right + 20, y)
    elif align == 'right':
        symbol1_rect.topright = (text_rect.left - 20, y)
    screen.blit(symbol1, symbol1_rect)

    # Position symbol2
    symbol2_rect = symbol2.get_rect()
    if align == 'left':
        symbol2_rect.topleft = (symbol1_rect.right + 20, y)
    elif align == 'right':
        symbol2_rect.topright = (symbol1_rect.left - 20, y)
    screen.blit(symbol2, symbol2_rect)

    missile_image_rect = missile_image_scaled.get_rect()

    if align == 'left':
        missile_image_rect.topleft = (text_rect.left, screen.get_height() - missile_image_rect.height)
    elif align == 'right':
        missile_image_rect.topright = (text_rect.right, screen.get_height() - missile_image_rect.height)

    # Blit the missile onto the screen
    screen.blit(missile_image_scaled, missile_image_rect)

    # Display missile count on the bottom right of the missile image
    missile_count_text = font1.render(str(missile_count), True, font_color)
    missile_count_rect = missile_count_text.get_rect()
    missile_count_rect.bottomright = missile_image_rect.bottomright
    screen.blit(missile_count_text, missile_count_rect)

    # Position the nuke below the blitted text
    nuke_image_rect = nuke_image_scaled.get_rect()

    if align == 'left':
        nuke_image_rect.bottomleft = (missile_image_rect.left, missile_image_rect.top - 20)
    elif align == 'right':
        nuke_image_rect.bottomright = (missile_image_rect.right, missile_image_rect.top - 20)

    # Blit the nuke onto the screen
    screen.blit(nuke_image_scaled, nuke_image_rect)

    # Display nuke count on the bottom right of the nuke image
    nuke_count_text = font1.render(str(nuke_count), True, font_color)
    nuke_count_rect = nuke_count_text.get_rect()
    nuke_count_rect.bottomright = nuke_image_rect.bottomright
    screen.blit(nuke_count_text, nuke_count_rect)

def render_all():
    global current_symbol
    # Rendering power-up values
    render_icons("Team 1", 20, 20, team1["nuke"], team1["missile"], symbol1_image_scaled, symbol3_image_scaled,
                 align='left')
    render_icons("Team 2", screen_width - 20, 20, team2["nuke"], team2["missile"], symbol2_image_scaled,
                 symbol4_image_scaled, align='right')
    render_place_mode(current_symbol)

def event_handle():
    global turn_count, place_mode, current_symbol
    if turn_count % 15 == 0:
        team1["missile"] += 1
    elif turn_count % 16 == 0:
        team2["missile"] += 1
    if board_x <= mouse_x <= board_x + board_length and board_y <= mouse_y <= board_y + board_length:
        cell_col = int((mouse_x - board_x) // cell_length)
        cell_row = int((mouse_y - board_y) // cell_length)
        sub_board_x = board_x + cell_col * cell_length + (cell_length - sub_board_length) // 2
        sub_board_y = board_y + cell_row * cell_length + (cell_length - sub_board_length) // 2

        sub_cell_col = int(
            (mouse_x - board_x - cell_col * cell_length - (cell_length - sub_board_length) // 2) // sub_cell_length
        )
        sub_cell_row = int(
            (mouse_y - board_y - cell_row * cell_length - (cell_length - sub_board_length) // 2) // sub_cell_length
        )

        if place_mode == "Symbol" and event.button == 1:
            if (
                    0 <= sub_cell_col < 3
                    and 0 <= sub_cell_row < 3
                    and sub_cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] is None
                    and not sub_board_win[cell_row][cell_col]  # Check if sub-board is already won
                    and not check_board_win()
            ):
                if current_symbol == symbol1_image_scaled and (
                        previous_x_state[cell_row][cell_col] is None or previous_x_state[cell_row][
                    cell_col] != current_symbol or turn_x[cell_row][cell_col] + 4 < turn_count):
                    sub_cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] = symbol1_image_scaled
                    if check_subboard_win(cell_row, cell_col, sub_cell_row, sub_cell_col):
                        sub_board_win[cell_row][cell_col] = True
                    previous_x_state[cell_row][cell_col] = current_symbol
                    current_symbol = symbol2_image_scaled
                    turn_x[cell_row][cell_col] = turn_count
                    turn_count += 1

                elif current_symbol == symbol2_image_scaled and (
                        previous_y_state[cell_row][cell_col] is None or previous_y_state[cell_row][
                    cell_col] != current_symbol or turn_y[cell_row][cell_col] + 4 < turn_count):
                    sub_cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] = symbol2_image_scaled
                    if check_subboard_win(cell_row, cell_col, sub_cell_row, sub_cell_col):
                        sub_board_win[cell_row][cell_col] = True
                    previous_y_state[cell_row][cell_col] = current_symbol
                    current_symbol = symbol3_image_scaled
                    turn_y[cell_row][cell_col] = turn_count
                    turn_count += 1

                elif current_symbol == symbol3_image_scaled and (
                        previous_plus_state[cell_row][cell_col] is None or previous_plus_state[cell_row][
                    cell_col] != current_symbol or turn_plus[cell_row][cell_col] + 4 < turn_count):
                    sub_cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] = symbol3_image_scaled
                    if check_subboard_win(cell_row, cell_col, sub_cell_row, sub_cell_col):
                        sub_board_win[cell_row][cell_col] = True
                    previous_plus_state[cell_row][cell_col] = current_symbol
                    current_symbol = symbol4_image_scaled
                    turn_plus[cell_row][cell_col] = turn_count
                    turn_count += 1

                elif current_symbol == symbol4_image_scaled and (
                        previous_square_state[cell_row][cell_col] is None or previous_square_state[cell_row][
                    cell_col] != current_symbol or turn_square[cell_row][cell_col] + 4 < turn_count):
                    sub_cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] = symbol4_image_scaled
                    if check_subboard_win(cell_row, cell_col, sub_cell_row, sub_cell_col):
                        sub_board_win[cell_row][cell_col] = True
                    previous_square_state[cell_row][cell_col] = current_symbol
                    current_symbol = symbol1_image_scaled
                    turn_square[cell_row][cell_col] = turn_count
                    turn_count += 1


        else:
            if (
                    0 <= sub_cell_col < 3
                    and 0 <= sub_cell_row < 3
                    and sub_cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] is not None
                    and not sub_board_win[cell_row][cell_col]  # Check if sub-board is already won
                    and not check_board_win()
            ):
                if turn_count % 2 == 0:
                    if event.button == 3 and team2["nuke"] > 0:
                        for i in range(3):
                            for j in range(3):
                                sub_cell_states[cell_row][cell_col][i][j] = None
                        team2["nuke"] -= 1
                        current_symbol = change_symbol(current_symbol)
                        turn_count += 1
                        place_mode = "Symbol"
                    elif event.button == 1:
                        if team2["missile"] > 0:
                            sub_cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] = None
                            team2["missile"] -= 1
                            current_symbol = change_symbol(current_symbol)
                            turn_count += 1
                            place_mode = "Symbol"



                else:
                    if event.button == 3 and team1["nuke"] > 0:
                        for i in range(3):
                            for j in range(3):
                                sub_cell_states[cell_row][cell_col][i][j] = None
                        team1["nuke"] -= 1
                        current_symbol = change_symbol(current_symbol)
                        turn_count += 1
                        place_mode = "Symbol"
                    elif event.button == 1:
                        if team1["missile"] > 0:
                            sub_cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] = None
                            team1["missile"] -= 1
                            current_symbol = change_symbol(current_symbol)
                            turn_count += 1
                            place_mode = "Symbol"


# Checking for main board win
def check_board_win():
    # Check rows
    for row in range(3):
        if all(cell_states[row][col] in team1_mem for col in range(3)):
            return "team1"
        elif all(cell_states[row][col] in team2_mem for col in range(3)):
            return "team2"


    # Check columns
    for col in range(3):
        if all(cell_states[row][col] in team1_mem for row in range(3)):
            return "team1"
        elif all(cell_states[row][col] in team2_mem for row in range(3)):
            return "team2"

    # Check diagonals
    if (
        cell_states[0][0] in team1_mem and cell_states[1][1] in team1_mem and cell_states[2][2] in team1_mem
        or cell_states[0][2] in team1_mem and cell_states[1][1] in team1_mem and cell_states[2][0] in team1_mem
    ):
        return "team1"
    elif (
        cell_states[0][0] in team2_mem and cell_states[1][1] in team2_mem and cell_states[2][2] in team2_mem
        or cell_states[0][2] in team2_mem and cell_states[1][1] in team2_mem and cell_states[2][0] in team2_mem
    ):
        return "team2"
    return None

# Change symbol after using power up
def change_symbol(symbol):
    if symbol == symbol1_image_scaled:
        symbol = symbol2_image_scaled
    elif symbol == symbol2_image_scaled:
        symbol = symbol3_image_scaled
    elif symbol == symbol3_image_scaled:
        symbol = symbol4_image_scaled
    else:
        symbol = symbol1_image_scaled

    return symbol

# Checking if subboard has been won
def check_subboard_win(row, col, srow, scol):
    symbol = sub_cell_states[row][col][srow][scol]

    # Check rows
    if all(sub_cell_states[row][col][srow][i] == symbol for i in range(3)):
        if symbol == symbol1_image_scaled:
            cell_states[row][col] = "symbol1"
            team1["nuke"] += 1
        elif symbol == symbol2_image_scaled:
            cell_states[row][col] = "symbol2"
            team2["nuke"] += 1
        elif symbol == symbol3_image_scaled:
            cell_states[row][col] = "symbol3"
            team1["nuke"] += 1
        elif symbol == symbol4_image_scaled:
            cell_states[row][col] = "symbol4"
            team2["nuke"] += 1
        sub_board_win[row][col] = True
        return True

    # Check columns
    if all(sub_cell_states[row][col][i][scol] == symbol for i in range(3)):
        if symbol == symbol1_image_scaled:
            cell_states[row][col] = "symbol1"
            team1["nuke"] += 1
        elif symbol == symbol2_image_scaled:
            cell_states[row][col] = "symbol2"
            team2["nuke"] += 1
        elif symbol == symbol3_image_scaled:
            cell_states[row][col] = "symbol3"
            team1["nuke"] += 1
        elif symbol == symbol4_image_scaled:
            cell_states[row][col] = "symbol4"
            team2["nuke"] += 1
        sub_board_win[row][col] = True
        return True

    # Check diagonal from top-left to bottom-right
    if all(sub_cell_states[row][col][i][i] == symbol for i in range(3)):
        if symbol == symbol1_image_scaled:
            cell_states[row][col] = "symbol1"
            team1["nuke"] += 1
        elif symbol == symbol2_image_scaled:
            cell_states[row][col] = "symbol2"
            team2["nuke"] += 1
        elif symbol == symbol3_image_scaled:
            cell_states[row][col] = "symbol3"
            team1["nuke"] += 1
        elif symbol == symbol4_image_scaled:
            cell_states[row][col] = "symbol4"
            team2["nuke"] += 1
        sub_board_win[row][col] = True
        return True

    # Check diagonal from top-right to bottom-left
    if (
        sub_cell_states[row][col][0][2] == symbol
        and sub_cell_states[row][col][1][1] == symbol
        and sub_cell_states[row][col][2][0] == symbol
    ):
        if symbol == symbol1_image_scaled:
            cell_states[row][col] = "symbol1"
            team1["nuke"] += 1
        elif symbol == symbol2_image_scaled:
            cell_states[row][col] = "symbol2"
            team2["nuke"] += 1
        elif symbol == symbol3_image_scaled:
            cell_states[row][col] = "symbol3"
            team1["nuke"] += 1
        elif symbol == symbol4_image_scaled:
            cell_states[row][col] = "symbol4"
            team2["nuke"] += 1
        sub_board_win[row][col] = True
        return True

    return False

def sub_board_win_blit(cell_states):
    for cell_row in range(3):
        for cell_col in range(3):
            board_cell_x = board_x + cell_col * cell_length + (cell_length - sub_board_length) // 2
            board_cell_y = board_y + cell_row * cell_length + (cell_length - sub_board_length) // 2

            if cell_states[cell_row][cell_col] == "symbol1":
                screen.blit(symbol1_board_win, (board_cell_x, board_cell_y))
            elif cell_states[cell_row][cell_col] == "symbol2":
                screen.blit(symbol2_board_win, (board_cell_x, board_cell_y))
            elif cell_states[cell_row][cell_col] == "symbol3":
                screen.blit(symbol3_board_win, (board_cell_x, board_cell_y))
            elif cell_states[cell_row][cell_col] == "symbol4":
                screen.blit(symbol4_board_win, (board_cell_x, board_cell_y))


# Game Loop
while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()

    elif running == 0:
        menu_screen()

    elif running == 1:
        # Switch between place modes
        if event.type == KEYDOWN and event.key == K_SPACE:
            if place_mode == "Symbol":
                place_mode = "Powerup"
            else:
                place_mode = "Symbol"

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            event_handle()


        screen.fill(Background_Colour)

        # Calling draw_board function
        draw_board(board_x, board_y, board_length, cell_length, sub_board_length,
                   sub_cell_length, board_line_thickness, sub_cell_line_thickness)

        # Getting mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Getting board pos and highlighting
        board_pos(mouse_x, mouse_y, board_x, board_y, board_length, cell_length,
                  place_mode, sub_cell_states, sub_board_win)
        # Blitting Sub board win
        sub_board_win_blit(cell_states)

        # Check for main board win
        main_board_winner = check_board_win()
        if main_board_winner is not None:
           if main_board_winner == "team1":
                screen.blit(team1_win, (board_x, board_y))
           else:
                screen.blit(team2_win, (board_x, board_y))

        render_all()

    pygame.display.flip()

# Quitting Pygame
pygame.quit()
