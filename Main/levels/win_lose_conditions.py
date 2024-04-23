import pygame
import sys

def game_over(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 36)
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
        text_restart = font.render('Press R to Restart', True, (255, 255, 255))
        text_quit = font.render('Press Q to Quit', True, (255, 255, 255))
        
        # Calculate the text's position to center it horizontally and adjust the vertical position
        restart_rect = text_restart.get_rect(center=(screen.get_width() / 2, vertical_offset))
        quit_rect = text_quit.get_rect(center=(screen.get_width() / 2, vertical_offset + 50))
        # Blit the text onto the screen at the new positions
        screen.blit(text_restart, restart_rect.topleft)
        screen.blit(text_quit, quit_rect.topleft)
        
        pygame.display.flip()
        clock.tick(30)
