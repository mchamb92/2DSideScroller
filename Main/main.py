import pygame
import sys
import time
from title import Menu
from levels.level1 import Level1
from options import Options
from soundtrack import soundtrack


FPS = 45

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1500,600), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.gameStateManager = GameStateManager('menu')
        self.menu = Menu(self.screen, self.gameStateManager)
        self.start = Start(self.screen, self.gameStateManager)
        self.level1 = Level1(self.screen, self.gameStateManager)
        self.options = Options(self.screen, self.gameStateManager, self.gameStateManager.get_state())
        
        self.states = {'start':self.start, 'menu': self.menu, 'level1': self.level1, 'options': self.options}
    
        # Initialize pause state
        self.paused = False  # Add this line to track pause state

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Toggle pause state when escape is pressed, space now for fireballsa
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                        if self.paused:
                            print("Game paused. Press 'Escape' to resume.")
                        else:
                            print("Game resumed.")
                    elif event.key == pygame.K_o:  # Switch to options menu
                        self.gameStateManager.set_state('options', self.gameStateManager.get_state())  # Pass the current state as previous state

            if not self.paused:
                current_state = self.gameStateManager.get_state()
                if current_state == 'menu':
                    self.menu.main_menu()
                elif current_state == 'options':  # Run options menu
                    self.options.run()
                else:
                    if self.level1.heatUp == True:
                        self.level1.gettingFired()
                    else:
                        self.states[current_state].run()
            


            pygame.display.update()
            self.clock.tick(FPS)

class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.font = pygame.font.Font(None, 36)
        # Pass gameStateManager to the Menu
        self.menu = Menu(self.display, self.gameStateManager)

    def run(self):
        # Initialize the loadingscreen attribute
        self.loadingscreen = None
        self.loadingscreen = pygame.image.load(r"Main/Level1_Img/backgrounds/loading_screen.png")
        # Get the dimensions of the display
        screen_width, screen_height = self.display.get_size()
        # Resize the image to fit the screen dimensions
        self.loadingscreen = pygame.transform.scale(self.loadingscreen, (screen_width, screen_height))
        self.display.blit(self.loadingscreen, (0, 0))
        text_surface = self.font.render('Press E to start', True, (255, 255, 255))  # Render white text
        text_rect = text_surface.get_rect(center=(750, 300))  # Position the text in the center
        self.display.blit(text_surface, text_rect)
        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.gameStateManager.set_state('level1')
            self.gameStateManager.start_time = time.time()  # Record start time
        if self.gameStateManager.get_state() == 'menu':
            self.menu.main_menu()
        elif self.gameStateManager.get_state() == 'level1':
            
            pass
 
                      
class GameStateManager:
    def __init__(self, currentState):
        self.currentState=currentState
        self.start_time = None  # Add this line
    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state

    
if __name__ == '__main__': 
    soundtrack('Main/music/Title Theme.wav')
    game = Game()
    game.run()