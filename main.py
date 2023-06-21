#-----------------------------------------------------------------------------
# Name:        Interstellar Infinity
# Purpose:     Avoid incoming obstacles and achieve a high score
# Authors:     Hussain, Arpit, Aayan
# Beta Testers: Linus, Chris
# Created:     30-Mar-2023
# Updated:     8-Jun-2023
#-----------------------------------------------------------------------------

import pygame
import sys
import random
from obstacle import Obstacle


# Initialize Pygame
pygame.init()

# Game Music / Aayan
# https://www.youtube.com/watch?v=YQ1mixa9RAw
pygame.mixer.pre_init(44100,16,2,4096)
pygame.mixer.music.load("game music.mp3")
death_sound = pygame.mixer.Sound("death sound effect.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

# Set up the display window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jumping Character")

# Load the background image / Hussain
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Create a sprite group for obstacles
obstacles_group = pygame.sprite.Group()

# Set up the clock for limiting the frame rate
clock = pygame.time.Clock()

# Character properties / Arpit
character_width = 100
character_height = 100
character_x = 100
character_y = screen_height - character_height - 50
character_jump_force = 75
character_gravity = 13

# Set up the logo / Arpit
logo_image = pygame.image.load("Interstellar.png")  
logo_rect = logo_image.get_rect()
logo_rect.center = (screen_width / 2, screen_height / 2)

# Set up the timer for displaying the "Press any key to start" message
start_timer = pygame.time.get_ticks()

# Load character animation frames / Hussain and Arpit
# https://www.youtube.com/watch?v=nXOVcOBqFwM
running_frames = []
jump_up_frame = pygame.image.load("jump_up.png")
jump_down_frame = pygame.image.load("jump_down.png")
jump_up = pygame.transform.scale(jump_up_frame, (character_width, character_height))
jump_down = pygame.transform.scale(jump_down_frame, (character_width, character_height))

for i in range(6):
    frame = pygame.image.load(f"run{i + 1}.png")
    frame = pygame.transform.scale(frame, (character_width, character_height))
    running_frames.append(frame)

# Character sprite class / Arpit
# https://opensource.com/article/17/12/game-python-moving-player
class Character(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the Character sprite.

        The Character is a subclass of pygame.sprite.Sprite and represents
        the player-controlled character in the game.

        """
        super().__init__()

        # Set up the character animation frames
        self.running_frames = running_frames
        self.jump_up = jump_up
        self.jump_down = jump_down

        # Set the initial image and position of the character
        self.image = self.running_frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (character_x, character_y)

        # Character movement and jumping variables
        self.is_jumping = False
        self.jump_count = 0
        self.jump_limit = 4

    def update(self):
        """
        Update the character's animation and movement.

        This method is called in the game loop to update the character's
        animation and movement based on its current state.

        """
        self.animate()
        self.move()

    def animate(self):
        """
        Update the character's animation frame.

        This method is called to update the character's animation frame
        based on its current state.

        """
        if self.is_jumping:
            self.image = self.jump_up
        else:
            frame_index = (pygame.time.get_ticks() // 100) % len(self.running_frames)
            self.image = self.running_frames[frame_index]

    def move(self):
        """
        Move the character vertically.

        This method is called to move the character vertically based on its
        current state (jumping or falling).

        """
        if self.is_jumping:
            self.jump_count -= character_gravity
            self.rect.y -= self.jump_count

            if self.jump_count <= 0:
                self.is_jumping = False

        else:
            self.rect.y += character_gravity

            if self.rect.y >= screen_height - character_height - 50:
                self.rect.y = screen_height - character_height - 50
                self.jump_limit = 4

# Create character sprite object
character_sprite = Character()

# Game states
MENU = 0
RUNNING = 1
GAME_OVER = 2
current_state = MENU

# Game over screen properties / Aayan
# https://www.makeuseof.com/start-menu-and-game-over-screen-with-pygame/
game_over_font = pygame.font.Font(None, 100)
game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
game_over_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 2))

# Score variables
score = 0
high_score = 0
score_font = pygame.font.Font(None, 40)

# Background positions
background_x = 0
background_x2 = screen_width

# Flashing score effect variables
flash_time = 0
flash_duration = 500
flash_on = False

# Time variables
current_time = 0
last_score_time = 0

# 1 second
score_increase_interval = 1000  

# 60 seconds
obstacle_spawn_interval = 10000

# Initial chance of obstacle spawn
obstacle_spawn_chance = 4

# Replay variables
replay_prompt = False

# Main menu loop / Aayan and Arpit
menu_running = True
while menu_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_running = False
            sys.exit()

        if current_state == MENU:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                current_state = RUNNING

    if current_state == MENU:
        # Draw the main menu

        # Black background
        screen.fill((0, 0, 0)) 
      
        # Clear the screen and draw the logo
        screen.blit(logo_image, logo_rect)

        menu_text = score_font.render("Press SPACE to Start", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(screen_width / 2, screen_height - 50))
        screen.blit(menu_text, menu_rect)

        # Update the display
        pygame.display.flip()
        clock.tick(30)

    elif current_state == RUNNING:
        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Check for jump input / Hussain
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and character_sprite.jump_limit > 0:
                    character_sprite.is_jumping = True
                    character_sprite.jump_count = character_jump_force
                    character_sprite.jump_limit -= 1

                # Check for game over condition / Arpit
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    current_state = MENU
                    obstacles_group.empty()
                    character_sprite.rect.topleft = (character_x, character_y)
                    character_sprite.jump_limit = 4
                    character_sprite.is_jumping = False
                    score = 0
                    replay_prompt = False
                    running = False

            if not running:
                break

            # Update character sprite
            character_sprite.update()

            # Update background position based on character movement / Hussain
            background_x -= 10
            background_x2 -= 10

            # Reset background position if it goes off the screen / Hussain
            if background_x <= -screen_width:
                background_x = screen_width
            if background_x2 <= -screen_width:
                background_x2 = screen_width

            # Update score / Hussain
            current_time = pygame.time.get_ticks()
            if current_time - last_score_time >= score_increase_interval:
                score += 5
                last_score_time = current_time

            # Flash score effect / Hussain
            if score >= 300 and score % 300 == 0:
                flash_time = current_time
                flash_on = True
                score += 100

            # Check for game over condition / Arpit
            collided_obstacles = pygame.sprite.spritecollide(character_sprite, obstacles_group, False, pygame.sprite.collide_mask)
            if collided_obstacles:
                current_state = GAME_OVER
                replay_prompt = True
                if score > high_score:
                    high_score = score
                break

            # Create new obstacles at random intervals / Arpit
            if random.randint(1, 100) < obstacle_spawn_chance:
                obstacle = Obstacle()
                obstacles_group.add(obstacle)

            # Update obstacle positions
            obstacles_group.update()

            # Remove obstacles that go off the screen / Arpit
            for obstacle in obstacles_group.copy():
                if obstacle.rect.right <= 0:
                    obstacles_group.remove(obstacle)

            # Increase obstacle spawn chance every minute / Arpit
            if current_time % 60000 == 0:
                obstacle_spawn_chance += 6

            # Draw the backgrounds, character, and obstacles / Aayan
            screen.blit(background_image, (background_x, 0))
            screen.blit(background_image, (background_x2, 0))
            screen.blit(character_sprite.image, character_sprite.rect)
            obstacles_group.draw(screen)

            # Draw the score and high score / Hussain
            # https://www.youtube.com/watch?v=Fp1dudhdX8k
            score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(topright=(screen_width - 20, 20))
            screen.blit(score_text, score_rect)

            high_score_text = score_font.render(f"High Score: {high_score}", True, (255, 255, 255))
            high_score_rect = high_score_text.get_rect(topleft=(20, 20))
            screen.blit(high_score_text, high_score_rect)

            # Flash score effect / Aayan
            if flash_on:
                if current_time - flash_time >= flash_duration:
                    flash_on = False
                else:
                    flash_score_text = score_font.render("BONUS!", True, (255, 0, 0))
                    flash_score_rect = flash_score_text.get_rect(center=(screen_width / 2, screen_height / 2))
                    screen.blit(flash_score_text, flash_score_rect)

            # Update the display
            pygame.display.flip()
            clock.tick(30)

    elif current_state == GAME_OVER:
    # Game over loop
      game_over_running = True
      
      # Added variable to track if the death sound has been played / Hussain
      death_sound_played = False  
      while game_over_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_running = False
                sys.exit()

            # Check for replay input / Arpit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and replay_prompt:
                current_state = RUNNING
                obstacles_group.empty()
                character_sprite.rect.topleft = (character_x, character_y)
                character_sprite.jump_limit = 4
                character_sprite.is_jumping = False
                score = 0
                game_over_running = False

        if not game_over_running:
            break

        # Draw the game over screen / Arpit
        screen.fill((0, 0, 0)) 
        screen.blit(game_over_text, game_over_rect)

        if replay_prompt:
            replay_text = score_font.render("Press SPACE to Replay", True, (255, 255, 255))
            replay_rect = replay_text.get_rect(center=(screen_width / 2, screen_height / 2 + 100))
            screen.blit(replay_text, replay_rect)

        # Play the death sound effect only once / Hussain
        if not death_sound_played:
            death_sound.play()
            death_sound_played = True

        # Update the display
        pygame.display.flip()
        clock.tick(20)

    # Refresh the music / Aayan
    pygame.mixer.music.stop()
    pygame.mixer.music.play(-1)



# Quit the game
pygame.quit()

# https://www.youtube.com/watch?v=JgT-IOPxk-k (Death sound)
