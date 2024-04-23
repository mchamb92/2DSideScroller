
import pygame
#"Main/Level1_img/weapons/18.png"
class Sword():
    def __init__(self,display,freddy):
        super().__init__()
        
        self.display = display
        self.freddy = freddy
        self.sword_img = pygame.image.load("Main/Level1_img/weapons/18.png").convert_alpha()
        self.scaled_width = 20  # Desired width after scaling
        self.scaled_height =90  # Desired height after scaling
        
        self.sword_img1 = pygame.transform.scale(self.sword_img, (self.scaled_width, self.scaled_height))
        self.sword_img1 = pygame.transform.rotate(self.sword_img1, 280)
        self.rect = self.sword_img1.get_rect()
        
        
        print('Sword dimensions: ', self.rect.width, ',', self.rect.height)
        self.sword_img2 = pygame.transform.rotate(self.sword_img1, 330)
        self.sword_img3 = pygame.transform.rotate(self.sword_img2, 30)
        
        
        self.sword_img4 = pygame.transform.rotate(self.sword_img1, 320)
        self.sword_img5 = pygame.transform.rotate(self.sword_img1,320)
        self.sword_img6 = pygame.transform.rotate(self.sword_img1,320)
        
        self.SwordFrame = 0
        
    def update(self,keys):
        sword_x_offset = 25  # Adjust so the sword appears correctly relative to Freddy
        sword_y_offset = 30  # Adjust based on your game's needs
        
        self.rect.x = self.freddy.rect.x + sword_x_offset
        self.rect.y = self.freddy.rect.y + sword_y_offset
       
        if keys[pygame.K_LSHIFT]:
            if self.SwordFrame <= 20:
                self.display.blit(self.sword_img1, (self.rect.x, self.rect.y))
                self.SwordFrame += 1
            elif self.SwordFrame <=40:
                self.display.blit(self.sword_img2, (self.rect.x, self.rect.y))
                self.SwordFrame +=1 
            else:
                sword_x_offset = 5
                sword_y_offset = -10
                self.rect.x = self.freddy.rect.x + sword_x_offset
                self.rect.y = self.freddy.rect.y + sword_y_offset
                self.SwordFrame +=1
                self.display.blit(self.sword_img3, (self.rect.x, self.rect.y))
                if self.SwordFrame == 60:
                    self.SwordFrame =21
           
                
            
            
                
        