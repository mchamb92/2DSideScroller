import pygame
import sys

def game_over(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font('assets/Gothic Pixels.ttf', 50)  # Updated to use custom font
    background = pygame.image.load('Main/Level1_Img/backgrounds/game_over_level1.png')  # Load the background image
    
    # Get the dimensions of the screen for centering text
    screen_width, screen_height = screen.get_size()
    # Load the background image and scale it to the current screen size
    background = pygame.image.load('Main/Level1_Img/backgrounds/game_over_level1.png')
    background = pygame.transform.scale(background, (screen_width, screen_height))
    bg_rect = background.get_rect()

    # Define a vertical offset for the text position
    vertical_offset = screen.get_height() * 0.7  # Adjust this value as needed

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    return 'restart'
                elif event.key == pygame.K_q:  # Quit the game
                    return 'quit'

       # Instead of filling the screen with a solid color, blit the loaded background
        screen.blit(background, bg_rect.topleft)
        text_restart = font.render('Press R to Restart', True, (139, 0, 0))
        text_quit = font.render('Press Q to Quit', True, (139, 0, 0))
        
        # Calculate the text's position to center it horizontally and adjust the vertical position
        restart_rect = text_restart.get_rect(center=(screen.get_width() / 2, vertical_offset))
        quit_rect = text_quit.get_rect(center=(screen.get_width() / 2, vertical_offset + 50))
        # Blit the text onto the screen at the new positions
        screen.blit(text_restart, restart_rect.topleft)
        screen.blit(text_quit, quit_rect.topleft)
        
        pygame.display.flip()
        clock.tick(30)

def game_win(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font('assets/Gothic Pixels.ttf', 50)  # Updated to use custom font  # Slightly larger font for the win message
    background = pygame.image.load('Main/Level1_Img/backgrounds/win_level1.png')

    # Get the dimensions of the screen for centering text and scaling the image
    screen_width, screen_height = screen.get_size()
    background = pygame.transform.scale(background, (screen_width, screen_height))
    bg_rect = background.get_rect()

    # Define a vertical offset for the text position, adjusted to suit the win screen layout
    vertical_offset = screen_height * 0.75  # Adjust as needed based on your image

    # Prepare the win text
    text_win = font.render('Congratulations! You have won!', True, (255, 215, 0))  # Gold color for celebration
    text_rect = text_win.get_rect(center=(screen_width / 2, vertical_offset))

    # Render the win screen for a set duration or until a key is pressed
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Option to Restart
                    return 'restart'
                elif event.key == pygame.K_m:  # Option to go to the main menu, if you have one
                    return 'main_menu'

        # Blit the win background
        screen.blit(background, bg_rect.topleft)

        # Blit the win text
        screen.blit(text_win, text_rect)

        pygame.display.flip()
        clock.tick(30)

        