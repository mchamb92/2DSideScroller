
import pygame,sys

# Assuming you've initialized pygame and set up a display beforehand

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Mob(pygame.sprite.Sprite):
    def __init__(self, screen_width=600, screen_height=1500, initial_y=None, initial_x=None):
        super().__init__()
        self.sprites = []
        self.death = []
        self.is_animating = True
        self.sprites.append(pygame.image.load('Main/Level1_Img/mob/mob_walk_death_1.png'))
        self.sprites.append(pygame.image.load('Main/Level1_Img/mob/mob_walk_death_2.png'))
        self.death.append(pygame.image.load('Main/Level1_Img/mob/mob_walk_death_3.png'))
        self.current_sprite = 0
        self.image_change_delay = 10
        self.current_delay = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        # Set initial positions. If no initial_x is provided, start at the screen's 10%.
        # For initial_y, if not provided, place it 50 pixels above the bottom.
        if initial_x is None:
            initial_x = screen_width // 10 
        if initial_y is None:
            initial_y = screen_height - 50  # Adjust to spawn closer to the bottom

        self.rect.x = initial_x
        self.rect.y = initial_y
        
        self.gravity = 0.5  # Gravity effect
        self.jump_force = -10  # Initial force for jumps
        self.vertical_speed = 0  # Current vertical speed
        
        self.speed_x = 0.55  # Horizontal speed
        
        self.direction_x = -1  # 1 for right, -1 for left
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.jump_max = screen_height-100  # this set a max limt for the mob to jump to
        
        self.health = 100  # Max health
        
    @staticmethod
    def draw_health_bar(display, mob, scroll):
        # Health bar drawing
        health_percentage = mob.health / 100
        bar_width = 50
        bar_height = 10
        fill = bar_width * health_percentage
        outline_rect = pygame.Rect(mob.rect.x-scroll + 30, mob.rect.y -20, bar_width, bar_height)
        fill_rect = pygame.Rect(mob.rect.x-scroll + 30, mob.rect.y - 20, fill, bar_height)
        
        pygame.draw.rect(display, (255, 0, 0), outline_rect)  # Red background
        pygame.draw.rect(display, (0, 255, 0), fill_rect)  # Green foreground
        pygame.draw.rect(display, (255, 255, 255), outline_rect, 2)  # White border 
          
    @staticmethod
    def spawn_mobs_horizontally(display, num_mobs, initial_y, spacing, x_offset=0):
        screen_width = display.get_width()
        screen_height = display.get_height()
        mobs = pygame.sprite.Group()
        initial_y = screen_height - 50
        for i in range(num_mobs):
            initial_x = (i * spacing) + x_offset  # Use the dynamic offset here
        # Ensure mobs spawn within the intended area, adjusting as necessary
            mob = Mob(screen_width=screen_width, screen_height=screen_height, initial_y=initial_y, initial_x=initial_x)
            mobs.add(mob)

        return mobs


    def update(self):
        if self.is_animating == True:
            self.current_delay += 1

            if self.current_delay >= self.image_change_delay:
                self.current_sprite += 1
                self.current_delay = 0

                if self.current_sprite >= len(self.sprites):
                    self.current_sprite = 0

                self.image = self.sprites[self.current_sprite]
                
        if self.health == 10:
            self.image = self.death[0]
        # speed based on direction
        self.rect.x += self.speed_x * self.direction_x
        
        # Apply gravity
        self.vertical_speed += self.gravity
        self.rect.y += self.vertical_speed
            
        # Boundary checks and jumping logic
        if self.rect.bottom > self.jump_max:
            self.rect.bottom = self.jump_max
            self.vertical_speed = self.jump_force  # Apply jump force to simulate a bounce
        elif self.rect.top < 0:
            self.rect.top = 0
            self.vertical_speed = 0  # Stop upward movement

    def seeRect(self, bg_scroll):
        self.rect.x -= bg_scroll    
    def revertX(self, bg_scroll):
        self.rect.x += bg_scroll
pygame.init()
clock = pygame.time.Clock()
moving_sprites = pygame.sprite.Group()

# Create an instance of the Mob class
mob_instance = Mob()
# Add the instance to the group
moving_sprites.add(mob_instance)

# Update and render the sprites
moving_sprites.update()

# Control the frame rate
clock.tick(10)