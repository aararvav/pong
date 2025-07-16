
import pygame
import random

# Constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

PADDLE_WIDTH = 7
PADDLE_HEIGHT = 100
BALL_SIZE = 25
WINNING_SCORE = 5  # You can change this to whatever you want

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

    # Sound Effects
    bounce_sound = pygame.mixer.Sound('bounce.wav')
    score_sound = pygame.mixer.Sound('score.wav')

    started = False

    # Paddles
    paddle_1 = pygame.Rect(30, SCREEN_HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle_2 = pygame.Rect(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle_1_move = 0
    paddle_2_move = 0

    # Ball
    ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)
    ball_speed_x = random.choice([-0.3, 0.3])
    ball_speed_y = random.choice([-0.3, 0.3])

    # Scores
    score_1 = 0
    score_2 = 0
    font = pygame.font.SysFont('Consolas', 40)

    running = True
    while running:
        delta_time = clock.tick(60)
        screen.fill(COLOR_BLACK)

        if not started:
            text = font.render('Press Space to Start', True, COLOR_WHITE)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    started = True
            continue

        # Ball movement
        ball.x += ball_speed_x * delta_time
        ball.y += ball_speed_y * delta_time

        # Ball collision with top/bottom
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed_y *= -1
            bounce_sound.play()

        # Ball collision with paddles
        if paddle_1.colliderect(ball) and ball_speed_x < 0:
            ball_speed_x *= -1
            bounce_sound.play()
        if paddle_2.colliderect(ball) and ball_speed_x > 0:
            ball_speed_x *= -1
            bounce_sound.play()

        # Scoring
        if ball.left <= 0:
            score_2 += 1
            score_sound.play()
            started = False
            ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball_speed_x = random.choice([-0.3, 0.3])
            ball_speed_y = random.choice([-0.3, 0.3])

        if ball.right >= SCREEN_WIDTH:
            score_1 += 1
            score_sound.play()
            started = False
            ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball_speed_x = random.choice([-0.3, 0.3])
            ball_speed_y = random.choice([-0.3, 0.3])

        # Check win condition
        if score_1 == WINNING_SCORE or score_2 == WINNING_SCORE:
            winner = "Player 1" if score_1 == WINNING_SCORE else "Player 2"
            text = font.render(f"{winner} Wins!", True, COLOR_WHITE)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, rect)
            pygame.display.flip()
            pygame.time.delay(3000)
            return

        # Move paddles
        paddle_1.y += paddle_1_move * delta_time
        paddle_2.y += paddle_2_move * delta_time

        # Keep paddles on screen
        if paddle_1.top < 0:
            paddle_1.top = 0
        if paddle_1.bottom > SCREEN_HEIGHT:
            paddle_1.bottom = SCREEN_HEIGHT
        if paddle_2.top < 0:
            paddle_2.top = 0
        if paddle_2.bottom > SCREEN_HEIGHT:
            paddle_2.bottom = SCREEN_HEIGHT

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    paddle_1_move = -0.5
                if event.key == pygame.K_s:
                    paddle_1_move = 0.5
                if event.key == pygame.K_UP:
                    paddle_2_move = -0.5
                if event.key == pygame.K_DOWN:
                    paddle_2_move = 0.5

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_s]:
                    paddle_1_move = 0
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    paddle_2_move = 0

        # Draw
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2)
        pygame.draw.ellipse(screen, COLOR_WHITE, ball)

        score_text = font.render(f"{score_1}   {score_2}", True, COLOR_WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 50, 20))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
