import pygame
import time
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Colors for the checkered board and dragon
LIGHT_COLOR = (40, 40, 40)  # Dark Gray for checkered board background
DARK_COLOR = (20, 20, 20)   # Even darker for alternate grid cells
RED = (255, 69, 0)          # Tomato Red for food
CHINESE_RED = (205, 92, 92) # Chinese Red for the dragon's body
GOLD = (255, 215, 0)        # Gold for accents (head, spikes, etc.)
WHITE = (255, 255, 255)     # For text
BLACK = (0, 0, 0)           # For borders
ZIGZAG_RED = (178, 34, 34)  # Dark red for the zig-zag border

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dragon Game')

clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 35)

# Initialize pygame mixer for sound
pygame.mixer.init()

# Helper function to align positions to the grid
def align_to_grid(pos):
    return [pos[0] // CELL_SIZE * CELL_SIZE, pos[1] // CELL_SIZE * CELL_SIZE]

# Dragon and food initialization
def start_game():
    global dragon_pos, dragon_body, direction, change_to, score, food_pos, food_spawn
    try:
        # Load and play the background music
        pygame.mixer.music.load("DragonBack.wav")
        pygame.mixer.music.play(-1, 0.0)  # Loop indefinitely
    except pygame.error as e:
        print("Error loading music:", e)

    dragon_pos = align_to_grid([100, 50])
    dragon_body = [align_to_grid([100, 50]), align_to_grid([90, 50]), align_to_grid([80, 50])]
    direction = 'RIGHT'
    change_to = direction
    score = 0

    food_pos = generate_food_pos()
    food_spawn = True

# Display Score
def show_score():
    score_surface = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, [10, 10])

def game_over():
    pygame.mixer.music.stop()  # Stop the background music when game over
    fade_background()  # Gradually fade the background
    
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(200)  # Adjust transparency level
    screen.blit(overlay, (0, 0))
    
    # Game Over message
    game_over_text = font.render("GAME OVER", True, GOLD)
    score_text = font.render(f"Your Score: {score}", True, WHITE)
    prompt_text = pygame.font.SysFont("comicsansms", 25).render("Press ENTER to Play Again or ESC to Quit", True, WHITE)

    # Center the text
    screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 3))
    screen.blit(score_text, ((WIDTH - score_text.get_width()) // 2, HEIGHT // 2))
    screen.blit(prompt_text, ((WIDTH - prompt_text.get_width()) // 2, HEIGHT * 2 // 3))

    pygame.display.flip()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Restart game
                    start_game()  # Reset the game
                    return  # Exit game_over and resume the game loop
                elif event.key == pygame.K_ESCAPE:  # Quit game
                    pygame.quit()
                    quit()

# Draw checkered board with dark background
def draw_checkered_board():
    for row in range(HEIGHT // CELL_SIZE):
        for col in range(WIDTH // CELL_SIZE):
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(
                screen, 
                color, 
                pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
    # Draw the zig-zag red border
    draw_zigzag_border()

# Function to draw the zig-zag border around the screen
def draw_zigzag_border():
    # Define zig-zag pattern points along the edges
    for i in range(0, WIDTH, 20):
        if i % 40 == 0:
            pygame.draw.line(screen, ZIGZAG_RED, (i, 0), (i + 10, 20), 3)  # Top edge
            pygame.draw.line(screen, ZIGZAG_RED, (i, HEIGHT), (i + 10, HEIGHT - 20), 3)  # Bottom edge
        else:
            pygame.draw.line(screen, ZIGZAG_RED, (i, 0), (i - 10, 20), 3)  # Top edge
            pygame.draw.line(screen, ZIGZAG_RED, (i, HEIGHT), (i - 10, HEIGHT - 20), 3)  # Bottom edge

    for i in range(0, HEIGHT, 20):
        if i % 40 == 0:
            pygame.draw.line(screen, ZIGZAG_RED, (0, i), (20, i + 10), 3)  # Left edge
            pygame.draw.line(screen, ZIGZAG_RED, (WIDTH, i), (WIDTH - 20, i + 10), 3)  # Right edge
        else:
            pygame.draw.line(screen, ZIGZAG_RED, (0, i), (20, i - 10), 3)  # Left edge
            pygame.draw.line(screen, ZIGZAG_RED, (WIDTH, i), (WIDTH - 20, i - 10), 3)  # Right edge

def fade_background():
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BLACK)
    for alpha in range(0, 256, 5):  # Gradually increase opacity
        fade_surface.set_alpha(alpha)
        draw_checkered_board()  # Redraw the board to maintain the grid appearance
        for pos in dragon_body:
            pygame.draw.rect(screen, CHINESE_RED, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)  # Adjust speed of the fade

# Modify the drawing of the dragon's body to make it more dragon-like
def draw_dragon():
    for i, pos in enumerate(dragon_body):
        # Drawing dragon body with a red color scheme
        if i == 0:
            # Dragon head with Chinese Red and golden accents (like horns)
            pygame.draw.rect(screen, CHINESE_RED, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(screen, GOLD, (pos[0] + CELL_SIZE // 2, pos[1] + CELL_SIZE // 2), 5)  # Fire-like eyes (golden)
            pygame.draw.polygon(screen, GOLD, [(pos[0] + CELL_SIZE // 4, pos[1]),
                                               (pos[0] + CELL_SIZE // 2, pos[1] - CELL_SIZE // 4),  # Horn
                                               (pos[0] + CELL_SIZE * 3 // 4, pos[1])])  # Horn shape
        else:
            # Dragon body (scaled look)
            pygame.draw.rect(screen, CHINESE_RED, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))  # Red for body
            pygame.draw.rect(screen, (255, 69, 0), pygame.Rect(pos[0] + 4, pos[1] + 4, CELL_SIZE - 8, CELL_SIZE - 8))  # Gold scale effect
            
            if i == len(dragon_body) - 1:  # Tail part (spiky and curved)
                pygame.draw.polygon(screen, CHINESE_RED, [(pos[0] + CELL_SIZE // 2, pos[1] + CELL_SIZE),
                                                          (pos[0] + CELL_SIZE, pos[1] + CELL_SIZE),
                                                          (pos[0] + CELL_SIZE, pos[1] + CELL_SIZE // 2)])  # Curved tail end

# Generate a random food position within the grid (excluding the edges)
def generate_food_pos():
    # Ensure the food is not too close to the edges
    return align_to_grid([random.randrange(1, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                          random.randrange(1, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE])

# Initialize the game state
start_game()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    direction = change_to

    if direction == 'UP':
        dragon_pos[1] -= CELL_SIZE
    elif direction == 'DOWN':
        dragon_pos[1] += CELL_SIZE
    elif direction == 'LEFT':
        dragon_pos[0] -= CELL_SIZE
    elif direction == 'RIGHT':
        dragon_pos[0] += CELL_SIZE

    # Ensure dragon stays within the grid boundaries
    if dragon_pos[0] < 0 or dragon_pos[0] >= WIDTH - CELL_SIZE or dragon_pos[1] < 0 or dragon_pos[1] >= HEIGHT - CELL_SIZE:
        game_over()  # Game over if the dragon hits the edge

    # Snake body growing mechanism
    dragon_body.insert(0, list(dragon_pos))
    if dragon_pos == food_pos:
        score += 10
        food_spawn = False
    else:
        dragon_body.pop()

    if not food_spawn:
        food_pos = generate_food_pos()
    food_spawn = True
    screen.fill(BLACK)  # Black background
    draw_checkered_board()  # Draw the board
    draw_dragon()  # Draw the dragon
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))  # Draw food
    show_score()  # Show score
    pygame.display.update()  # Update screen

    if (dragon_pos[0] < 0 or dragon_pos[0] >= WIDTH or 
        dragon_pos[1] < 0 or dragon_pos[1] >= HEIGHT or 
        dragon_pos in dragon_body[1:]):
        game_over()  # Game over

    clock.tick(10)  # Speed of the game
