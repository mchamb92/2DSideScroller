import pygame
import sys
from button import Button

class Options:
    def __init__(self, display, gameStateManager, previous_state):
        self.display = display
        self.gameStateManager = gameStateManager
        self.previous_state = previous_state
        self.font = pygame.font.Font(None, 48)
        self.base_color = (200, 200, 200)
        self.hovering_color = (255, 255, 255)
        self.buttons = []
        self.selected_button = None
        self.create_buttons()
        self.running = False  # Add a flag to control the run loop

    def create_buttons(self):
        button_texts = ["Volume settings", "Exit"]
        button_positions = [(self.display.get_width() // 2, 200), (self.display.get_width() // 2, 300)]
        for text, pos in zip(button_texts, button_positions):
            button = Button(None, pos, text, self.font, self.base_color, self.hovering_color)
            self.buttons.append(button)

    def run(self):
        self.running = True  # Set the running flag to True
        while self.running:  
            self.display.fill((50, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_hover(event.pos)

            for button in self.buttons:
                button.update(self.display)

            pygame.display.flip()

    def handle_click(self, position):
        for button in self.buttons:
            if button.checkForInput(position):
                if button.text_input == "Exit":
                    self.gameStateManager.set_state(self.previous_state)
                    self.running = False  # Set running flag to False to exit the run loop
                return
            
    def handle_hover(self, position):
        for button in self.buttons:
            if button.checkForInput(position):
                button.changeColor(position)
                return
