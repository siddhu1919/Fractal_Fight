import pygame as pg
from pygame import mixer
import os
from players import Player


# ----------------------------------------------------------------------------------------#
# Initialising The Pygame Window
pg.init()
# Initialising The Mixer
mixer.init()

# ----------------------------------------------------------------------------------------#
# Screen Resolution
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 650
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Fractal Space")

# ----------------------------------------------------------------------------------------#
# Setting the frame rate (FPS)
clock = pg.time.Clock()
FPS = 60


# ----------------------------------------------------------------------------------------#
#     <----------Loading The Assets Before Starting The Game--------->
# Loading Game music and sfx
pg.mixer.music.load("assets\\Sfx\\Infiltrator.mp3")
pg.mixer.music.set_volume(1)
pg.mixer.music.play(-1,0.0,4000)

# round Sound
round1 = pg.mixer.Sound("assets\\Sfx\\round1.mp3")
round1.set_volume(1)

round2 = pg.mixer.Sound("assets\\Sfx\\round2.mp3")
round2.set_volume(1)

round3 = pg.mixer.Sound("assets\\Sfx\\round3.mp3")
round3.set_volume(1)

# Sword Sound
sword_sfx = pg.mixer.Sound("assets\\Sfx\\slash_sfx.mp3")
sword_sfx.set_volume(1)
# #Sword Sound
# sword_sfx = pg.mixer.Sound.load()

# Death Sound
death_sfx = pg.mixer.Sound("assets\\Sfx\\death_sfx.wav")
death_sfx.set_volume(1)

# Jump Sound
Jump_sfx = pg.mixer.Sound("assets\\Sfx\\Jump_sfx.wav")
Jump_sfx.set_volume(1)

p1_sfx_data = [sword_sfx, Jump_sfx]
p2_sfx_data = [sword_sfx, Jump_sfx]


# ----------------------------------------------------------------------------------------#

# Load the GIF Background Frame By Frame & specify the folder containing your images
image_folder = "assets\\Images\\Background\\bg_frames"

# Create an empty list to store the loaded images
loaded_images = []
# Iterate through the files in the folder
for filename in os.listdir(image_folder):
    if (
        filename.endswith(".png")
        or filename.endswith(".jpg")
        or filename.endswith(".jpeg")
    ):
        # Load the image using pygame.image.load() and add it to the list
        image_path = os.path.join(image_folder, filename)
        image = pg.image.load(image_path)
        loaded_images.append(image)

# Initialize variables to keep track of the current image index
current_image_index = 0

# ----------------------------------------------------------------------------------------#
# Loading Player-1 Sprite
p1_spritesheet = pg.image.load(
    "assets\\Images\\Player\\p1_spritesheet.png"
).convert_alpha()
p2_spritesheet = pg.image.load(
    "assets\\Images\\Enemy\\p2_spritesheet.png"
).convert_alpha()
p1_animation_steps = [8, 8, 6, 6, 6, 4, 4, 2, 2]
# 0: Idle , 1: Running , 2: Attack1 , 3:Attack2 , 4: Death , 5: TakeHit_white , 6: TakeHit2 , 7: Fall , 8: Jump
p2_animation_steps = [4, 8, 4, 4, 7, 3, 3, 2, 2]
# 0: Idle , 1: Running , 2: Attack1 , 3:Attack2 , 4: Death , 5: TakeHit_white , 6: TakeHit2 , 7: Fall , 8: Jump

# ----------------------------------------------------------------------------------------#
# Loading VS and Victory Images
VS_IMG = pg.image.load("assets\\Images\\Icon\\vs.png")
KO_IMG = pg.image.load("assets\\Images\\Icon\\ko.png")

# ----------------------------------------------------------------------------------------#
# Defining The colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Game Auxilary and Optonal Features
# Game Timer
counter = 3
count_now = pg.time.get_ticks()
# PLayers Score
SCORE = [0, 0]  # [P1_score,P2_score]
GAME_OVER = 0
GAME_OVER_PAUSE = 2000  # 2

# ----------------------------------------------------------------------------------------#
# Counting the number of round
ROUND_COUNT = 1

# ----------------------------------------------------------------------------------------#
# Defining Players Data
p1_size = 200
p1_scale = 3
p1_offset = [85, 67]
p1_data = [p1_size, p1_scale, p1_offset]
# --------------------------------------->
p2_size = 200
p2_scale = 3
p2_offset = [85, 71]
p2_data = [p2_size, p2_scale, p2_offset]


# ----------------------------------------------------------------------------------------#
# Creating Instance of the player -> 2
p1 = Player(
    1,
    250,
    420,
    False,
    p1_data,
    p1_spritesheet,
    p1_animation_steps,
    [sword_sfx, Jump_sfx],
)
p2 = Player(
    2,
    900,
    420,
    True,
    p2_data,
    p2_spritesheet,
    p2_animation_steps,
    [sword_sfx, Jump_sfx],
)  # Incomplete

# ----------------------------------------------------------------------------------------#
# Font Loading
counter_font = pg.font.Font("assets\\fonts\\turok.ttf", 200)
score_font = pg.font.Font("assets\\fonts\\turok.ttf", 45)
player_font = pg.font.Font("assets\\fonts\\turok.ttf", 50)
death_font = pg.font.Font("assets\\fonts\\turok.ttf", 198)
victory_font = pg.font.Font("assets\\fonts\\turok.ttf", 198)


# ----------------------------------------------------------------------------------------#
# Function to Draw Text
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# ----------------------------------------------------------------------------------------#
# Function for The Health Bars
def draw_health_bar(health, x, y):
    health_ratio = health / 100
    pg.draw.rect(screen, WHITE, (x - 2, y - 2, 405, 35))
    pg.draw.rect(screen, YELLOW, (x, y, 400, 30))
    pg.draw.rect(screen, RED, (x, y, 400 * health_ratio, 30))


# ----------------------------------------------------------------------------------------#
# BAckground Draw
def draw():
    global current_image_index
    # Clear the screen
    screen.fill((0, 0, 0))  # Fill the screen with a background color (e.g., black)

    # Blit (draw) the current image onto the screen
    current_image = loaded_images[current_image_index]
    # Scale the background image
    current_image = pg.transform.scale(current_image, (1300, 650))
    screen.blit(current_image, (0, 0))
    # Limit the frame rate for the background
    clock.tick(28)
    # Change the current image index (looping back to the start if needed)
    current_image_index = (current_image_index + 1) % len(loaded_images)
    # Drawing the Health Bars
    draw_health_bar(p1.health, 20, 20)
    draw_health_bar(p2.health, 880, 20)


# ----------------------------------------------------------------------------------------#


# ----------------------------------------------------------------------------------------#
# Original GameLoop
run = 1
while run:
    clock.tick(FPS)
    # Drawing Background
    draw()

    # Drawing Vs
    screen.blit(pg.transform.scale(VS_IMG, (250, 150)), (540, 40))
    draw_text("Player 1", player_font, YELLOW, 20, 51)  # Player 1 Name
    draw_text("Player 2", player_font, YELLOW, 1099, 51)  # Player 2 Name
    draw_text("Score " + str(SCORE[0]), score_font, WHITE, 260, 55)  # Player 2 Name
    draw_text("Score " + str(SCORE[1]), score_font, WHITE, 900, 55)  # Player 2 Name

    # Countdown Timer
    if counter <= 0:
        # PLayer MOvement Update
        p1.move(SCREEN_WIDTH, SCREEN_HEIGHT, p2, GAME_OVER)
        p2.move(SCREEN_WIDTH, SCREEN_HEIGHT, p1, GAME_OVER)
    else:
        # Displaying Counter Text
        draw_text(str(counter), counter_font, YELLOW, 570, 250)
        if (pg.time.get_ticks() - count_now) >= 1000:  # 1 sec
            counter -= 1
            count_now = pg.time.get_ticks()
            # print(counter)

    # Updating Player Animation
    p1.update_animation()
    p2.update_animation()
    # Drawing Players
    p1.draw(screen)
    p2.draw(screen)
    # Checking For The Game Over Condition
    if GAME_OVER == 0:
        # if player 1 dies
        if p1.alive == 0:
            SCORE[1] += 1
            GAME_OVER = 1
            ROUND_COUNT += 1

            game_over_time = pg.time.get_ticks()
            death_sfx.play()

        # if player 2 dies
        elif p2.alive == 0:
            SCORE[0] += 1
            GAME_OVER = 1
            ROUND_COUNT += 1

            death_sfx.play()
            game_over_time = pg.time.get_ticks()
    else:
        screen.blit(pg.transform.scale(KO_IMG, (700, 300)), (280, 200))
        if pg.time.get_ticks() - game_over_time > GAME_OVER_PAUSE:
            GAME_OVER = 0
            count_now = 3
            ROUND_COUNT = 1

            p1 = Player(
                1,
                250,
                420,
                False,
                p1_data,
                p1_spritesheet,
                p1_animation_steps,
                [sword_sfx, Jump_sfx],
            )
            p2 = Player(
                2,
                900,
                420,
                True,
                p2_data,
                p2_spritesheet,
                p2_animation_steps,
                [sword_sfx, Jump_sfx],
            )

    # Closing Game Event Handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = 0
    # Updating the display
    pg.display.update()
# Exiting the Game
pg.quit()
