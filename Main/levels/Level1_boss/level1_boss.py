import pygame


class Boss(pygame.sprite.Sprite):
    def __init__(self, screen_width=600, screen_height=1500, initial_y=0, initial_x=None):
        super().__init__()
        self.image = pygame.image.load("Main/Level1_img/boss/first_boss.png").convert_alpha()
        
        self.rect = self.image.get_rect()
        
        # Set initial positions
        if initial_x is None:
            initial_x = screen_width // 10  # Start at the middle of the screen
        self.rect.x = initial_x
        self.rect.y = initial_y
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.gravity = 0.5  # Gravity effect
        self.jump_force = -15  # Initial force for jumps
        self.vertical_speed = 0  # Current vertical speed
        
        self.speed_x = 1  # Horizontal speed
        
        self.direction_x = -1  # 1 for right, -1 for left
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.jump_max = screen_height-100  # this set a max limt for the mob to jump to
        
        self.health = 1000
          
    @staticmethod
    def spawn_boss_horizontally(display, num_mobs, initial_y, spacing, x_offset=0):
        screen_width, screen_height = display.get_size()
        bosses = pygame.sprite.Group()
        initial_y = 450
        for i in range(num_mobs):
            initial_x = (i * spacing) + x_offset
            boss = Boss(screen_width=screen_width, screen_height=screen_height, initial_y=initial_y, initial_x=initial_x)
            bosses.add(boss)
        return bosses
    
    @staticmethod
    def draw_health_bar(display, bosses, scroll):
        # Health bar drawing
        health_percentage = bosses.health / 1000
        bar_width = 50
        bar_height = 10
        fill = bar_width * health_percentage
        outline_rect = pygame.Rect(bosses.rect.x-scroll + 50, bosses.rect.y -10, bar_width, bar_height)
        fill_rect = pygame.Rect(bosses.rect.x-scroll + 50, bosses.rect.y - 10, fill, bar_height)
        
        pygame.draw.rect(display, (255, 0, 0), outline_rect)  # Red background
        pygame.draw.rect(display, (0, 255, 0), fill_rect)  # Green foreground
        pygame.draw.rect(display, (255, 255, 255), outline_rect, 2)  # White border 



    def update(self):
        
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