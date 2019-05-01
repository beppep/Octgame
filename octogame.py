#import pygametools as pt
import pygame
import math
import time

name = "Tiles/Octagame1Tiles_00.png"
imageCore = pygame.image.load(name)
name = "Tiles/Octagame1Tiles_01.png"
imageWheel = pygame.image.load(name)
name = "Tiles/Octagame1Tiles_02.png"
imageWheel2 = pygame.image.load(name)

#8 1 2
#7 0 3
#6 5 4


#0=broken
#1=wheel
#2=
#3=
#4=


#0=broken?
#1=spin right
#2=spin left

players = []
global playerTurn
playerTurn = 0



class Player:

    def __init__(self, x=1, y=1, layout=[1,1,0,0,0,0,0,0,0]):
        self.x=x
        self.y=y
        self.layout = layout
        
        players.append(self)

    def Use(self, slot):
        global playerTurn

        #SET DIRECTIONS
        
        dirX=0
        dirY=0
        if(slot == 2 or slot == 3 or slot == 4):
            dirX = 1
        if(slot == 6 or slot == 7 or slot == 8):
            dirX = -1
        if(slot == 1 or slot == 2 or slot == 8):
            dirY = -1
        if(slot == 4 or slot == 5 or slot == 6):
            dirY = 1

        #DO ACTION

        if(not(dirX==0 and dirY==0)):

            #DO WEAPON ACTION
            
            if (self.layout[slot] == 0):
                pass
            if (self.layout[slot] == 1):
                self.x+=dirX
                self.y+=dirY
                print("move",dirX,dirY)
            if (self.layout[slot] == 2):
                pass

        else:

            #DO CORE ACTION

            if(self.layout[slot] == 0):
                
                
        #END TURN
        
        time.sleep(2)
        playerTurn=1-playerTurn
        
            
player1=Player(5,7,[1,1,1,1,1,0,1,1,1,0])
player2=Player(1,2,[1,1,0,0,0,1,1,1,0,0])


global gameDisplay
gameDisplay = pygame.display.set_mode((32*32, 32*18))

jump_out = False
while jump_out == False:

    #INPUT
    
    keys = pygame.key.get_pressed()
    
    if(keys[pygame.K_s]):
       players[playerTurn].Use(0)
    if(keys[pygame.K_w]):
       players[playerTurn].Use(1)
    if(keys[pygame.K_e]):
       players[playerTurn].Use(2)
    if(keys[pygame.K_d]):
       players[playerTurn].Use(3)
    if(keys[pygame.K_c]):
       players[playerTurn].Use(4)
    if(keys[pygame.K_x]):
       players[playerTurn].Use(5)
    if(keys[pygame.K_z]):
       players[playerTurn].Use(6)
    if(keys[pygame.K_a]):
       players[playerTurn].Use(7)
    if(keys[pygame.K_q]):
       players[playerTurn].Use(8)
       
    #GRAPHICS
    
    gameDisplay.fill((127,127,127))

    for player in players:
        
        
        gameDisplay.blit(imageCore,(player.x*32, player.y*32))
        
        
        for n in range(len(player.layout)):
            
            if(n%2==1 and player.layout[n]>0):
                imageTemp = pygame.transform.rotate(imageWheel, 45*(n-1))
                gameDisplay.blit(imageTemp,(player.x*32, player.y*32))
            
            elif(player.layout[n]>0):
                imageTemp = pygame.transform.rotate(imageWheel2, 45*(n))
                gameDisplay.blit(imageTemp,(player.x*32, player.y*32))






    #pt.update()
    jump_out = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jump_out = True
    if jump_out:
        pygame.display.quit()
        quit()
    pygame.display.update()



pt.end_program()
