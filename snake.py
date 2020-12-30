import pygame
import time
import os
import sys
import random
from pygame import mixer


print("\nHello From the Developer of this Game, Rishit.")
time.sleep(2)
print("\nREAD THE RULES DOCUMENTATION BEFORE PLAYING!")
time.sleep(2)

print("\n")
print("Choose Level:")
print("+> Easy (1)")
print("+> Medium (2)")
print("+> Hard (3)")

while True:
    difficulty = input("Enter Difficulty Level: ")
    if difficulty == "1":
        speed = 4
        break
    elif difficulty == "2":
        speed = 6
        break
    elif difficulty == "3":
        speed = 8
        break
    else:
        print("Choose from Above Options Only!")


# Initialise Game
pygame.init()
clock = pygame.time.Clock()
mixer.init()
mixer.music.load('bg.wav')
mixer.music.set_volume(150)
mixer.music.play(-1)

# Screen and Window Size:
screen_width = 800
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")
icon = pygame.image.load("snake_icon.ico")
pygame.display.set_icon(icon)

# Colors
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)

# Snake Editing
x1 = 350
y1 = 300
snake = pygame.Rect([x1, y1, 20, 20])

x1_change = 0
y1_change = 0

snake_size = 15

snk_list = []
snk_length = 1

# Snake Food
food_x = random.randint(30, screen_width - 40)
food_y = random.randint(30, screen_height - 40)
food_height = 15
food_width = 15

# Game State
game_over = True

# Game over
font = pygame.font.SysFont("freelansbold.tff", 72)

# Score Counter
score = 0
score_font = pygame.font.SysFont("chiller", 45)
score_over = pygame.font.SysFont("chiller", 80)
score_text_var = pygame.font.SysFont("freelansbold", 50)
high_score = pygame.font.SysFont("chiller", 45)

# High Score
if (not os.path.exists("database.txt")):
    with open("database.txt", 'w') as f:
        f.write(str(0))
with open('database.txt', 'r') as f:
    database = f.read()


# TO INCREASE SNAKE LENGTH LOGIC:
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def score_over1():
    text = score_font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, [screen_width//2 - 50, screen_height//2 + 90])


def score_text():
    text = score_text_var.render("Your Score Was:", True, blue)
    screen.blit(text, [screen_width//2 - 120, screen_height//2 + 30])


def game_over_text(text, color):
    x = font.render(text, True, (240, 0, 0))
    screen.blit(x, [screen_width//2 - 150, screen_height//2 - 100])


def score_show():
    text = score_font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (20, 10))


def highscore():
    text = high_score.render("HighScore: " + str(database), True, white)
    screen.blit(text, (600, 10))


def game_over_():
    global game_over
    if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
        with open("database.txt", "w") as f:
            f.write(str(database))
        mixer.music.load('game_over.wav')
        mixer.music.play()
        game_over = False


def snake_collide():
    global food_x, food_y, snk_length, speed, score, database
    snake_rect = pygame.Rect(x1, y1, snake_size, snake_size)
    food_rect = pygame.Rect(food_x, food_y, snake_size, snake_size)

    if snake_rect.colliderect(food_rect):
        snk_length += 5
        score += 1
        food_x = random.randint(30, screen_width - 40)
        food_y = random.randint(30, screen_height - 40)
        mixer.music.load('food.wav')
        mixer.music.play()
        speed += 0.1
        if score > int(float(database)):
            database = score


def snake_draw():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, white, [x1, y1, 15, 15])
    pygame.draw.rect(screen, red, [food_x, food_y, food_width, food_height])
    score_show()
    highscore()

def main_loop():
    global x1, y1, x1_change, y1_change, game_over, food_x, food_y, score, speed, snk_list, snake_size, snk_length
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # User Input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x1_change = -speed
                y1_change = 0
            elif event.key == pygame.K_d:
                x1_change = speed
                y1_change = 0
            elif event.key == pygame.K_w:
                y1_change = -speed
                x1_change = 0
            elif event.key == pygame.K_s:
                y1_change = speed
                x1_change = 0

    x1 += x1_change
    y1 += y1_change

    # Game Over Checking
    game_over_()
    # Body Collision Check
    head = [x1, y1]

    if head in snk_list[:-1]:
        mixer.music.load('game_over.wav')
        mixer.music.play()
        game_over = False

    # Drawing On Screen
    snake_draw()
    pygame.display.flip()

    # Collision
    snake_collide()

    # SNAKE LENGTH LOGIC
    snk_list.insert(0, [x1, y1])
    if len(snk_list) > snk_length:
        del snk_list[-1]

    plot_snake(screen, white, snk_list, snake_size)

    # Final Initialisation
    pygame.display.flip()
    clock.tick(70)


# Main Game Loop
while game_over:
    main_loop()


# Game_Over
screen.fill((0, 0, 0))
game_over_text("Game Over !!!", (255, 0, 0))
score_text()
score_over1()
pygame.display.flip()
time.sleep(5)
pygame.quit()
sys.exit()
