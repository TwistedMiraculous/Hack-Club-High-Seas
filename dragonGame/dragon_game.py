import pygame
import time
import random

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dragon Game')

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 35)

# Load assets
eat_sound = pygame.mixer.Sound('eat_sound.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')
dragon_img = pygame.image.load('dragon.png')  # Replace with your dragon image
food_img = pygame.image.load('food.png')  # Replace with your food image

# Game variables
UP, DOWN, LEFT, RIGHT = 'UP', 'DOWN', 'LEFT', 'RIGHT'
dragon_pos = [100, 50]
dragon_body = [[100, 50], [90, 50], [80, 50]]
direction = RIGHT
change_to = direction
score = 0

food_pos = [random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
            random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE]
food_spawn = True

obstacles = [[random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
              random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE] for _ in range(5)]

# Functions
def show_score():
    score_surface = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, [10, 10])

def game_over():
    pygame.mixer.Sound.play(game_over_sound)
    msg = font.render(f"Game Over! Your Score: {score}", True, RED)
    screen.blit(msg, [WIDTH // 4, HEIGHT // 3])
    pygame.display.flip()
    time.sleep(3)
    retry_game()

def retry_game():
    global dragon_pos, dragon_body, direction, change_to, score, food_spawn, food_pos, obstacles
    dragon_pos = [100, 50]
    dragon_body = [[100, 50], [90, 50], [80, 50]]
    direction = RIGHT
    change_to = direction
    score = 0
    food_spawn = True
    food_pos = [random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
                random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE]
    obstacles = [[random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
                  random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE] for _ in range(5)]

def move_dragon():
    global dragon_pos
    if direction == UP:
        dragon_pos[1] -= CELL_SIZE
    elif direction == DOWN:
        dragon_pos[1] += CELL_SIZE
    elif direction == LEFT:
        dragon_pos[0] -= CELL_SIZE
    elif direction == RIGHT:
        dragon_pos[0] += CELL_SIZE

def check_collision():
    global food_spawn, score, food_pos
    if dragon_pos == food_pos:
        pygame.mixer.Sound.play(eat_sound)
        score += 10
        food_spawn = False
    else:
        dragon_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
                    random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE]
    food_spawn = True

    if dragon_pos[0] < 0 or dragon_pos[0] >= WIDTH or dragon_pos[1] < 0 or dragon_pos[1] >= HEIGHT:
        game_over()

    for block in dragon_body[1:]:
        if dragon_pos == block:
            game_over()

    for obs in obstacles:
        if dragon_pos == obs:
            game_over()

def draw_game():
    screen.fill(BLACK)
    for pos in dragon_body:
        screen.blit(dragon_img, (pos[0], pos[1]))

    screen.blit(food_img, (food_pos[0], food_pos[1]))

    for obs in obstacles:
        pygame.draw.rect(screen, BLUE, pygame.Rect(obs[0], obs[1], CELL_SIZE, CELL_SIZE))

    show_score()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != DOWN:
                change_to = UP
            elif event.key == pygame.K_DOWN and direction != UP:
                change_to = DOWN
            elif event.key == pygame.K_LEFT and direction != RIGHT:
                change_to = LEFT
            elif event.key == pygame.K_RIGHT and direction != LEFT:
                change_to = RIGHT

    direction = change_to
    move_dragon()
    dragon_body.insert(0, list(dragon_pos))
    check_collision()
    draw_game()
    pygame.display.flip()
    clock.tick(10 + score // 10)  # Increase speed as score increases
