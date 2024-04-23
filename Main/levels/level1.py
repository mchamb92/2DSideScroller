import pygame
import time
import os
import sys
import random
from game_lose import game_lose
from levels.platforms.platforms import TileMap
from levels.mobs.mobs_LevelOne import Mob
from main_character.player import Player
from levels.backgrounds.background import Background
from levels.Level1_boss.level1_boss import Boss
from Voice import Voice 
from soundtrack import soundtrack
from weapons.fireball import Fireball
from weapons.sword import Sword
from .win_lose_conditions import game_over


class Level1:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

        
        self.mobs = pygame.sprite.Group()  # Corrected from a list to a sprite group
        self.boss = pygame.sprite.Group()
        # Initialize Background with the display
        self.bg = Background(self.display)
        
        self.lines = "In a mystical realm, a hero embarks \non a quest to recover ancient artifacts,\n battling foes and unraveling mysteries\n to restore harmony to the land."
        # Frame rate and timing for spawns
        self.start_time = time.time()
        self.spawn_intervals = [3, 5, 6, 9, 10, 15] # seconds between spawns
        self.next_spawn_time = self.spawn_intervals[0]
        self.spawn_index = 0
        
         # Timing for text box display
        self.text_box_start_time = 1  # Displaying the text box 1 second into the game
        self.text_box_end_time = 10  # Stop displaying the text box 6 seconds into the game
        self.text_displayed = False  # Flag

        
        
        self.text_boss_start_time = 55
        self.text_boss_end_time = 60
        self.text_boss_displayed = False
        self.shake_intensity = 5
        
        #audio for the text
        self.audio_start_time = self.text_box_start_time
        self.audio_end_time = self.text_box_end_time
        
        self.audio_displayed = False  

        current_path = os.path.dirname(__file__)
        # Initialize the TileMap
        csv_file_path = "Main/levels/platforms/level 1 tile map.csv"
        self.tile_map = TileMap(csv_file_path, tile_size=32)  # Adjust as needed

        #initialize main character pos and jumps
        self.jumpCount = 0
        self.jump = 0
        self.player_x = 300
        self.player_y = 395
        self.alive = True
        
        self.freddy = Player.spawnPlayer(self.display, 2, 300, 390)
        print('freddy dimensions: ', self.freddy.rect.width, ', ', self.freddy.rect.height)
       
        self.sword = Sword(display,self.freddy)
        #initialize power up fireball to collect
        self.powerUp_img = pygame.image.load('assets/fireball.png').convert_alpha()
        self.scaled_width = 50  # Desired width after scaling
        self.scaled_height = 50  # Desired height after scaling
        
        self.powerUp_img1 = pygame.transform.scale(self.powerUp_img, (self.scaled_width, self.scaled_height))
        self.powerUp_rect = self.powerUp_img1.get_rect()
        print('Power Up dimensions: ', self.powerUp_rect.width, ',', self.powerUp_rect.height)
        self.powerUp_img2 = pygame.transform.flip(self.powerUp_img1,0, 90)
        self.powerUp_img3 = pygame.transform.flip(self.powerUp_img1,90,90)
        self.powerUp_img4 = pygame.transform.flip(self.powerUp_img1,90,0)
        self.fireFrame = 0
        
        
        # Original dimensions of the image
        # original_width, original_height = self.powerUp_img.get_width(), self.powerUp_img.get_height()
        # print(original_width, ", ", original_height, '\n')
        # Scale the image

        self.some_additional_offset = 100

        self.bossFightTextShown = False
        
        self.score = 0
        
    def spawn_mobs(self):
        
        dynamic_offset = 0
        if self.spawn_intervals[self.spawn_index] == 3:
            self.some_additional_offset = 500
            dynamic_offset = self.bg.scroll + self.some_additional_offset
            mobs_to_add = Mob.spawn_mobs_horizontally(self.display, 2, 400, 500, dynamic_offset)
            self.mobs.add(*mobs_to_add)
            print("Mob spawned : 1")
            
            
        if self.spawn_intervals[self.spawn_index] == 5:
            self.some_additional_offset = 1000
            dynamic_offset = self.bg.scroll + self.some_additional_offset
            mobs_to_add = Mob.spawn_mobs_horizontally(self.display, 1, 500, 50, dynamic_offset)
            self.mobs.add(*mobs_to_add)
            print("Mob spawned : 5")
            
            
        if self.spawn_intervals[self.spawn_index] == 6:
            self.some_additional_offset = 1500
            soundtrack('Main/music/xDeviruchi - Exploring The Unknown.wav')
            dynamic_offset = self.bg.scroll + self.some_additional_offset
            mobs_to_add = Mob.spawn_mobs_horizontally(self.display, 2, 500, 500, dynamic_offset)
            self.mobs.add(*mobs_to_add)
            print("Mob spawned : 8")
            
            
        if self.spawn_intervals[self.spawn_index] == 9:
            self.some_additional_offset = 2000
            dynamic_offset = self.bg.scroll + self.some_additional_offset
            mobs_to_add = Mob.spawn_mobs_horizontally(self.display, 2, 500, 200, dynamic_offset)
            self.mobs.add(*mobs_to_add)
            print("Mob spawned : 9")
           
            
        if self.spawn_intervals[self.spawn_index] == 10:
            self.some_additional_offset = 2500
            dynamic_offset = self.bg.scroll + self.some_additional_offset
            mobs_to_add = Mob.spawn_mobs_horizontally(self.display, 3, 500, 100, dynamic_offset)
            self.mobs.add(*mobs_to_add)
            print("Mob spawned : 10")
            
            
    def spawn_boss(self):
        

        if self.spawn_intervals[self.spawn_index] == 15:
            dynamic_offset = 10000
            boss_to_add = Boss.spawn_boss_horizontally(self.display, 1, 500, 50, dynamic_offset)
            self.boss.add(boss_to_add)
            
        

    #def spawn_powerUp(self):
        #make the png a sprite and scale and blit to screen
                
                      
            
    def update_timer(self):
        self.font = pygame.font.Font(None, 36)
    # Calculate elapsed time
        if self.gameStateManager.start_time is not None:
            current_time = time.time()
            elapsed_time = current_time - self.gameStateManager.start_time
        
            # Format as minutes:seconds
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            timer_text = f"{minutes:02d}:{seconds:02d}"
            if minutes >= 2:
                self.game_over
            # Render the text
            text_surface = self.font.render(timer_text, True, (255, 255, 255))  # White text
            text_rect = text_surface.get_rect(topright=(1420, 20))  # Position it at the top right
        
            # Blit the text surface onto the screen
            self.display.blit(text_surface, text_rect)
                 
    def game_over(self):
        result = game_over(self.display)  # Ensure you pass the correct display surface
        if result == 'restart':
            self.reset_game()  # Method to reset the game state
        elif result == 'quit':
            pygame.quit()
            sys.exit()

    def reset_game(self):
        # Reinitialize game components
        self.__init__(self.display, self.gameStateManager)
        self.run()  # Restart the game loop if necessary
  

    def run(self):
        self.display.fill((0, 0, 0))
        pygame.draw.rect(self.display, (255, 0, 0), (50, 50, 100, 100))  # Draw a red rectangle
        self.tile_map.draw(self.display)
        current_time = time.time()
        #total time since instance of lvl1 was initialized
        elapsed_time = current_time - self.start_time
        game_elapsed_time = current_time - self.start_time


        keys=pygame.key.get_pressed()
        self.freddy.update(keys)
        
        # Draw the background first
        self.bg.draw_bg()
        self.bg.draw_ground()
        self.update_timer()
        font = pygame.font.SysFont('Times New Roman',30)
        text_color = (255,255,255)
        text_surface = font.render('Freddy World', True, text_color)
        self.display.blit(text_surface, (0,10))
       

        #Jump button is 'w':
        if keys[pygame.K_w] and self.player_y == 395:
            #print('jump')
            self.jump = 1

        #Timed spawning only works with infinite scroll and infinite scroll doesn't work bc?
            #coordinate spawning would be easier to plan and level would have a set duration till boss fight.
            #less group list creation would be necessary --> cleaner code.    
        if elapsed_time >= self.next_spawn_time:
            #self
            self.spawn_mobs()
            self.spawn_boss()  
            self.spawn_index +=1
            if self.spawn_index < len(self.spawn_intervals):
                self.next_spawn_time += self.spawn_intervals[self.spawn_index]
            else:
                self.next_spawn_time = float('inf') # Stop spawning after last interval
                
        self.mobs.update()

        # Use a list to store temporary rects adjusted for scrolling, for collision detection
        temp_collision_rects = []

        for mob in self.mobs:
            # Calculate the drawing position considering scrolling
            mob_world_x = mob.rect.x - self.bg.scroll

            # Draw the mob with adjusted position
            self.display.blit(mob.image, (mob_world_x, mob.rect.y))
            Mob.draw_health_bar(self.display, mob, self.bg.scroll)
            
            pygame.draw.rect(self.display, (255, 0, 0), (mob_world_x, mob.rect.y, mob.rect.width, mob.rect.height), 2)
            
            # Create a temporary rect for collision detection, adjusted for scrolling
            temp_rect = pygame.Rect(mob_world_x, mob.rect.y, mob.rect.width, mob.rect.height)
            temp_collision_rects.append((mob, temp_rect))

                                       
        boss_temp_collision_rects = []                               
        #self.spawn_boss()   
        self.boss.update()
        for boss in self.boss:
            boss_world_x = boss.rect.x - self.bg.scroll
            self.display.blit(boss.image, (boss_world_x, boss.rect.y))
            Boss.draw_health_bar(self.display, boss, self.bg.scroll)
            # Create a temporary rect for collision detection, adjusted for scrolling
            temp_rects = pygame.Rect(boss_world_x, boss.rect.y, boss.rect.width, boss.rect.height)
            boss_temp_collision_rects.append((boss, temp_rects))
         
            
          
        keys = pygame.key.get_pressed()
        self.sword.update(keys)   
        
        
        if keys[pygame.K_LSHIFT]:
            for mob, temp_rect in temp_collision_rects:
                if self.sword.rect.colliderect(temp_rect):
                    mob.health -= 2
                    mob.speed_x+=.09
                    if mob.health == 2:
                        mob.kill()
                        self.score+=50        
                        
        for mob, temp_rect in temp_collision_rects:
                if self.freddy.rect.colliderect(temp_rect):
                    self.freddy.health -= 10
                    if self.freddy.health <=0:
                        self.freddy.kill()
                        game_lose('Main/music/xDeviruchi - The Final of The Fantasy.wav')
                        self.game_over() # Game over when health is depleted
                        
         
        score_text = f"Freddy Health: {self.freddy.health}"
        text_surface = self.font.render(score_text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(topright=(850, 50))  # Position it at the top right
        self.display.blit(text_surface, text_rect) 
        
        for boss, temp_rects in boss_temp_collision_rects:
            if self.sword.rect.colliderect(temp_rects):
                    boss.health -= 2
                    boss.speed_x+=.009
                    if boss.health == 2:
                        boss.kill()
                        print("You Won!!")
                              
        for boss, temp_rects in boss_temp_collision_rects:
                if self.freddy.rect.colliderect(temp_rects):
                    self.freddy.health -= 10
                    if self.freddy.health <=0:
                        self.freddy.kill()
                        pygame.quit()   
                        
        # Collision detection using temporary rects
        if keys[pygame.K_f]:
            for boss, temp_rect in temp_collision_rects:
                if self.freddy.rect.colliderect(temp_rect):
                    # Deduct health from the specific mob that was hit 
                    boss.health -= 5
                    
                    
                    # Check if the mob's health is 0 or less
                    if boss.health <= 0:
                        # If so, kill the mob
                        boss.kill()
                                   
        for boss, temp_rect in temp_collision_rects:
                if self.freddy.rect.colliderect(temp_rect):
                    self.freddy.health -= 1
                    if self.freddy.health <=0:
                        self.freddy.kill()
                        pygame.quit()
        
        #Update and draw player
        self.freddy.update(keys)
        if self.jump == 1:
            self.freddy.jump()
            self.jumpCount += 1
        if self.jumpCount >= 60:
            self.jump = 0
            self.jumpCount = 0
            self.freddy.rect.y = self.freddy.initial_y

        #Freddy is updated, so spawn the fireball at his pos
            #shoot fireball    
        if keys[pygame.K_f]:
            #spawn fireball into player projectile list
            #update fireball sprite every frame
            #apply gravity until it hits the ground and then make it bounce twice
            #explodes on third bounce or collision
            #remove fireball from the projectiles list
            self.freddy.projectiles.append(Fireball(350, self.freddy.rect.y, True))
            if self.fireFrame <= 20:
                self.display.blit(self.powerUp_img1, (350, self.freddy.rect.y))
                self.fireFrame += 1
            elif self.fireFrame <= 40:
                self.display.blit(self.powerUp_img2, (350, self.freddy.rect.y))
                self.fireFrame += 1
            elif self.fireFrame <= 60:
                self.display.blit(self.powerUp_img3, (350, self.freddy.rect.y))
                self.fireFrame += 1
            else:
                self.fireFrame += 1
                self.display.blit(self.powerUp_img4, (350, self.freddy.rect.y))
                if self.fireFrame == 80:    
                    self.fireFrame = 0

        
             
        self.display.blit(self.freddy.image, (self.freddy.rect.x - 25, self.freddy.rect.y - 15))
        pygame.draw.rect(self.display, (0, 255, 0), self.freddy.rect, 2)
        Player.draw_health_bar_player(self.display, self.freddy,100)
        
        
        
        if self.bg.scroll == 10000:
            keys = pygame.key.get_pressed()
            self.freddy.player_movements(keys)
        
        
        
        if self.text_box_start_time <= game_elapsed_time <= self.text_box_end_time:
            Player.draw_text_box(self.display, self.freddy,self.lines)
            if not self.audio_displayed:
                Voice('Main/music/AI.mp3')  # Play the audio
                #soundtrack('Main/music/xDeviruchi - Exploring The Unknown.wav')
                self.audio_displayed = True  # Prevent audio from being played again in this session
            self.text_displayed = True  # Keep showing the text box
        else:
            self.audio_displayed = False
        
        if self.text_boss_start_time <= game_elapsed_time <= self.text_boss_end_time:
            font = pygame.font.SysFont('Times New Roman', 100)
            text_color = (148, 0, 211)
            text_surface = font.render('BOSS FIGHT!!!!', True, text_color)

            # Random offset for shaking effect
            offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            offset_y = random.randint(-self.shake_intensity, self.shake_intensity)

            # Position for text
            text_x = 420 + offset_x
            text_y = 175 + offset_y

            # Blit the text surface to the display with shaking
            self.display.blit(text_surface, (text_x, text_y))
            self.text_boss_displayed = True
        if self.bg.scroll == 2000:
            self.score +=10
        if self.bg.scroll == 4000:
            self.score +=10
        if self.bg.scroll == 6000:
            self.score +=10
        if self.bg.scroll == 8000:
            self.score +=10
                                
        score_text = f"Scoreboard: {self.score:02d}"
        text_surface = self.font.render(score_text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(topright=(800, 20))  # Position it at the top right
        self.display.blit(text_surface, text_rect)     