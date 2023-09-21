import os
import pygame
import sys

pygame.init()

# Set the screen dimensions
screen_width = 800
screen_height = 600

# Create the Pygame window
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the frame rate (FPS)
clock = pygame.time.Clock()

# Specify the folder containing your images
image_folder = "assets\Images\Background\\bg_frames"  # Replace with the path to your image folder

# Create an empty list to store the loaded images
loaded_images = []

# Iterate through the files in the folder
for filename in os.listdir(image_folder):
    if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
        # Load the image using pygame.image.load() and add it to the list
        image_path = os.path.join(image_folder, filename)
        image = pygame.image.load(image_path)
        loaded_images.append(image)

# Initialize variables to keep track of the current image index
current_image_index = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))  # Fill the screen with a background color (e.g., black)

    # Blit (draw) the current image onto the screen
    current_image = loaded_images[current_image_index]
    screen.blit(current_image, (0, 0))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(15)

    # Change the current image index (looping back to the start if needed)
    current_image_index = (current_image_index + 1) % len(loaded_images)

pygame.quit()
sys.exit()
