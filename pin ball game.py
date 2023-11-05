import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BRICK_WIDTH, BRICK_HEIGHT = 80, 30
BALL_SPEED = 5
PADDLE_SPEED = 10
BRICK_ROWS = 5
BRICK_COLUMNS = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Create the window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pinball Game")

# Clock for managing the frame rate
clock = pygame.time.Clock()

# Paddle
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x = BALL_SPEED * random.choice((1, -1))
ball_speed_y = BALL_SPEED * -1

# Bricks
bricks = []
for row in range(BRICK_ROWS):
    for column in range(BRICK_COLUMNS):
        brick = pygame.Rect(column * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

def draw_objects():
    win.fill(BLACK)
    pygame.draw.rect(win, BLUE, paddle)
    pygame.draw.ellipse(win, RED, ball)
    for brick in bricks:
        pygame.draw.rect(win, GREEN, brick)

def move_ball():
    global ball_speed_x, ball_speed_y

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x *= -1

    if ball.top <= 0:
        ball_speed_y *= -1

    if ball.colliderect(paddle) and ball_speed_y > 0:
        ball_speed_y *= -1

    if ball.bottom >= HEIGHT:
        return True

    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y *= -1
            break

    return False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += PADDLE_SPEED

    if move_ball():
        # Game over
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        win.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        break

    draw_objects()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
