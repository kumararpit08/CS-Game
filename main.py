import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jumping Character")

# Set up the clock for limiting the frame rate
clock = pygame.time.Clock()

# Character properties
character_width = 100
character_height = 100
character_x = 100
character_y = screen_height - character_height - 50
character_jump_force = 75
character_gravity = 20

# Load character animation frames
running_frames = []
jump_up_frame = pygame.image.load("jump_up.png")
jump_down_frame = pygame.image.load("jump_down.png")
jump_up = pygame.transform.scale(jump_up_frame, (character_width, character_height))
jump_down = pygame.transform.scale(jump_down_frame, (character_width, character_height))
for i in range(6):
    frame = pygame.image.load(f"run{i + 1}.png")
    frame = pygame.transform.scale(frame, (character_width, character_height))
    running_frames.append(frame)
character_index = 0
character_image = running_frames[character_index]

# Background properties
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
background_x = 0

# Duplicate the background image
background_image2 = background_image.copy()
background_x2 = screen_width

# Create the character rectangle
character_rect = character_image.get_rect(topleft=(character_x, character_y))

# Variables to track the character's jump state and jump limit
is_jumping = False
jump_count = 0
jump_limit = 2

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check for jump input
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not is_jumping and jump_limit > 0:
            is_jumping = True
            jump_count = character_jump_force
            jump_limit -= 1

    # Update character animation
    character_index += 1
    if character_index >= len(running_frames):
        character_index = 0
    character_image = running_frames[character_index]

    # Update character position
    if is_jumping:
        print(jump_count)
        character_y -= jump_count
        jump_count -= character_gravity
        character_image = jump_up
        if jump_count <= -15:
            is_jumping = False
            character_image = jump_down
    else:
        # Apply gravity when not jumping
        character_y += character_gravity

        # Prevent the character from falling below the ground
        if character_y > screen_height - character_height - 50:
            character_y = screen_height - character_height - 50
            jump_limit = 2  # Reset jump limit when character touches the ground

    # Update background position
    background_x -= 12
    background_x2 -= 12

    # Reset the positions when the backgrounds go off-screen
    if background_x <= -screen_width:
        background_x = screen_width
    if background_x2 <= -screen_width:
        background_x2 = screen_width

    # Draw the backgrounds and character
    screen.blit(background_image, (background_x, 0))
    screen.blit(background_image2, (background_x2, 0))
    screen.blit(character_image, (character_x, character_y))

    # Update the display
    pygame.display.flip()
    clock.tick(15)
