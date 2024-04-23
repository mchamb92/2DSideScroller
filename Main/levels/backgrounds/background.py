import pygame

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 600

class Background:
    def __init__(self, screen):
        self.scroll = 0
        self.screen = screen  # Use the game window passed in
        
        self.bg_images = []
        for i in range(1, 6):                
            bg_image = pygame.image.load(f"Main/Level1_img/backgrounds/plx-{i}.png").convert_alpha()
            bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg_images.append(bg_image)
                
        if self.bg_images:
            self.bg_width = self.bg_images[0].get_width()
            
        self.ground_image = pygame.image.load("Main/Level1_img/backgrounds/ground.png").convert_alpha()
        self.ground_width = self.ground_image.get_width()
        self.ground_height = self.ground_image.get_height() 

    def draw_bg(self):
        for x in range(15):
            speed = 1
            for i in self.bg_images:
                self.screen.blit(i, ((x * self.bg_width) - self.scroll * speed, 0))
                speed += .001
        #get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and self.scroll > 0:
            self.scroll -= 5
        if key[pygame.K_d] and self.scroll < 10000:
            self.scroll += 5
    def draw_ground(self):
        for x in range(19):
            self.screen.blit(self.ground_image, ((x * self.ground_width) - self.scroll * 1, SCREEN_HEIGHT - self.ground_height))
