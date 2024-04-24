import pygame
import time
import os
import sys
import random
from game_lose import game_lose, win_music
from levels.platforms.platforms import TileMap
from levels.mobs.mobs_LevelOne import Mob
from main_character.player import Player
from levels.backgrounds.background import Background
from levels.Level1_boss.level1_boss import Boss
from Voice import Voice 
from soundtrack import soundtrack
from weapons.fireball import Fireball
from weapons.sword import Sword
from .win_lose_conditions import game_over, game_win

#published to github
class Level1:
    def __init__(self, display, gameStateManager):

        self.display = display
        self.gameStateManager = gameStateManager
        # Initialize Background with the display
        self.bg = Background(self.display)
        
        self.mobs = pygame.sprite.Group()
        self.boss = pygame.sprite.Group()
        
        # Frame rate and timing for spawns
        self.start_time = time.time()
        self.spawn_intervals = [3, 5, 6, 9, 10, 8] # seconds between spawns
        self.next_spawn_time = self.spawn_intervals[0]
        self.spawn_index = 0
        self.some_additional_offset = 100
        
        # Timing for text box display
        self.lines = "In a mystical realm, a hero embarks \non a quest to recover ancient artifacts,\n battling foes and unraveling mysteries\n to restore harmony to the land."
        self.text_box_start_time = 1  # Displaying the text box 1 second into the game
        self.text_box_end_time = 10  # Stop displaying the text box 6 seconds into the game
        self.text_displayed = False  # Flag

        self.animateIterate = 80
        self.heatUp = False
        
        self.text_boss_start_time = 55
        self.text_boss_end_time = 60
        self.text_boss_displayed = False
        self.shake_intensity = 5
        
        #audio for the text
        self.audio_start_time = self.text_box_start_time
        self.audio_end_time = self.text_box_end_time
        self.audio_displayed = False  

        # Boss text
        self.bossFightTextShown = False

        # Initialize the TileMap
        csv_file_path = "Main/levels/platforms/level 1 tile map.csv"
        self.tile_map = TileMap(csv_file_path, tile_size=32)  # Adjust as needed

        #initialize main character, pos, and jump variables
        self.jumpCount = 0
        self.jump = 0
        self.player_x = 300
        self.player_y = 395
        self.alive = True
        self.freddy = Player.spawnPlayer(self.display, 1, 300, 390)
        self.score = 0
       
        self.sword = Sword(display,self.freddy)
        #initialize power up fireball to collect
        self.powerUp_img = pygame.image.load('assets/fireball.png').convert_alpha()
        self.scaled_width = 50  # Desired width after scaling
        self.scaled_height = 50  # Desired height after scaling
        
        self.powerUp_img1 = pygame.transform.scale(self.powerUp_img, (self.scaled_width, self.scaled_height))
        self.powerUp_rect = self.powerUp_img1.get_rect()
        self.powerUp_img2 = pygame.transform.rotate(self.powerUp_img1,-90)
        self.powerUp_img3 = pygame.transform.rotate(self.powerUp_img2,-90)
        self.powerUp_img4 = pygame.transform.rotate(self.powerUp_img3,-90)
        self.fireFrame = 0
        self.spawnFire = False
        self.despawnFire = False

        self.apple = pygame.image.load('assets/apple.png').convert_alpha()
        self.apple_img = pygame.transform.scale(self.apple, (80,80))
        self.spawnApple = False
        self.despawnApple= False
        self.apple_rect = self.apple_img.get_rect()
        self.appleFrame = 0
        
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
        

        if self.spawn_intervals[self.spawn_index] == 8:
            dynamic_offset = 8000
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
                self.game_over()
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

    def game_win(self):
        result = game_win(self.display)  # Call game win function that shows the screen and waits for input
        if result == 'restart':
            self.reset_game()  # Reset the game if 'restart' was chosen
        elif result == 'main_menu':
            # Assuming you have a way to handle switching to the main menu
            self.gameStateManager.set_state('menu')

    def reset_game(self):
        # Reinitialize game components
        self.__init__(self.display, self.gameStateManager)
        # Reset all game-related attributes
        self.gameStateManager.start_time = time.time()
        self.score = 0

        # Reset mobs and bosses
        self.mobs.empty()
        self.boss.empty()

        # Reset player attributes
        self.freddy = Player.spawnPlayer(self.display, 1, 300, 390)
        self.freddy.health = 800  # Reset health
        self.freddy.rect.x = 300  # Reset position
        self.freddy.rect.y = 390
        self.freddy.current_frame = 0  # Reset animation frame
        self.freddy.parabolaX = 0  # Reset any jump or movement mechanics

        # Reset game environment and state
        self.tile_map = TileMap('Main/levels/platforms/level 1 tile map.csv', tile_size=32)
        self.spawn_index = 0
        self.next_spawn_time = self.spawn_intervals[0]
        self.some_additional_offset = 100

        self.sword = Sword(self.display,self.freddy)
        
        
        
        self.run()  # Restart the game loop if necessary
  
    def gettingFired(self):
        self.display.fill((0,0,0))
        pygame.draw.rect(self.display, (255, 0, 0), (50, 50, 100, 100))
        #subtract the time spent animating from the game clock.
        #elapsed time
        font = pygame.font.SysFont('Times New Roman',30)
        text_color = (255,255,255)
        text_surface = font.render('Flame On!', True, text_color)
        self.display.blit(text_surface, (0,10))

        if self.animateIterate >= 70:
            self.freddy.rect.x += 2
            self.freddy.rect.y -= 3
            self.freddy.image = self.freddy.greenSprites[0]
        elif self.animateIterate >= 60:
            self.freddy.rect.x += 2
            self.freddy.rect.y -= 3
            self.freddy.image = self.freddy.redSprites[0]
        elif self.animateIterate >= 50:
            self.freddy.rect.x += 2
            self.freddy.rect.y -= 3
            self.freddy.image = self.freddy.greenSprites[0]
        elif self.animateIterate >= 40:
            self.freddy.rect.x += 2
            self.freddy.rect.y -= 3
            self.freddy.image = self.freddy.redSprites[0]
        elif self.animateIterate >= 35:
            self.freddy.rect.x -= 2
            self.freddy.rect.y += 3
            self.freddy.image = self.freddy.death[1]
        elif self.animateIterate >= 30:
            self.freddy.rect.x -= 2
            self.freddy.rect.y += 3
            self.freddy.image = self.freddy.death[1]
        elif self.animateIterate >= 20:
            self.freddy.rect.x -= 2
            self.freddy.rect.y += 3
            self.freddy.image = self.freddy.redSprites[0]
        elif self.animateIterate >= 10:
            self.freddy.rect.x -= 2
            self.freddy.rect.y += 3
            self.freddy.image = self.freddy.greenSprites[0]
        else:
            self.freddy.rect.x -= 2
            self.freddy.rect.y += 3
            self.freddy.image = self.freddy.redSprites[0]
        self.animateIterate -= 1
        self.display.blit(self.freddy.image, (self.freddy.rect.x - 25, self.freddy.rect.y - 15))
        if self.animateIterate == 0:
            self.heatUp = False



    def run(self):
        self.display.fill((0, 0, 0))
        pygame.draw.rect(self.display, (255, 0, 0), (50, 50, 100, 100))  # Draw a red rectangle
        self.tile_map.draw(self.display)
        current_time = time.time()
        #total time since instance of lvl1 was initialized #make clock stop when paused in game
        elapsed_time = current_time - self.start_time
        game_elapsed_time = current_time - self.start_time
        
        # Draw the background first
        self.bg.draw_bg()
        self.bg.draw_ground()
        self.update_timer()
        font = pygame.font.SysFont('Times New Roman',30)
        text_color = (255,255,255)
        text_surface = font.render('Freddy World', True, text_color)
        self.display.blit(text_surface, (0,10))
       
        #Events
        keys=pygame.key.get_pressed()
        if keys[pygame.K_w] and self.player_y == 395:
            self.jump = 1
        #Handle jump    
        if self.jump == 1:
            self.freddy.jump()
            self.jumpCount += 1
        if self.jumpCount >= 60:
            self.jump = 0
            self.jumpCount = 0
            self.freddy.rect.y = self.freddy.initial_y
        if not self.freddy.flameOn:
            self.freddy.update(keys)
        else:
            self.freddy.updateRed(keys)
            

        #Mob spawning
        if elapsed_time >= self.next_spawn_time:
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
         
        #Spawn power Up once, then update until acquired or off left side of screen
        if self.score >= 200 and self.spawnFire == False and self.despawnFire == False:
            self.powerUp_rect.x = 1300
            self.powerUp_rect.y = 420
            self.bounceVel = 3
            self.fireGrav = 1
            self.spawnFire = True
        
        
        if self.score >=300 and self.spawnApple == False and self.despawnApple == False:
            self.apple_rect.x= 1300
            self.apple_rect.y = 410
            self.spawnApple = True
            
       
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:   
            self.apple_rect.x += 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.apple_rect.x -= 5     
         
        if self.spawnApple:
            if -50 >=self.apple_rect.x:
                self.spawnApple = False
                self.despawnApple = True
                
                
        if self.freddy.rect.colliderect(self.apple_rect) and self.despawnApple!= True:
                self.despawnApple = True
                self.spawnApple = False   
                self.freddy.health +=200 
                
        if self.spawnFire:
            #once fire is off screen's left side, despawn.
            if -50 >= self.powerUp_rect.x:
                self.spawnFire = False
            #image swirl  
                self.despawnFire = True
            self.swirl = self.fireFrame//5  
            if self.swirl == 0 or self.swirl == 4:
                self.powerUp_img = self.powerUp_img1

                self.powerUp_rect.y -= self.bounceVel
            elif self.swirl == 1 or self.swirl == 5:
                self.powerUp_img = self.powerUp_img2
                self.powerUp_rect.y -= self.bounceVel-1

            elif self.swirl == 2 or self.swirl == 6:
                self.powerUp_img = self.powerUp_img3
                
            elif self.swirl == 3 or self.swirl == 7:
                self.powerUp_img = self.powerUp_img4
                self.powerUp_rect.y += self.fireGrav
            self.fireFrame += 1
            self.powerUp_rect.y += self.fireGrav
            if self.fireFrame == 40:    
                self.fireFrame = 0
                self.powerUp_rect.y = 420
                
                    
            #scroll with bg  
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:   
               self.powerUp_rect.x += 5
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.powerUp_rect.x -= 5
            
            
                
            if self.freddy.rect.colliderect(self.powerUp_rect):
                self.despawnFire = True
                self.spawnFire = False
                self.freddy.heatUp()
                self.heatUp = True    

        self.sword.update(keys) 
        
        if keys[pygame.K_LSHIFT]:
            for mob, temp_rect in temp_collision_rects:
                if self.sword.rect.colliderect(temp_rect):
                    mob.health -= 2
                    mob.speed_x+=.01
                    if mob.health == 2:
                        mob.kill()
                        self.score+=50        

        #Collision detection between fireballs and mobs
        if self.freddy.flameOn:
            for mob, temp_rect in temp_collision_rects:
                for whizbang in self.freddy.projectiles:
                    if whizbang.rect.colliderect(temp_rect):
                        mob.health -= 0.5
                        if whizbang.state == 0:
                            whizbang.start_boom()
                        if mob.health <= 5:
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
                    boss.speed_x+=.006
                    if boss.health == 2:
                        boss.kill()
                        print("You Won!!")
                        self.game_win()
                              
        for boss, temp_rects in boss_temp_collision_rects:
                if self.freddy.rect.colliderect(temp_rects):
                    self.freddy.health -= 10
                    if self.freddy.health <=0:
                        self.freddy.kill()
                        self.game_over()   
                        
        # Collision detection using temporary rects
        if keys[pygame.K_f]:
            
            for boss, temp_rects in boss_temp_collision_rects:
                if self.freddy.rect.colliderect(temp_rects):
                    # Deduct health from the specific mob that was hit 
                    boss.health -= 5
                    # Check if the mob's health is 0 or less
                    if boss.health <= 0:
                        # If so, kill the mob
                        boss.kill()
                        # Call the game win function to handle the win condition 
                        win_music('Main/music/xDeviruchi - Take some rest and eat some food!.wav')
                        self.game_win()
                        
            for mob, temp_rect in temp_collision_rects:
                if self.freddy.rect.colliderect(temp_rect):
                    mob.health -= 2
                    mob.speed_x+=.09
                    if mob.health == 2:
                        mob.kill()
                        self.score+=50        
        

        #Draw player and hit-box     
        self.display.blit(self.freddy.image, (self.freddy.rect.x - 25, self.freddy.rect.y - 15))
        pygame.draw.rect(self.display, (0, 255, 0), self.freddy.rect, 2)
        Player.draw_health_bar_player(self.display, self.freddy,100)
        #Draw fireballs
        if self.spawnFire:
            self.display.blit(self.powerUp_img, (self.powerUp_rect.x, self.powerUp_rect.y))
        if self.freddy.flameOn:
            for whizbang in self.freddy.projectiles:
                self.display.blit(whizbang.fires[whizbang.current_image], (whizbang.rect.x, whizbang.rect.y))

        if self.spawnApple:
            self.display.blit(self.apple_img, (self.apple_rect.x, self.apple_rect.y))
            
        
        #????is this for the boss fight?
        if self.bg.scroll == 10000:
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