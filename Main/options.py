import pygame
import sys
from button import Button
from soundtrack import set_volume, current_volume

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
        # Adjusting the position of the volume slider to center it horizontally
        self.volume_slider = pygame.Rect(self.display.get_width() // 2 - 200, 300, 400, 20)  # Volume slider position and size
        self.volume_text = self.font.render("Volume", True, (255, 255, 255))  # Render volume text
        self.volume_text_rect = self.volume_text.get_rect(center=(self.display.get_width() // 2, 250))  # Position volume text above exit button
        self.volume_level = current_volume #Initial volume level (0 to 1)
        self.running = False  # Add a flag to control the run loop
    

    def create_buttons(self):
        button_texts = ["Volume Setting", "Exit"]
        button_positions = [(self.display.get_width() // 2, 200), (self.display.get_width() // 2, 400)]
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
                elif event.type == pygame.KEYDOWN:
                    print("Key pressed:", event.key)  
                    if event.key == pygame.K_ESCAPE:
                        self.gameStateManager.set_state(self.previous_state)
                        self.running = False
                    else:
                        self.handle_key(event.key)

            # Draw volume slider
            pygame.draw.rect(self.display, (255, 255, 255), self.volume_slider)
            pygame.draw.rect(self.display, (0, 0, 255), (self.volume_slider.x, self.volume_slider.y, self.volume_slider.width * self.volume_level, self.volume_slider.height))

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
            
    def handle_key(self, key):
        if key == pygame.K_q:
            print("Decrease volume key pressed")
            self.volume_level = max(0, self.volume_level - 0.1)
            set_volume(self.volume_level)
        elif key == pygame.K_e:
            print("Increase volume key pressed")
            self.volume_level = min(1, self.volume_level + 0.1)
            set_volume(self.volume_level)
