import pygame
import sys
from button import Button  # Ensure this is correctly implemented elsewhere

class Menu:
    def __init__(self, screen,gameStateManager):
        self.screen = screen
        self.bg = pygame.image.load("assets/background2.png")
        self.font_path = "assets/font.ttf"  # Update this path as needed
        self.gameStateManager = gameStateManager
    def get_font(self, size):  # Helper method to load fonts
        return pygame.font.Font(self.font_path, size)

    def play(self):
        # Implement play screen functionality here
            self.gameStateManager.set_state('start')
            return

    def options(self):
        # Implement options screen functionality here
        self.gameStateManager.set_state('options')
        pass
	
    def main_menu(self):
        while True:
            self.screen.blit(self.bg, (0, 0))
            menu_mouse_pos = pygame.mouse.get_pos()

            menu_text = self.get_font(100).render("MAIN MENU", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(750, 100))
            self.screen.blit(menu_text, menu_rect)

            play_button = Button(image=None, pos=(750, 250), 
                                 text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            options_button = Button(image=None, pos=(750, 400), 
                                    text_input="OPTIONS", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            quit_button = Button(image=None, pos=(750, 550), 
                                 text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            for button in [play_button, options_button, quit_button]:
                button.changeColor(menu_mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(menu_mouse_pos):
                        self.play()
                    if options_button.checkForInput(menu_mouse_pos):
                        self.options()
                    if quit_button.checkForInput(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()
            if self.gameStateManager.get_state() != 'menu':
                return              
            pygame.display.update()
