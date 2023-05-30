import pygame
import random

# Set up the display window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Obstacle Dodge")

# Obstacle properties
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 20

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("obstacle.png")
        self.image = pygame.transform.scale(self.image, (obstacle_width, obstacle_height))
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.randint(0, screen_height - obstacle_height)

    def update(self):
        self.rect.x -= obstacle_speed
