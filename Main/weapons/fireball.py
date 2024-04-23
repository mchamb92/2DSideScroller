import pygame as pg
import pygame
class Fireball(object):
    def __init__(self, x_pos, y_pos, move_direction: bool):
        super().__init__()
        #What we need to do:
        #determine when the fire will spawn, collision as circle
        #fireball leaves the mouth of the freddy dred sprite.
        #--troubleshoot printing the fireball directly over sprite's mouth consistently.
        #need x and y coordinates attached to sprite circle (research)
        #
        #Rect created, try to create a circle too
        self.rect = pg.Rect(x_pos, y_pos, 16, 16)
        
        self.direction = move_direction#-->
        #tertiary statement: (research review)
        self.x_vel = 5 if move_direction else -5

        self.y_vel = 0

        self.state = 0
        self.current_image = 0
        self.image_tick = 0
        #7 images loaded into class
        self.fires = [pg.image.load('assets/fireball.png').convert_alpha()]
        self.fires.append(pg.transform.flip(self.fires[0], 0, 90))
        self.fires.append(pg.transform.flip(self.fires[0], 90, 90))
        self.fires.append(pg.transform.flip(self.fires[0], 90, 0))
        self.fires.append(pg.image.load('assets/firework0.png').convert_alpha())
        self.fires.append(pg.image.load('assets/firework1.png').convert_alpha())
        self.fires.append(pg.image.load('assets/firework2.png').convert_alpha())
        
        self.fireball = pygame.image.load("assets/fireball.png").convert_alpha()
        
        self.rect=self.fireball.get_rect()
        
        screen_height = 1500
        self.jump_max = screen_height-100
        self.gravity = 0.5  # Gravity effect
        self.jump_force = -15  # Initial force for jumps
        self.vertical_speed = 0  # Current vertical speed
        
        self.speed_x = 1  # Horizontal speed
        
        self.direction_x = 1  # 1 for right, -1 for left
    #update parameters for use in level1.py
    def update_image(self):
        self.image_tick += 1
            #rolling fireball
        if self.state == 0:
            if self.image_tick % 15 == 0:
                self.current_image += 1
                if self.current_image > 3:
                    self.current_image = 0
                    self.image_tick = 0
                            #kaboom
        elif self.state == -1:
            if self.image_tick % 10 == 0:
                self.current_image += 1
            if self.current_image == 7:
                #end of explosion, so remove the object
                core.get_map().remove_whizbang(self)

    def start_boom(self):
        self.x_vel = 0
        self.y_vel = 0
        self.current_image = 4
        self.image_tick = 0
        self.state = -1

    def update_x_pos(self, blocks):
        self.rect.x += self.x_vel
      
        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                if pg.Rect.colliderect(self.rect, block.rect):

                    # Fireball blows up only when collides on x-axis
                    self.start_boom()

    def update_y_pos(self, blocks):
        self.rect.y += self.y_vel
        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                if pg.Rect.colliderect(self.rect, block.rect):
                    self.rect.bottom = block.rect.top
                    self.y_vel = -3
#update borders in this function//
    def check_map_borders(self, core):
        if self.rect.x <= 0:
            core.get_map().remove_whizbang(self)
        elif self.rect.x >= 6768:
            core.get_map().remove_whizbang(self)
        elif self.rect.y > 448:
            core.get_map().remove_whizbang(self)

    def move(self, core):
        self.y_vel += GRAVITY

        blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
        self.update_y_pos(blocks)
        self.update_x_pos(blocks)

        self.check_map_borders(core)

    def check_collision_with_mobs(self, core):
        for mob in core.get_map().get_mobs():
            if self.rect.colliderect(mob.rect):
                if mob.collision:
                    mob.die(core, instantly=False, crushed=False)
                    self.start_boom()

    def update(self, core):
        if self.state == 0:
            self.update_image(core)
            self.move(core)
            self.check_collision_with_mobs(core)
        elif self.state == -1:
            self.update_image(core)
    #where to blit the image from. write the blit statement on this function?
    def render(self, window):
        #self.screen = pg.display.set_mode((WINDOW_W, WINDOW_H))

        #include the window data into this file so I can blit from here.


        core.screen.blit(self.images[self.current_image], core.get_map().get_camera().apply(self))
###################################################################################################
    #maybe apply into level1.py
        #the function will need to be defined in the level class becasue that is where
        #the fire is spawned, updated, and printed/rendered.
    def spawn_fireball(self, x, y, move_direction):
        #define list self.projectiles in levelone class
            #//player inventory/state could define the projectiles list//
        #spawn_fireball creates an instance of Fireball in level1,
        #then adds it to projectiles list.
        self.projectiles.append(Fireball(x, y, move_direction))
    def remove_fireball(self, whizbang):
        #remove_whizbang deletes the fireball from object from self.projectiles
        self.projectiles.remove(whizbang)
    # Player's fireballs
        #update then render

    #for whizbang in self.projectiles:
        #whizbang.update(core)
            #update is the function in the Fireball class,
            #and whizbang is the name of the Fireball instance.

    #for whizbang in self.projectiles:
            #whizbang.render(core)
        
    #summarize the instructions for screen scrolling and player traversal.
        #send in discord chat and text.

    #Logically speaking, I want the player to have the ability to spawn the fireballs
    def Throw(self,keys):
        if keys[pygame.K_f]:
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
            