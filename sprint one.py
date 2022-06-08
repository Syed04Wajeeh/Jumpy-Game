#Jumpy game
#Coders: Wajeeh, Isha, Vishvah


import pygame
from pygame.locals import *
import sys
import random
import os

#Initiating the nessesary pygame modules
pygame.init()
pygame.font.init()
pygame.mixer.init()

score = 0

#Creating fonts for the game to use later on
buttonfont = pygame.font.SysFont("verdana",16) 
font = pygame.font.SysFont("verdana", 30)

#Creating the actual text for the game to draw
buttontext = buttonfont.render("Restart" , True , (255,255,255))
text = font.render("Score:" + str(score), True, (255, 255, 255)) 
scoreendtext = font.render("Your final score:" + str(score), True, (255, 0, 0)) 
clock = pygame.time.Clock()

vec = pygame.math.Vector2

GAMESTATE = 0

#Height and width of the screen
HEIGHT = 600
WIDTH = 400

#Physics variables
ACC = .5
FRIC = -0.07

#Creating the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The story of")
background = pygame.image.load("background.png")

#Creating sprite groups to contain all the sprites of the game
#draw all sprites at once
sprite_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
stapler_group = pygame.sprite.Group()
paper_group = pygame.sprite.Group()
book_group = pygame.sprite.Group()
table_group = pygame.sprite.Group()

#player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.sprites = []
        self.sprites.append(pygame.image.load("character.png"))
        self.sprites.append(pygame.image.load("jumpingworm.png"))
        self.surf = pygame.Surface((30,1))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()

        self.jumping = False
        self.pos = vec((200, 570))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    #Control x position of the player using keys
    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
        self.rect.midbottom = self.pos

    #allows the player to jump
    def jump(self):
        hits = pygame.sprite.spritecollide(player, platform_group, False)

        #prevents double jumping
        if hits and not self.jumping:
            boing = pygame.mixer.Sound("boing.wav")
            boing.play()
            self.jumping = True
            self.vel.y = - 17 
            x = 1
            
        self.rect.midbottom = self.pos

    def checkstapler(self):
        hits = pygame.sprite.spritecollide(player, stapler_group, False)

        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = - 17

    def checkpaper(self):

            
        hits = pygame.sprite.spritecollide(player, paper_group, False)

        if hits and not self.jumping:
            
            jumpedon = True

        if hits and not self.jumping and jumpedon:
            pygame.sprite.spritecollide(player, paper_group, True)

        

    #code to animate and refresh the players position
    def update(self):

        hits = pygame.sprite.spritecollide(player, platform_group, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
                                      
        if self.vel.y == 0.0 and self.jumping == False:
            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]
                    
        elif self.vel.y < 0 or self.vel.y > 0 :
            self.current_sprite = 1
            self.image = self.sprites[self.current_sprite]

    def animation(self):
        
            if self.jumping:
                self.current_sprite += 1
                if self.current_sprite >= len(self.sprites):
                    self.current_sprite = 0
                self.image = self.sprites[self.current_sprite]
                
class platform(pygame.sprite.Sprite):
    def __init__(self, width, x_pos, y_pos, image_path):
        super().__init__()
        self.surf = pygame.Surface((width, 30))
        self.image = pygame.image.load(image_path)
        self.rect = self.surf.get_rect(center = (x_pos, y_pos))
        

class button(pygame.sprite.Sprite):
    def __init__(self, screen, color, x_pos, y_pos, width, height):
        super().__init__()
        pygame.draw.rect(screen, color, [x_pos, y_pos, width, height])

#class for level generation beyond the initial max y value
def levelgeneration():
    while len(platform_group) < 6:

        #creates a random platform of 4 types: book, desk, paper, or stapler
        y = (random.randint(1,4))
        if y == 1:
            platform_type = "book.png"
            newplat = platform(140, random.randint(1, WIDTH), random.randint(-45, -1), platform_type)
            
            platform_group.add(newplat)
            sprite_group.add(newplat)
            book_group.add(newplat)
            
        elif y == 2:
            platform_type = "desk.png"
            newplat = platform(140, random.randint(1, WIDTH), random.randint(-45, -1), platform_type)
                         
            platform_group.add(newplat)
            sprite_group.add(newplat)
            table_group.add(newplat)
            
        elif y == 3:
            platform_type = "paper.png"
            newplat = platform(140, random.randint(1, WIDTH), random.randint(-45, -1), platform_type)
            
            platform_group.add(newplat)
            sprite_group.add(newplat)
            paper_group.add(newplat)
            
        else:
            platform_type = "stapler.png"
            newplat = platform(140, random.randint(1, WIDTH), random.randint(-45, -1), platform_type)
            
            platform_group.add(newplat)
            sprite_group.add(newplat)
            stapler_group.add(newplat)



GAMESTATE = 1
restart = 0

while restart == 0:
    print("restarted")
    restart = 1
    #empties the sprites in the groups on restart
    sprite_group.empty()
    platform_group.empty()
    
    score = 0

    #initiates the player, as well as the floor and a starting floating platform
    player = Player()

    plat1 = platform(140, random.randint(1, WIDTH), 400, "book.png")       
    floor = platform(WIDTH, WIDTH/2, HEIGHT , "floor.png")

    #adding previous sprites to group
    sprite_group.add(player)
    sprite_group.add(floor)
    sprite_group.add(plat1)

    platform_group.add(floor)
    platform_group.add(plat1)

    #creates platforms equal to the amount of times looped
    for x in range (3):
        y = (random.randint(1,4))
        if y == 1:
            platform_type = "book.png"
            schoolplatform = platform(140, random.randint(1, WIDTH), random.randint(150, 240), platform_type)
            platform_group.add(schoolplatform)
            sprite_group.add(schoolplatform)
            book_group.add(schoolplatform)
            
        elif y == 2:
            platform_type = "desk.png"
            schoolplatform = platform(140, random.randint(1, WIDTH), random.randint(150, 240), platform_type)
            platform_group.add(schoolplatform)
            sprite_group.add(schoolplatform)
            table_group.add(schoolplatform)
            
        elif y == 3:
            platform_type = "paper.png"
            schoolplatform = platform(140, random.randint(1, WIDTH), random.randint(150, 240), platform_type)
            platform_group.add(schoolplatform)
            sprite_group.add(schoolplatform)
            paper_group.add(schoolplatform)
            
        else:
            platform_type = "stapler.png"
            schoolplatform = platform(140, random.randint(1, WIDTH), random.randint(150, 240), platform_type)
            platform_group.add(schoolplatform)
            sprite_group.add(schoolplatform)             
            stapler_group.add(schoolplatform)
   
    while True:
        if restart == 0:
            break
##        
##        while GAMESTATE == 0:
##            if restart == 0:
##                break
##            
        while GAMESTATE == 1:
            if restart == 0:
                break

            #death sequence
            clock.tick(60)
            if player.pos.y > (HEIGHT + 10):
                death_sound = pygame.mixer.Sound("death.wav")
                death_sound.play()
                GAMESTATE = 2
                break

            #score text
            text = font.render("Score:" + str(score), True, (0, 0, 0))
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:    
                    if event.key == pygame.K_SPACE:
                        player.jump()

            #scrolls the screen (actually moves all sprites down)          
            if player.rect.top <= HEIGHT/3: 
                player.pos.y += abs(player.vel.y)
                for plat in platform_group:
                    plat.rect.y += abs(player.vel.y)
                    if plat.rect.top >= HEIGHT:
                        plat.kill()
                        score += 1

            levelgeneration()

            pygame.display.flip()

            screen.blit(background, (0,0))
            screen.blit(text, (0, 0))
            
            player.move()
            player.checkstapler()
            player.checkpaper()
            player.update()
            
            sprite_group.draw(screen)

        #death sequence
        if GAMESTATE == 2:
            if restart == 0:
                break
            clock.tick(60)
            screen.fill((0,0,0))
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                        
            
            buttontext = buttonfont.render("Restart" , True , (255,255,255))
            text = font.render("GAME OVER", True, (255, 0, 0))
            scoreendtext = font.render("Your final score:" + str(score), True, (255, 0, 0))
            
            screen.blit(text, (WIDTH/4, HEIGHT/3))
            screen.blit(scoreendtext, (WIDTH/5, HEIGHT/6))
        
            Button = button(screen, (255, 0, 0), 150, 375, 100, 50)
            screen.blit(buttontext, (170, 387))
            pygame.display.flip()

            while True:
                if restart == 0:
                    break
                clock.tick(60)
                mouse = pygame.mouse.get_pos()
                for event in pygame.event.get():

                    if restart == 0:
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:

                      if 150 <= mouse[0] <= 250 and 375 <= mouse[1] <= 425:

                          restart = 0
                          GAMESTATE = 1
                          print(restart)
                          break

                            
                            
                      
clock.tick(60)

