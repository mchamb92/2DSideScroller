import pygame
import os

from weapons.fireball import Fireball
#testing branches on gitkraken.
class Player(pygame.sprite.Sprite):
    def __init__(self,imageChoice, screen_width = 700, screen_height=1500, initial_x = 300, initial_y = 390):
        super().__init__()
        #Current file directory
        self.fire = Fireball(350,450,True)
        print()
        imageChoice = 1
        current_path = os.path.dirname('assets')
        self.sprites = []
        self.death = []
        #Load image file path
        if imageChoice == 1:
            self.image = pygame.image.load('assets/main_character.png').convert_alpha()
            self.sprites.append(pygame.image.load('assets/main_char_walk_1.png').convert_alpha())
            self.sprites.append(pygame.image.load('assets/main_char_walk_2.png').convert_alpha())
            self.sprites.append(pygame.image.load('assets/main_char_walk_3.png').convert_alpha())
            self.sprites.append(pygame.image.load('assets/main_char_walk_4.png').convert_alpha())
            self.sprites.append(pygame.image.load('assets/main_char_walk_5.png').convert_alpha())
        
        elif imageChoice == 2:
            self.image = pygame.image.load('assets/main character 2nd option.png').convert_alpha()
        
        self.death.append(pygame.image.load('assets/main_char_death.png').convert_alpha())    
        self.current_frame = 0
        self.image = self.sprites[self.current_frame]    
        #self.rect = self.image.get_rect()
        #Creates the rectangle for the sprite, now scale it down
        # Scale down the sprite's rectangle
        scaled_rect_width = 39
        scaled_rect_height = 80
        self.rect = pygame.Rect(initial_x, initial_y, scaled_rect_width, scaled_rect_height)
        #This will be the area of collision
        #coordinates of top left corner.
        self.width = self.image.get_width
        self.height = self.image.get_height
        self.initial_y = initial_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.jump_max = screen_height - 80
        self.parabolaX = 0
        
        self.health = 500
        
        self.ticks = pygame.time.get_ticks()
        self.animation_delay = 200
        self.animation_timer = self.ticks
        self.speed = 5
        #Fireball Power-Up
        self.flameOn = False
        self.projectiles = []
        
    @staticmethod
    def spawnPlayer(display, imageNum, initial_x, initial_y):
        screen_width = display.get_width()
        screen_height = display.get_height()
        player = Player(imageNum, screen_width, screen_height, initial_x, initial_y)  
        return player
    
    @staticmethod
    def draw_health_bar_player(display, player,scroll):
        # Health bar drawing
        health_percentage = player.health / 500
        bar_width = 50
        bar_height = 10
        fill = bar_width * health_percentage
        outline_rect = pygame.Rect(player.rect.x-scroll + 70, player.rect.y -50, bar_width, bar_height)
        fill_rect = pygame.Rect(player.rect.x-scroll + 70, player.rect.y - 50, fill, bar_height)
        
        pygame.draw.rect(display, (255, 0, 0), outline_rect)  # Red background
        pygame.draw.rect(display, (0, 255, 0), fill_rect)  # Green foreground
        pygame.draw.rect(display, (255, 255, 255), outline_rect, 2)  # White border 
   
    @staticmethod
    def draw_text_box(display, player, text, font_size=24, text_color=(255, 255, 255), box_color=(0, 0, 0, 128), padding=10, offset_y=50):
        font = pygame.font.Font(None, font_size)


        lines = text.split('\n')
        max_width = 0
        text_surfs = []


        for line in lines:
            text_surf = font.render(line, True, text_color)
            text_surfs.append(text_surf)
            if text_surf.get_width() > max_width:
                max_width = text_surf.get_width()


        total_height = sum(text_surf.get_height() for text_surf in text_surfs) + padding * (len(text_surfs) - 1)


        box_rect = pygame.Rect(0, 0, max_width + padding * 2, total_height + padding * 2)
        box_rect.center = (player.rect.centerx, player.rect.y - offset_y - total_height // 2 - padding)


        box_surface = pygame.Surface(box_rect.size, pygame.SRCALPHA)
        box_surface.fill(box_color)


        display.blit(box_surface, box_rect.topleft)


        current_y = box_rect.y + padding
        for text_surf in text_surfs:
            text_rect = text_surf.get_rect(center=(box_rect.centerx, current_y + text_surf.get_height() // 2))
            display.blit(text_surf, text_rect)
            current_y += text_surf.get_height() + padding
    
   
   
   
    def jump(self):
        #Jump curve
        factor = self.parabolaX - 30
        square = factor*factor
        coefficient = float(square)*0.2
        jump_height = int(coefficient)-180
        self.rect.y = self.initial_y + jump_height
        self.parabolaX += 1
        if self.parabolaX >= 60:
            self.parabolaX = 0
            
    def player_movements(self, keys):
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))

    def update(self, keys_pressed):
    # Check for movement
        if pygame.time.get_ticks() - self.animation_timer > self.animation_delay:
            self.animation_timer = pygame.time.get_ticks()
            if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_d]:
                # If moving, update animation
                self.current_frame = (self.current_frame + 1) % len(self.sprites)
                if self.current_frame == 0:
                    self.current_frame = 1  # Skip frame 0

            else:
                self.current_frame = 0  # Set current frame to 0 when not moving

            # Update the image according to the current frame
            if keys_pressed[pygame.K_a]:
                self.image = pygame.transform.flip(self.sprites[self.current_frame], True, False)
            else:
                self.image = self.sprites[self.current_frame]

        # Check for movement
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_d]:
            # If moving, update position
            # Your movement logic here
            pass
        if self.health == 5:
            self.image = self.death[0]