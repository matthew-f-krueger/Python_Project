# -*- coding: utf-8 -*-
"""
Completed on Sun Nov 10, 2024

@author: Matthew Krueger
"""

import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game with Power-Ups")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
PINK = (255, 105, 180)
PURPLE = (128, 0, 128)
ORANGE = (255, 140, 0)
CYAN = (0, 255, 255)

# Font
font = pygame.font.Font(None, 36)

# Paddle dimensions and positions
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball settings
BALL_SIZE = 20
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
initial_ball_speed = 2
ball_speed_x = initial_ball_speed * random.choice([-1, 1])
ball_speed_y = initial_ball_speed * random.choice([-1, 1])

# Game settings
paddle_speed = 7
clock = pygame.time.Clock()
max_points = 25
is_between_points = False  # Indicates the between-points phase
game_started = False  # Track if the game has started

# Score and Money
class Player:
    def __init__(self):
        self.score = 0
        self.money = 0
        self.paddle_speed = paddle_speed
        self.is_ready = False  # Indicates if player is ready to resume
        self.hits = 0  # Tracks ball hits for money calculation
        self.has_back_wall = False  # Tracks if the player has a back wall
        self.back_wall_hits = 0  # Counts hits on back wall

left_player = Player()
right_player = Player()

# Power-Ups
POWER_UPS = {
    "Speed Boost": {"cost": 10, "effect": lambda player: setattr(player, 'paddle_speed', player.paddle_speed + 3)},
    "Slow Opponent": {"cost": 15, "effect": lambda opponent: setattr(opponent, 'paddle_speed', max(opponent.paddle_speed - 3, 1))},
    "Buy a Point": {"cost": 20, "effect": lambda player: setattr(player, 'score', player.score + 1)},
    "Back Wall": {"cost": 25, "effect": lambda player: setattr(player, 'has_back_wall', True)},
}

# Draw Power-Ups
def draw_powerups():
    y = 150
    powerup_keys_left = ["1", "2", "3", "4"]
    powerup_keys_right = ["7", "8", "9", "0"]

    for i, (name, power) in enumerate(POWER_UPS.items()):
        left_text = font.render(f"{name} (${power['cost']}) - Press {powerup_keys_left[i]}", True, GREEN)
        right_text = font.render(f"{name} (${power['cost']}) - Press {powerup_keys_right[i]}", True, GREEN)
        screen.blit(left_text, (25, y))
        screen.blit(right_text, (WIDTH - 375, y))
        y += 40

# Reset ball and enter between-points phase
def reset_ball():
    global ball_speed_x, ball_speed_y, is_between_points
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = initial_ball_speed * random.choice([-1, 1])
    ball_speed_y = initial_ball_speed * random.choice([-1, 1])
    is_between_points = True  # Enter between-points phase

# Handle scoring and reset for between-points phase
def handle_score(scoring_player, opponent_player):
    scoring_player.score += 1
    scoring_player.money += 10  # $10 bonus for winning the point
    scoring_player.hits = opponent_player.hits = 0  # Reset hits
    reset_ball()

# Track if power-up is active
power_up_active = False  # Set to True when the power-up is purchased

# Draw the back wall with conditional coloring
def draw_back_wall():
    if not power_up_active:
        wall_color = RED
    else:
        wall_color = WHITE  # Change to your desired color when active
    pygame.draw.rect(screen, wall_color, (0, 0, WIDTH, 10))  # Adjust position and size as needed

# Update the power-up status in the buy_powerup function
def buy_powerup(player, opponent, powerup_name):
    global power_up_active
    if powerup_name in POWER_UPS and player.money >= POWER_UPS[powerup_name]["cost"]:
        player.money -= POWER_UPS[powerup_name]["cost"]
        POWER_UPS[powerup_name]["effect"](player if powerup_name != "Slow Opponent" else opponent)
        
        # Check if the purchased power-up should activate the wall effect
        if powerup_name == "Back Wall":  # Assuming "Back Wall" is the relevant power-up
            power_up_active = True

# Draw starting screen with animations and decorations
def draw_start_screen():
    screen.fill(BLACK)

    # Moving gradient effect in the background
    gradient_color = pygame.Color(255, 255, 255)
    gradient_color.hsva = ((pygame.time.get_ticks() // 10) % 360, 100, 100)
    screen.fill(gradient_color, rect=pygame.Rect(0, 0, WIDTH, HEIGHT))

    # Decorative fading lines
    for i in range(0, WIDTH, 40):
        fade_factor = (pygame.time.get_ticks() // 50) % 255  # Create a fading effect
        pygame.draw.line(screen, (fade_factor, fade_factor, fade_factor), (i, 0), (i, HEIGHT), 2)
    
    # Animated particles
    for _ in range(10):
        particle_x = random.randint(0, WIDTH)
        particle_y = random.randint(0, HEIGHT)
        pygame.draw.circle(screen, random.choice([GREEN, PINK, BLUE]), (particle_x, particle_y), random.randint(3, 6))

    # Fun decoration: stars floating across the screen
    for _ in range(5):  # Generate random stars
        star_x = random.randint(0, WIDTH)
        star_y = random.randint(0, HEIGHT)
        pygame.draw.circle(screen, WHITE, (star_x, star_y), random.randint(2, 4))  # Draw random stars
    
    # Fun pulsing circles
    for i in range(3):
        radius = (pygame.time.get_ticks() // 50 + i * 30) % 100 + 30
        pygame.draw.circle(screen, random.choice([PINK, PURPLE, YELLOW]), (WIDTH // 2, HEIGHT // 2), radius, 5)

    # Floating rectangles
    for _ in range(3):
        rect_x = random.randint(100, WIDTH - 100)
        rect_y = random.randint(100, HEIGHT - 100)
        rect_width = random.randint(50, 150)
        rect_height = random.randint(20, 50)
        pygame.draw.rect(screen, random.choice([RED, ORANGE, PURPLE]), (rect_x, rect_y, rect_width, rect_height))
    
    # Display random text for fun background shadow effect
    if pygame.time.get_ticks() % 1000 < 500:
        random_text = font.render("Press Enter to Start!", True, random.choice([WHITE, YELLOW, PINK]))
        screen.blit(random_text, (WIDTH // 2 - random_text.get_width() // 2, HEIGHT // 2 + 100))
    
    # Title and instructions
    title_text = font.render("Pong Game with Power-Ups", True, WHITE)
    instruction_text = font.render("Press Enter to Start", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    screen.blit(instruction_text, (WIDTH // 2 - 120, HEIGHT // 2 + 100))
    pygame.display.flip()  # Update the display
    clock.tick(20)  # Frame rate to control animation speed

# Draw shop with refined decorations and animations
def draw_shop():
    screen.fill((25, 25, 25))  # Subtle dark gray background for a cleaner look

    # Score and money display with a subtle frame
    score_font = pygame.font.Font(None, 32)
    left_score_text = score_font.render(f"Score: {left_player.score}  Money: ${left_player.money}", True, (200, 200, 200))
    right_score_text = score_font.render(f"Score: {right_player.score}  Money: ${right_player.money}", True, (200, 200, 200))
    screen.blit(left_score_text, (50, HEIGHT - 100))
    screen.blit(right_score_text, (WIDTH - 280, HEIGHT - 100))

    # Ready-up text with animated pulsing effect
    pulse_value = abs(math.sin(pygame.time.get_ticks() / 500) * 100)
    left_ready_color = (255 - pulse_value if not left_player.is_ready else 0, pulse_value if left_player.is_ready else 0, 0)
    right_ready_color = (255 - pulse_value if not right_player.is_ready else 0, pulse_value if right_player.is_ready else 0, 0)
    left_ready_text = score_font.render("Left Player Ready (Press R)", True, left_ready_color)
    right_ready_text = score_font.render("Right Player Ready (Press L)", True, right_ready_color)
    screen.blit(left_ready_text, (25, HEIGHT - 50))
    screen.blit(right_ready_text, (WIDTH - 325, HEIGHT - 50))

    # Spotlight effect at the top
    spotlight_radius = 300 + int(abs(math.sin(pygame.time.get_ticks() / 800) * 50))
    pygame.draw.circle(screen, (35, 35, 50), (WIDTH // 2, 80), spotlight_radius)
 
    # Decorative background elements for a more immersive look
    for i in range(0, WIDTH, 60):  # Vertical line pattern
        pygame.draw.line(screen, (35, 35, 60), (i, 140), (i, HEIGHT - 150), 1)
    for j in range(0, HEIGHT, 60):  # Horizontal line pattern
        pygame.draw.line(screen, (35, 35, 60), (0, j), (WIDTH, j), 1)
        
    # Animated power-up slots with labels
    powerup_font = pygame.font.Font(None, 28)
    prices = ["$10", "$15", "$20", "$25"]  # Prices for each power-up
    purchase_keys = ["1/7", "2/8", "3/9", "4/0"]  # Purchase key labels for each power-up

    for i, (powerup, price, keys) in enumerate(zip(["Speed Boost", "Slow Opponent", "Buy a Point", "Back Wall"], prices, purchase_keys)):
        powerup_x = 35 + (i * 200)  # Position power-ups evenly across the screen
        powerup_text = powerup_font.render(powerup, True, (220, 220, 220))
        screen.blit(powerup_text, (powerup_x, 200))

        # Draw price tag with a bouncing effect
        price_tag_y = 240 + abs(math.sin(pygame.time.get_ticks() / 300 + i) * 5)
        price_text = powerup_font.render(price, True, (255, 215, 0))  # Golden price text
        pygame.draw.rect(screen, (50, 50, 50), (powerup_x - 10, price_tag_y - 10, 80, 30), border_radius=5)
        screen.blit(price_text, (powerup_x, price_tag_y))

        # Pulsing border around each power-up
        highlight_color = (100, 100, 255) if pygame.time.get_ticks() % 1000 < 500 else (150, 150, 255)
        pygame.draw.rect(screen, highlight_color, (powerup_x - 10, 190, 165, 80), 2, border_radius=8)

        # Draw purchase key label below each power-up with custom decoration and animation
        label_x = powerup_x + 50
        label_y = 300  # Positioned slightly lower

        # Animation effect for the label: slightly scales up and down
        scale_factor = 1.05 + 0.05 * math.sin(pygame.time.get_ticks() / 300 + i)  # Slight pulsing effect
        scaled_font = pygame.font.Font(None, int(30 * scale_factor))  # Slightly larger font with scaling
        scaled_label_text = scaled_font.render(f"Press {keys}", True, (220, 220, 220))

        # Custom decoration and border for label
        label_bg_rect = pygame.Rect(label_x - 50, label_y - 8, 120, 34)  # Increased size for decoration
        pygame.draw.rect(screen, (30, 30, 30), label_bg_rect, border_radius=6)  # Dark background
        pygame.draw.rect(screen, (100, 100, 255), label_bg_rect, 2, border_radius=6)  # Blue border

        # Render the animated label text onto the screen, centered within the label background
        text_x = label_x + 10 - scaled_label_text.get_width() // 2
        text_y = label_y + 10 - scaled_label_text.get_height() // 2
        screen.blit(scaled_label_text, (text_x, text_y))

    # Animated pulsing circles next to score label for both players
    pulse_radius = 5 + abs(math.sin(pygame.time.get_ticks() / 300) * 5)
    pygame.draw.circle(screen, (180, 180, 255), (35, HEIGHT - 90), int(pulse_radius), 1)
    pygame.draw.circle(screen, (180, 180, 255), (WIDTH - 295, HEIGHT - 90), int(pulse_radius), 1)

    # Title with a soft glow effect
    title_font = pygame.font.Font(None, 64)
    title_text = title_font.render("Power-Up Shop", True, (180, 180, 255))
    
    # Draw the glow layers with varying colors based on glow_size
    for glow_size in range(1, 5):
        glow_color = (180 - glow_size * 10, 180 - glow_size * 10, 255 - glow_size * 20)  # Adjusted glow color
        glow_text = title_font.render("Power-Up Shop", True, glow_color)  # Render title with adjusted glow color
        screen.blit(glow_text, (WIDTH // 2 - 140 - glow_size, 40 - glow_size))
    
    # Decorative dividers
    pygame.draw.line(screen, (80, 80, 80), (0, 140), (WIDTH, 140), 3)  # Divider line below the title
    pygame.draw.line(screen, (80, 80, 80), (0, HEIGHT - 150), (WIDTH, HEIGHT - 150), 3)  # Divider above scores

    # Draw the main title text on top
    screen.blit(title_text, (WIDTH // 2 - 140, 40))
    
    pygame.display.flip()  # Update the display
    clock.tick(60)  # Frame rate control

# Function to create a random gradient background
def random_gradient():
    color1 = random.choice([RED, GREEN, BLUE, CYAN])
    color2 = random.choice([RED, GREEN, BLUE, CYAN])
    return color1, color2

# Function to draw a smooth gradient from top to bottom
def draw_gradient(color1, color2):
    for y in range(HEIGHT):
        # Calculate the blend factor (how much color1 vs color2 to use)
        blend_factor = y / HEIGHT
        r = int(color1[0] * (1 - blend_factor) + color2[0] * blend_factor)
        g = int(color1[1] * (1 - blend_factor) + color2[1] * blend_factor)
        b = int(color1[2] * (1 - blend_factor) + color2[2] * blend_factor)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

# Function to create a border effect around the screen
def draw_border():
    border_thickness = 10
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), border_thickness)

# Function to create flashing effect (once, not continuous)
def flash_text(text, x, y, speed=10):
    for i in range(speed):
        alpha = (i * 255) // speed  # Fade in and out effect
        text.set_alpha(alpha)
        # Only blit the flashing text, don't clear the screen
        screen.blit(text, (x, y))
        pygame.display.flip()
        clock.tick(60)

def draw_border_with_fading_effect():
    glow_color = (255, 255, 255)  # White border color
    fade_layers = 20  # Number of layers for the fade effect

    # Draw progressively smaller rectangles with decreasing opacity
    for i in range(fade_layers):
        alpha_value = max(255 - i * 10, 0)  # Decrease opacity as it moves inward
        fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Surface with transparency

        # Only draw the border region, leaving the center untouched
        pygame.draw.rect(
            fade_surface,
            (glow_color[0], glow_color[1], glow_color[2], alpha_value),
            (i, i, WIDTH - 2 * i, HEIGHT - 2 * i),
            1  # Draw only the outline
        )

        # Apply the fading border surface to the screen
        screen.blit(fade_surface, (0, 0))

# Increase the font size
large_font = pygame.font.Font(None, 80)  # Larger font for the winner text
normal_font = pygame.font.Font(None, 40)  # Smaller font for instructions

# Draw the Game Over screen with all visual effects and options
def game_over_screen(winner):
    screen.fill(BLACK)

    # Background gradient animation
    color1, color2 = random_gradient()
    draw_gradient(color1, color2)

    # Add a moving background effect (circles)
    for i in range(5):
        pygame.draw.circle(screen, random.choice([RED, GREEN, BLUE, CYAN]), (random.randint(0, WIDTH), random.randint(0, HEIGHT)), random.randint(30, 60))

    # Add cool effect: Flashing stars
    for i in range(10):
        pygame.draw.circle(screen, random.choice([WHITE, YELLOW]), (random.randint(0, WIDTH), random.randint(0, HEIGHT)), random.randint(2, 5))

    # Draw the border with some glow effect
    draw_border_with_fading_effect()

    # Display winner message with black outline and white text
    winner_text = large_font.render(f"{winner} Player Won!", True, WHITE)
    winner_text_black = large_font.render(f"{winner} Player Won!", True, BLACK)
    # Draw the black outline (slightly offset)
    screen.blit(winner_text_black, (WIDTH // 2 - winner_text.get_width() // 2 - 5, HEIGHT // 2 - 150 - 5))  # Black outline
    # Draw the white text over it
    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 150))  # White text

    # Instructions for replay or going to homepage
    replay_text = normal_font.render("Press 6 to Play Again", True, WHITE)
    homepage_text = normal_font.render("Press 5 to Go to Homepage", True, WHITE)
    quit_text = normal_font.render("Press ESC to Quit", True, WHITE)

    # Draw the black outline for each instruction text
    replay_text_black = normal_font.render("Press 6 to Play Again", True, BLACK)
    homepage_text_black = normal_font.render("Press 5 to Go to Homepage", True, BLACK)
    quit_text_black = normal_font.render("Press ESC to Quit", True, BLACK)

    # Draw the black outlines (slightly offset)
    screen.blit(replay_text_black, (WIDTH // 2 - replay_text.get_width() // 2 - 3, HEIGHT // 2 + 50 - 3))
    screen.blit(homepage_text_black, (WIDTH // 2 - homepage_text.get_width() // 2 - 3, HEIGHT // 2 + 100 - 3))
    screen.blit(quit_text_black, (WIDTH // 2 - quit_text.get_width() // 2 - 3, HEIGHT // 2 + 150 - 3))

    # Then draw the white text on top of the black outlines
    screen.blit(replay_text, (WIDTH // 2 - replay_text.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(homepage_text, (WIDTH // 2 - homepage_text.get_width() // 2, HEIGHT // 2 + 100))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 150))

    # Apply a flashing effect for each option
    flash_text(replay_text, WIDTH // 2 - replay_text.get_width() // 2, HEIGHT // 2 + 50, speed=20)
    flash_text(homepage_text, WIDTH // 2 - homepage_text.get_width() // 2, HEIGHT // 2 + 100, speed=20)
    flash_text(quit_text, WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 150, speed=20)

    # Add rotating text effect (just an example)
    rotate_text = normal_font.render("Thanks for playing!", True, WHITE)
    rotated_text = pygame.transform.rotate(rotate_text, random.randint(0, 360))
    screen.blit(rotated_text, (WIDTH // 2 - rotated_text.get_width() // 2, HEIGHT // 2 + 200))

    pygame.display.flip()  # Update the display

    # Event loop for handling key presses, including ESC to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # Use sys.exit() instead of quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_5:  # Go to homepage
                return "home"
            elif event.key == pygame.K_6:  # Play again
                return "restart"
            elif event.key == pygame.K_ESCAPE:  # ESC to quit
                pygame.quit()
                sys.exit()  # Use sys.exit() instead of quit()

# Add a variable to track the elapsed time for ball speed increase
ball_speed_increase_interval = 1  # Increase speed every frame (very slightly)
frame_count = 0  # Frame counter to track the number of frames

def main():
    global is_between_points, ball_speed_x, ball_speed_y, game_started, frame_count
    game_over = False  # Track if the game is over
    winner = None  # To track the winner

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not game_started:
                    game_started = True

                # Check if the game is over and key pressed
                if game_over:
                    if event.key == pygame.K_5:  # Go to homepage
                        game_started = False
                        game_over = False
                        reset_game()  # Reset game state
                    elif event.key == pygame.K_6:  # Play again
                        game_started = True
                        game_over = False
                        reset_game()  # Reset game state

        if game_over:
            game_over_screen(winner)  # Pass the winner to the game over screen
        elif not game_started:
            draw_start_screen()  # Show start screen before the game starts
        else:
            if is_between_points:
                draw_shop()  # Show shop screen
                keys = pygame.key.get_pressed()

                # Left player power-up purchase keys (1-4)
                if keys[pygame.K_1]: buy_powerup(left_player, right_player, "Speed Boost")
                if keys[pygame.K_2]: buy_powerup(left_player, right_player, "Slow Opponent")
                if keys[pygame.K_3]: buy_powerup(left_player, right_player, "Buy a Point")
                if keys[pygame.K_4]: buy_powerup(left_player, right_player, "Back Wall")

                # Right player power-up purchase keys (7-0)
                if keys[pygame.K_7]: buy_powerup(right_player, left_player, "Speed Boost")
                if keys[pygame.K_8]: buy_powerup(right_player, left_player, "Slow Opponent")
                if keys[pygame.K_9]: buy_powerup(right_player, left_player, "Buy a Point")
                if keys[pygame.K_0]: buy_powerup(right_player, left_player, "Back Wall")

                if keys[pygame.K_r]: left_player.is_ready = True
                if keys[pygame.K_l]: right_player.is_ready = True

                if left_player.is_ready and right_player.is_ready:
                    is_between_points = False
                    left_player.is_ready = right_player.is_ready = False

            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] and left_paddle.top > 0:
                    left_paddle.y -= left_player.paddle_speed
                if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
                    left_paddle.y += left_player.paddle_speed
                if keys[pygame.K_UP] and right_paddle.top > 0:
                    right_paddle.y -= right_player.paddle_speed
                if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
                    right_paddle.y += right_player.paddle_speed

                ball.x += ball_speed_x
                ball.y += ball_speed_y

                if ball.top <= 0 or ball.bottom >= HEIGHT:
                    ball_speed_y *= -1

                # Paddle collision logic with bounce fix
                if ball.colliderect(left_paddle) and ball_speed_x < 0:
                    ball_speed_x = abs(ball_speed_x)
                    ball.x = left_paddle.right
                    left_player.hits += 1
                    left_player.money += 1

                elif ball.colliderect(right_paddle) and ball_speed_x > 0:
                    ball_speed_x = -abs(ball_speed_x)
                    ball.x = right_paddle.left - BALL_SIZE
                    right_player.hits += 1
                    right_player.money += 1

                # Back wall functionality for each player
                if left_player.has_back_wall and ball.left <= 0:
                    ball_speed_x = abs(ball_speed_x)
                    left_player.back_wall_hits += 1
                    if left_player.back_wall_hits >= 3:
                        left_player.has_back_wall = False
                        left_player.back_wall_hits = 0

                if right_player.has_back_wall and ball.right >= WIDTH:
                    ball_speed_x = -abs(ball_speed_x)
                    right_player.back_wall_hits += 1
                    if right_player.back_wall_hits >= 3:
                        right_player.has_back_wall = False
                        right_player.back_wall_hits = 0

                if ball.left <= 0 and not left_player.has_back_wall:
                    handle_score(right_player, left_player)
                elif ball.right >= WIDTH and not right_player.has_back_wall:
                    handle_score(left_player, right_player)

                # Check if either player has reached the max score
                if left_player.score >= max_points:
                    game_over = True
                    winner = "Left Player"
                elif right_player.score >= max_points:
                    game_over = True
                    winner = "Right Player"

                # Gradually increase the ball's speed every frame
                frame_count += 1
                if frame_count >= ball_speed_increase_interval:
                    ball_speed_x *= 1.001  # Increase speed by 0.1%
                    ball_speed_y *= 1.001  # Increase speed by 0.1%
                    frame_count = 0  # Reset frame counter

                # Draw elements
                screen.fill(BLACK)
                pygame.draw.rect(screen, WHITE, left_paddle)
                pygame.draw.rect(screen, WHITE, right_paddle)
                pygame.draw.ellipse(screen, WHITE, ball)

                # Draw back walls for players who have them
                if left_player.has_back_wall:
                    back_wall_color = GREEN if left_player.back_wall_hits == 0 else YELLOW if left_player.back_wall_hits == 1 else RED
                    pygame.draw.line(screen, back_wall_color, (5, 0), (5, HEIGHT), 5)
                if right_player.has_back_wall:
                    back_wall_color = GREEN if right_player.back_wall_hits == 0 else YELLOW if right_player.back_wall_hits == 1 else RED
                    pygame.draw.line(screen, back_wall_color, (WIDTH - 5, 0), (WIDTH - 5, HEIGHT), 5)

                left_score_text = font.render(f"Score: {left_player.score}  Money: ${left_player.money}", True, WHITE)
                right_score_text = font.render(f"Score: {right_player.score}  Money: ${right_player.money}", True, WHITE)
                screen.blit(left_score_text, (50, HEIGHT - 100))
                screen.blit(right_score_text, (WIDTH - 280, HEIGHT - 100))

                pygame.display.flip()
                clock.tick(60)  # Control frame rate

# Reset the game state after game over
def reset_game():
    global ball_speed_x, ball_speed_y, left_player, right_player
    left_player = Player()
    right_player = Player()
    reset_ball()
    
if __name__ == "__main__":
    main()
