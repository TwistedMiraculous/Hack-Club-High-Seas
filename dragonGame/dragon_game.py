import pygame
import time
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dragon Game')

clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 35)



# Dragon and food initialization
dragon_pos = [100, 50]
dragon_body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
change_to = direction
score = 0

food_pos = [random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
            random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE]
food_spawn = True


# Display Score
def show_score():
    score_surface = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, [10, 10])

#Game over
def game_over():
    msg = font.render(f"Game Over! Your Score: {score}", True, RED)
    screen.blit(msg, [WIDTH // 4, HEIGHT // 3])
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    quit()

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
    if direction == 'DOWN':
        dragon_pos[1] += CELL_SIZE
    if direction == 'LEFT':
        dragon_pos[0] -= CELL_SIZE
    if direction == 'RIGHT':
        dragon_pos[0] += CELL_SIZE

  # Snake body growing and food spawning
    dragon_body.insert(0, list(dragon_pos))
    if abs(dragon_pos[0] - food_pos[0]) < CELL_SIZE and abs(dragon_pos[1] - food_pos[1]) < CELL_SIZE:
        score += 10
        food_spawn = False
    else:
        dragon_body.pop()

    if not food_spawn:
        food_pos = [
            random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
            random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE,
        ]
    food_spawn = True


    # Game over conditions
    if dragon_pos[0] < 0 or dragon_pos[0] >= WIDTH or dragon_pos[1] < 0 or dragon_pos[1] >= HEIGHT:
        game_over()

    for block in dragon_body[1:]:
        if dragon_pos == block:
            game_over()

    # Drawing the screen
    screen.fill(BLACK)
    for pos in dragon_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

    show_score()
    pygame.display.flip()
    clock.tick(15)