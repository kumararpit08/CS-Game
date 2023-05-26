import pygame

pygame.init()

# Set up the display window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the font and text for the menu options
font = pygame.font.Font(None, 30)
menu_options = [
    "Play Game",
    "Sound",
    "Settings",
    "Character Skins",
]
selected_option = None  # currently selected option (None indicates no selection)

# Set up the clock for limiting the frame rate
clock = pygame.time.Clock()

# Set up the game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if selected_option is not None:
                    selected_option_text = menu_options[selected_option]
                    if selected_option_text == "Play Game":
                        print("Play game option selected")
                        # Add your game logic here
                    elif selected_option_text == "Sound":
                        print("Sound option selected")
                        # Add sound control logic here
                    elif selected_option_text == "Settings":
                        print("Settings option selected")
                        # Add settings logic here
                    elif selected_option_text == "Character Skins":
                        print("Character Skins option selected")
                        # Add character skin logic here
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            selected_option = None
            for i, option in enumerate(menu_options):
                text = font.render(option, True, (255, 255, 255))
                text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 + i * 50))
                if text_rect.collidepoint(mouse_pos):
                    selected_option = i
                    break

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the menu options
    for i, option in enumerate(menu_options):
        text = font.render(option, True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 + i * 50))
        if i == selected_option:
            pygame.draw.rect(screen, (255, 255, 255), (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10))
        screen.blit(text, text_rect)

    # Update the display and limit the frame rate
    pygame.display.update()
    clock.tick(60)

pygame.quit()
