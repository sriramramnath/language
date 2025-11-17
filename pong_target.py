# Pygame Pong - Target Implementation
# This is the target code we want LevLang to be able to generate.

import pygame
import random
import sys

# --- Initialization ---
pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60

PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_RADIUS = 10

# --- Display Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# --- Classes ---

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 7

    def move(self, up=True):
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        
        # Keep paddle on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def ai_move(self, ball):
        # Simple AI to track the ball
        if self.rect.centery < ball.rect.centery:
            self.rect.y += self.speed
        if self.rect.centery > ball.rect.centery:
            self.rect.y -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.speed_x = 7 * random.choice((1, -1))
        self.speed_y = 7 * random.choice((1, -1))

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def check_collision(self, paddles):
        # Top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1
        
        # Paddles
        for paddle in paddles:
            if self.rect.colliderect(paddle.rect):
                self.speed_x *= -1
                break

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_y *= random.choice((1, -1))
        self.speed_x *= random.choice((1, -1))

    def draw(self, surface):
        pygame.draw.ellipse(surface, WHITE, self.rect)

# --- Functions ---

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def draw_scores(surface, score1, score2):
    draw_text(surface, str(score1), 64, WIDTH // 4, 50)
    draw_text(surface, str(score2), 64, WIDTH * 3 // 4, 50)

def draw_divider(surface):
    for i in range(10, HEIGHT, 25): # Dashed line
        pygame.draw.rect(surface, WHITE, (WIDTH // 2 - 2, i, 4, 10))

# --- Main Game Loop ---

def main():
    player1 = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    player2 = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()
    
    paddles = [player1, player2]
    
    player1_score = 0
    player2_score = 0

    running = True
    while running:
        clock.tick(FPS)

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --- Player Movement ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1.move(up=True)
        if keys[pygame.K_s]:
            player1.move(up=False)
        
        # --- AI Movement ---
        player2.ai_move(ball)

        # --- Game Logic ---
        ball.move()
        ball.check_collision(paddles)

        # --- Scoring ---
        if ball.rect.left <= 0:
            player2_score += 1
            ball.reset()
        if ball.rect.right >= WIDTH:
            player1_score += 1
            ball.reset()

        # --- Drawing ---
        screen.fill(BLACK)
        draw_divider(screen)
        player1.draw(screen)
        player2.draw(screen)
        ball.draw(screen)
        draw_scores(screen, player1_score, player2_score)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
