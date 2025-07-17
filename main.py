
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
WINNING_SCORE = 6

def draw_centered_text(screen, text, font, y):
    surface = font.render(text, True, COLOR_WHITE)
    rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y))
    screen.blit(surface, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

    bounce_sound = pygame.mixer.Sound('bounce.wav')
    score_sound = pygame.mixer.Sound('score.wav')
    font = pygame.font.SysFont('Consolas', 40)
    big_font = pygame.font.SysFont('Consolas', 60)

    # Start screen
    selected_mode = 0
    selecting_mode = True
    difficulty = 0
    selecting_difficulty = False
    started = False
    single_player = False
    ai_level = "easy"

    while selecting_mode:
        screen.fill(COLOR_BLACK)
        draw_centered_text(screen, "PONG!!!", big_font, 200)
        draw_centered_text(screen, "Press SPACE to Start", font, 300)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                selecting_mode = False

    # Mode selection
    while not started and not selecting_difficulty:
        screen.fill(COLOR_BLACK)
        options = ["Single Player", "Multiplayer"]
        for i, text in enumerate(options):
            prefix = "-> " if i == selected_mode else "   "
            draw_centered_text(screen, prefix + text, font, 300 + i * 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_mode = (selected_mode - 1) % 2
                elif event.key == pygame.K_DOWN:
                    selected_mode = (selected_mode + 1) % 2
                elif event.key == pygame.K_RETURN:
                    if selected_mode == 0:
                        single_player = True
                        selecting_difficulty = True
                    else:
                        started = True

    # Difficulty selection if single player
    while selecting_difficulty:
        screen.fill(COLOR_BLACK)
        options = ["Easy", "Medium", "Hard"]
        for i, text in enumerate(options):
            prefix = "-> " if i == difficulty else "   "
            draw_centered_text(screen, prefix + text, font, 300 + i * 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    difficulty = (difficulty - 1) % 3
                elif event.key == pygame.K_DOWN:
                    difficulty = (difficulty + 1) % 3
                elif event.key == pygame.K_RETURN:
                    ai_level = ["easy", "medium", "hard"][difficulty]
                    selecting_difficulty = False
                    started = True


    # Game setup
    paddle_1 = pygame.Rect(30, SCREEN_HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle_2 = pygame.Rect(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle_1_move = 0
    paddle_2_move = 0

    ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)
    ball_speed_x = random.choice([-0.45, 0.45])
    ball_speed_y = random.choice([-0.45, 0.45])

    max_speed = 0.65 if not single_player else {"easy": 0.45, "medium": 0.6, "hard": 0.8}[ai_level]
    score_1 = 0
    score_2 = 0
    bounce_counter = 0
    started = False

    while True:
        delta_time = clock.tick(60)
        screen.fill(COLOR_BLACK)

        if not started:
            draw_centered_text(screen, "Press SPACE to Start", font, SCREEN_HEIGHT // 2)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    started = True
            continue

        ball.x += ball_speed_x * delta_time
        ball.y += ball_speed_y * delta_time

        # Bounce off top/bottom
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed_y *= -1
            bounce_sound.play()

        # Paddle collisions
        if paddle_1.colliderect(ball) and ball_speed_x < 0:
            ball_speed_x *= -1
            bounce_counter += 1
            bounce_sound.play()
        if paddle_2.colliderect(ball) and ball_speed_x > 0:
            ball_speed_x *= -1
            bounce_counter += 1
            bounce_sound.play()

        # Determine settings based on mode/difficulty
        if single_player:
            if ai_level == "easy":
                bounce_limit = 2
                increase_percent = 1.08
            elif ai_level == "medium":
                bounce_limit = 1
                increase_percent = 1.10
            else:  # hard
                bounce_limit = 1
                increase_percent = 1.12
        else:
            bounce_limit = 2
            increase_percent = 1.12

        # Gradually increase speed
        if bounce_counter and bounce_counter % bounce_limit == 0:
            if abs(ball_speed_x) < max_speed:
                ball_speed_x *= increase_percent
            if abs(ball_speed_y) < max_speed:
                ball_speed_y *= increase_percent
            bounce_counter = 0


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
            ball_speed_x = random.choice([-0.45, 0.45])
            ball_speed_y = random.choice([-0.45, 0.45])

        if score_1 == WINNING_SCORE or score_2 == WINNING_SCORE:
            winner = "Player 1" if score_1 == WINNING_SCORE else "Player 2"
            draw_centered_text(screen, f"{winner} Wins!", font, SCREEN_HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(3000)
            return

        # Paddle movement
        paddle_1.y += paddle_1_move * delta_time
        if single_player:
            target_y = ball.centery
            speed = {"easy": 0.25, "medium": 0.30, "hard": 0.88}[ai_level] * delta_time
            if paddle_2.centery < target_y:
                paddle_2.y += speed
            elif paddle_2.centery > target_y:
                paddle_2.y -= speed
        else:
            paddle_2.y += paddle_2_move * delta_time

        # Clamp paddles
        paddle_1.top = max(0, min(paddle_1.top, SCREEN_HEIGHT - PADDLE_HEIGHT))
        paddle_2.top = max(0, min(paddle_2.top, SCREEN_HEIGHT - PADDLE_HEIGHT))

        # Input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    paddle_1_move = -0.5
                if event.key == pygame.K_s:
                    paddle_1_move = 0.5
                if not single_player:
                    if event.key == pygame.K_UP:
                        paddle_2_move = -0.5
                    if event.key == pygame.K_DOWN:
                        paddle_2_move = 0.5
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_s]:
                    paddle_1_move = 0
                if event.key in [pygame.K_UP, pygame.K_DOWN] and not single_player:
                    paddle_2_move = 0

        # Drawing
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2)
        pygame.draw.ellipse(screen, COLOR_WHITE, ball)
        score_text = font.render(f"{score_1}   {score_2}", True, COLOR_WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 50, 20))
        pygame.display.update()

if __name__ == "__main__":
    main()



# HOW AND WHERE TO CHANGE SPEEDS OF BALL OR PADLES : 
# # AI PADDLE SPEED (harder AI = higher speed)
# # Located inside the main game loop → AI paddle control block
# speed = {
#     "easy": 0.25,    # AI paddle slow
#     "medium": 0.35,  # AI paddle normal
#     "hard": 0.6      #  increase this to make AI react faster
# }[ai_level] * delta_time


# # BALL SPEED INCREASE SETTINGS (how often & how much the ball gets faster)
# # Place this inside your game loop after paddle collision checks

# # Set bounce frequency & speed multiplier based on mode
# if single_player:
#     if ai_level == "easy":
#         bounce_limit = 3      # speed up every 3 paddle hits
#         increase_percent = 1.05  # 5% faster each time
#     elif ai_level == "medium":
#         bounce_limit = 2
#         increase_percent = 1.06
#     else:  # hard
#         bounce_limit = 1
#         increase_percent = 1.07
# else:
#     bounce_limit = 2
#     increase_percent = 1.08  # multiplayer gets faster too

# # Apply speed increase
# if bounce_counter and bounce_counter % bounce_limit == 0:
#     if abs(ball_speed_x) < max_speed:
#         ball_speed_x *= increase_percent
#     if abs(ball_speed_y) < max_speed:
#         ball_speed_y *= increase_percent
#     bounce_counter = 0


# # MAX BALL SPEED SETTING (limit top speed based on mode)
# # Set once before game loop
# max_speed = {
#     "easy": 0.4,
#     "medium": 0.45,
#     "hard": 0.55
# }[ai_level] if single_player else 0.5
