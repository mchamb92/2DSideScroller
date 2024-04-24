import pygame as pg
import pygame
class Fireball(object):
    def __init__(self, x_pos, y_pos, move_direction: bool):
        super().__init__()
       
        self.rect = pg.Rect(x_pos, y_pos, 16, 16)
        
        self.direction = move_direction#-->
        #tertiary statement: (research review)
        self.x_vel = 5 if move_direction else -5
        self.y_vel = 0
        self.screen_height = 700
        self.jump_max = self.screen_height - 80
        self.gravity = 0.5  # Gravity effect
        self.jump_force = -10  # Initial force for jumps
        self.bounced = False

        self.state = 0
        self.current_image = 0
        self.image_tick = 0
        #7 images loaded into class
        self.fires = [pg.image.load('assets/fireball.png').convert_alpha()]
        self.fires.append(pg.transform.rotate(self.fires[0], -90))
        self.fires.append(pg.transform.rotate(self.fires[1], -90))
        self.fires.append(pg.transform.rotate(self.fires[2], -90))
        self.fires.append(pg.image.load('assets/firework0.png').convert_alpha())
        self.fires.append(pg.image.load('assets/firework1.png').convert_alpha())
        self.fires.append(pg.image.load('assets/firework2.png').convert_alpha())


    def update(self):
        if self.state == 0:
            self.update_image()
            self.move()
        elif self.state == -1:
            self.update_image()
    
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
                self.state = -2

    def move(self):
        #has it hit the floor?
        self.rect.x += self.x_vel
        if self.rect.y >= 470 and self.bounced == False: 
            self.rect.y == 470
            self.y_vel = self.jump_force
            self.bounced = True
        elif self.rect.y < 470 and self.bounced == True:
            self.bounced = False
        self.y_vel += self.gravity
        if self.y_vel > 10:
            self.y_vel = 10
        self.rect.y += self.y_vel

    def start_boom(self):
        self.x_vel = 0
        self.y_vel = 0
        self.current_image = 4
        self.image_tick = 0
        self.state = -1
        
    
###################################################################################################
            