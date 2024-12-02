import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants for grid and blocks
GRID_WIDTH, GRID_HEIGHT = 10, 20  # Grid size in blocks
BLOCK_SIZE = 30  # Block size in pixels

# Calculate screen dimensions
PLAY_AREA_WIDTH = GRID_WIDTH * BLOCK_SIZE
PLAY_AREA_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
INFO_PANEL_WIDTH = 200  # Width for the score, level, and preview
SCREEN_WIDTH = PLAY_AREA_WIDTH + INFO_PANEL_WIDTH
SCREEN_HEIGHT = PLAY_AREA_HEIGHT
pygame.mixer.music.load('tetris_theme.mp3')
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely
FPS = 60

# Colors
COLORS = [
    (0, 0, 0),     # Background
    (255, 255, 0),   # Yellow
    (255, 165, 0),   # Orange
    (128, 0, 128),   # Purple
    (0, 255, 255),   # Cyan
    (0, 255, 0),     # Green
    (255, 0, 0),     # Red
    (100, 100, 100)  # Grid lines
]

# Shapes (Tetris blocks)
SHAPES = [
    [[1, 1, 1, 1]],                         # I
    [[1, 1], [1, 1]],                       # O
    [[0, 1, 0], [1, 1, 1]],                 # T
    [[1, 1, 0], [0, 1, 1]],                 # S
    [[0, 1, 1], [1, 1, 0]],                 # Z
    [[1, 1, 1], [1, 0, 0]],                 # L
    [[1, 1, 1], [0, 0, 1]],                 # J
]

# Fonts
TITLE_FONT = pygame.font.Font('tetris-font.ttf', 48)
MENU_FONT = pygame.font.Font('tetris-font.ttf', 32)
INFO_FONT = pygame.font.Font('tetris-font.ttf', 24)


BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
BUTTON_COLOR = (0, 0, 0)  # Black
BUTTON_TEXT_COLOR = (255, 255, 255)  # White
BUTTON_FONT = pygame.font.Font('tetris-font.ttf', 24)

# Button positions
PAUSE_BUTTON_POS = (PLAY_AREA_WIDTH + 50, 400)
RESTART_BUTTON_POS = (PLAY_AREA_WIDTH + 50, 450)






def draw_grid(surface):
    """Draw a background grid on the game screen."""
    for x in range(0, PLAY_AREA_WIDTH, BLOCK_SIZE):
        pygame.draw.line(surface, COLORS[7], (x, 0), (x, PLAY_AREA_HEIGHT))
    for y in range(0, PLAY_AREA_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(surface, COLORS[7], (0, y), (PLAY_AREA_WIDTH, y))

def draw_neon_block(surface, color, rect):
    neon_color = (255, 255, 255)  # White neon effect
    pygame.draw.rect(surface, neon_color, rect.inflate(4, 4), border_radius=5)
    pygame.draw.rect(surface, color, rect, border_radius=5)

def draw_text(surface, text, font, color, pos):
    """Helper function to draw text."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=pos)
    surface.blit(text_obj, text_rect)

def draw_button(surface, text, font, color, rect, border_radius=5):
    """Helper function to draw buttons."""
    pygame.draw.rect(surface, color, rect, border_radius)
    draw_text(surface, text, font, (255, 255, 255), rect.center)

def draw_pause_button(surface):
    """Draw the pause button."""
    button = pygame.Rect(PAUSE_BUTTON_POS[0], PAUSE_BUTTON_POS[1], BUTTON_WIDTH, BUTTON_HEIGHT)
    draw_button(surface, 'Pause', BUTTON_FONT, BUTTON_COLOR, button)

def draw_restart_button(surface):
    """Draw the restart button."""
    button = pygame.Rect(RESTART_BUTTON_POS[0], RESTART_BUTTON_POS[1], BUTTON_WIDTH, BUTTON_HEIGHT)
    draw_button(surface, 'Restart', BUTTON_FONT, BUTTON_COLOR, button)

def pause_game(game):
    """Pause the game."""
    game.paused = True

def main_menu():
    """Display the main menu with buttons."""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')

    while True:
        screen.fill((0, 0, 0))
        draw_text(screen, 'TETRIS', TITLE_FONT, (255, 255, 255), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))

        # Create Buttons
        start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        draw_button(screen, 'Start Game', MENU_FONT, (0, 0, 255), start_button)

        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50)
        draw_button(screen, 'Exit', MENU_FONT, (255, 0, 0), exit_button)
 

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if start_button.collidepoint(event.pos):
                        main_game()
                    elif exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

def game_over_screen():
    """Display the Game Over screen with restart and exit buttons."""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')

    while True:
        screen.fill((0, 0, 0))
        draw_text(screen, 'GAME OVER', TITLE_FONT, (255, 0, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

        # Create Buttons
        restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        draw_button(screen, 'Restart', MENU_FONT, (0, 255, 0), restart_button)

        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50)
        draw_button(screen, 'Exit', MENU_FONT, (255, 0, 0), exit_button)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if restart_button.collidepoint(event.pos):
                        main_game()
                    elif exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

def rotate(shape):
    """Rotate a shape clockwise."""
    return [list(row) for row in zip(*shape[::-1])]

def check_collision(grid, shape, offset):
    """Check if the current shape collides with the grid."""
    x_off, y_off = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + x_off < 0 or x + x_off >= GRID_WIDTH or y + y_off >= GRID_HEIGHT:
                    return True
                if y + y_off >= 0 and grid[y + y_off][x + x_off]:
                    return True
    return False

def clear_lines(grid):
    """Clear completed lines and return the number of lines cleared."""
    lines = 0
    for i in range(GRID_HEIGHT):
        if all(grid[i]):
            del grid[i]
            grid.insert(0, [0] * GRID_WIDTH)
            lines += 1
    return lines

def handle_buttons(game, event):
    """Handle button clicks for Pause and Restart."""
    pause_button = pygame.Rect(PAUSE_BUTTON_POS[0], PAUSE_BUTTON_POS[1], BUTTON_WIDTH, BUTTON_HEIGHT)
    restart_button = pygame.Rect(RESTART_BUTTON_POS[0], RESTART_BUTTON_POS[1], BUTTON_WIDTH, BUTTON_HEIGHT)

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
        if pause_button.collidepoint(event.pos):
            game.paused = not game.paused  # Toggle pause state
        elif restart_button.collidepoint(event.pos):
            game.__init__(game.screen)  # Restart the game


def new_board():
    """Create a new empty grid."""
    return [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

class Tetris:
    def __init__(self, screen):
        self.screen = screen
        self.grid = new_board()
        self.score = 0
        self.level = 1
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.piece_pos = [GRID_WIDTH // 2 - len(self.current_piece[0]) // 2, 0]
        self.game_over = False
        self.drop_speed = 500  # Milliseconds per drop
        self.last_drop = pygame.time.get_ticks()
        self.paused = False

    def new_piece(self):
        """Generate a new random piece."""
        return random.choice(SHAPES), random.randint(1, len(COLORS) - 1)

    def drop(self):
        """Drop the current piece by one row."""
        self.piece_pos[1] += 1
        if check_collision(self.grid, self.current_piece[0], self.piece_pos):
            self.piece_pos[1] -= 1
            self.lock_piece()
            self.clear_lines_and_update()
            self.spawn_new_piece()

    def lock_piece(self):
        """Lock the current piece into the grid."""
        shape, color = self.current_piece
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y + self.piece_pos[1]][x + self.piece_pos[0]] = color

    def clear_lines_and_update(self):
        """Clear lines and update the score/level."""
        lines_cleared = clear_lines(self.grid)
        self.score += lines_cleared * 100
        self.level = 1 + self.score // 1000
        self.drop_speed = max(100, 500 - (self.level - 1) * 100)

    def spawn_new_piece(self):
        """Spawn a new piece and check for game over."""
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        self.piece_pos = [GRID_WIDTH // 2 - len(self.current_piece[0]) // 2, 0]
        if check_collision(self.grid, self.current_piece[0], self.piece_pos):
            self.game_over = True

    def rotate_piece(self):
        """Rotate the current piece."""
        self.current_piece = (rotate(self.current_piece[0]), self.current_piece[1])
        if check_collision(self.grid, self.current_piece[0], self.piece_pos):
            self.current_piece = (rotate(rotate(rotate(self.current_piece[0]))), self.current_piece[1])

    def move_piece(self, dx):
        """Move the current piece left or right."""
        self.piece_pos[0] += dx
        if check_collision(self.grid, self.current_piece[0], self.piece_pos):
            self.piece_pos[0] -= dx

    def update(self):
        """Update the game state."""
        if not self.game_over and not self.paused and pygame.time.get_ticks() - self.last_drop > self.drop_speed:
            self.drop()
            self.last_drop = pygame.time.get_ticks()

    def draw(self):
        """Draw the game."""
        self.screen.fill(COLORS[0])  # Clear screen
        draw_grid(self.screen)

        # Draw grid blocks
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    draw_neon_block(self.screen, COLORS[cell], rect)

        # Draw current piece
        shape, color = self.current_piece
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect((x + self.piece_pos[0]) * BLOCK_SIZE,
                                       (y + self.piece_pos[1]) * BLOCK_SIZE,
                                       BLOCK_SIZE, BLOCK_SIZE)
                    draw_neon_block(self.screen, COLORS[color], rect)

        # Draw next piece preview
        preview_x = PLAY_AREA_WIDTH + 20
        preview_y = 100
        draw_text(self.screen, 'Next:', INFO_FONT, (255, 255, 255), (preview_x + 80, 50))
        shape, color = self.next_piece
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(preview_x + x * BLOCK_SIZE, preview_y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    draw_neon_block(self.screen, COLORS[color], rect)

        # Draw score and level
        info_x = PLAY_AREA_WIDTH + 20
        draw_text(self.screen, f'Score: {self.score}', INFO_FONT, (255, 255, 255), (info_x + 80, 240))
        draw_text(self.screen, f'Level: {self.level}', INFO_FONT, (255, 255, 255), (info_x + 80, 280))

        # Display pause message if paused
        if self.paused:
            draw_text(self.screen, 'PAUSED', TITLE_FONT, (255, 255, 255), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))


def handle_game_over(self):
    """Handle game over logic to return to the main menu."""
    game_over_screen()
    self.game_over = True
    



def main_game():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()

    game = Tetris(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not game.paused and not game.game_over:
                    if event.key == pygame.K_LEFT:
                        game.move_piece(-1)
                    elif event.key == pygame.K_RIGHT:
                        game.move_piece(1)
                    elif event.key == pygame.K_DOWN:
                        game.drop()
                    elif event.key == pygame.K_UP:
                        game.rotate_piece()
                if event.key == pygame.K_p:  # Toggle pause with 'P'
                    game.paused = not game.paused
            # Handle button clicks
            handle_buttons(game, event)

        # Update the game state
        if not game.paused and not game.game_over:
            game.update()


        if game.game_over:
            handle_game_over(game)
            break


       

        # Draw everything
        game.draw()
        draw_pause_button(screen)
        draw_restart_button(screen)

        pygame.display.flip()
        clock.tick(FPS)



if __name__ == '__main__':
    main_menu()