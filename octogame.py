#import pygametools as pt
import pygame
import math
import time

controls=[pygame.K_s,pygame.K_w,pygame.K_e,pygame.K_d,pygame.K_c,pygame.K_x,pygame.K_z,pygame.K_a,pygame.K_q]

imageList = []
coreImageList = []


for i in range(13):
	name = "Tiles/Octagame1Tiles_" + "0"*(i<10) + str(i) + ".png"
	imageList.append(pygame.image.load(name))
for i in range(4):
	name = "Tiles/Octagame2Tiles_" + str(i) + ".png" #lol nloel dom heter inte 00 01 här
	coreImageList.append(pygame.image.load(name))

#8 1 2
#7 0 3
#6 5 4


#0=broken
#1=wheel
#2=Shield
#3=Laser
#4=


#0=broken?
#1=spin right
#2=spin left
#3=flip horizontal

players = []
global playerTurn
playerTurn = 0



class Player:

    def __init__(self, x=1, y=1, layout=[1,1,0,0,0,0,0,0,0]):
        self.x=x
        self.y=y
        self.layout = layout
        self.dirX=0
        self.dirY=0
        
        players.append(self)

    def hurt(self,slot):
        if(self.layout[slot] == 2):
            pass
        elif(self.layout[slot] == 0):
            self.die()
        else:
            self.layout[slot] = 0

    def die(self):
        print("Death")
        #players.pop(players.index(self))


    #USE USE USE USE USE USE USE USE USE USE USE USE USE 
    def use(self, slot):
        global playerTurn
        global gameDisplay
        opponent = players[1-playerTurn]
        #print("Use","playerturn", playerTurn,"slot",slot,"weapon",self.layout[slot])
        #SET DIRECTIONS
        
        self.dirX=0
        self.dirY=0
        if(slot == 2 or slot == 3 or slot == 4):
            self.dirX = 1
        if(slot == 6 or slot == 7 or slot == 8):
            self.dirX = -1
        if(slot == 1 or slot == 2 or slot == 8):
            self.dirY = -1
        if(slot == 4 or slot == 5 or slot == 6):
            self.dirY = 1
        #DO ACTION

        if(not(self.dirX==0 and self.dirY==0)):

            #DO WEAPON ACTION
            
            if (self.layout[slot] == 0):
                pass
            if (self.layout[slot] == 1):
                newx = self.x + self.dirX
                newy = self.y + self.dirY
                if(newy>=0 and newy<18 and newx>=0 and newx<32 and not(newy == players[1-playerTurn].y and newx == players[1-playerTurn].x)):
                    self.x = newx
                    self.y = newy
                    #print("move",dirX,dirY)
            if (self.layout[slot] == 3):
                #print("shoot")

                pygame.draw.line(gameDisplay,(255,100,120),[self.x*32+16,self.y*32+16],[self.x*32+self.dirX*32*32+16,self.y*32+self.dirY*32*32+16],2)
                opponent = players[1-playerTurn]
                if(math.atan2(-self.dirY,-self.dirX) == math.atan2(self.y-opponent.y,self.x-opponent.x)):
                    opponent.hurt((slot+4-1)%8+1)
                    print("Hurt")
                

        else:

            #DO CORE ACTION

            if(self.layout[slot] == 1):
                self.layout = rotateList(self.layout,1)
            if(self.layout[slot] == 2):
                self.layout = rotateList(self.layout,7)
            if(self.layout[slot] == 3):
                self.layout = flipList(self.layout)
                
        #END TURN
        
        #time.sleep(1) #updatera screeen innan sleep
        playerTurn=1-playerTurn
        
def rotateList(l,iterations): 
    for i in range(iterations):
        l=[l.pop(0)]+[l[j-1] for j in range(len(l))]
    return l # returns rotated list

def flipList(l):
    return [l.pop(0)] + [l[len(l)-j-4] for j in range(len(l))]





player1=Player(5,7,[3,1,2,3,4,0,0,0,0])
player2=Player(1,2,[2,3,2,4,1,1,2,3,4])


global gameDisplay
gameDisplay = pygame.display.set_mode((32*32, 32*18))

jump_out = False
while jump_out == False:

    #INPUT
    gameDisplay.fill((200,200,200))
    keys = pygame.key.get_pressed()
    for i in range(len(controls)):
    	if(keys[controls[i]]):
    		#print("slot", i)
    		players[playerTurn].use(i)
       		
       
    #GRAPHICS
    
    

    #GRID
    g_color=150
    for i in range(33):
    	pygame.draw.line(gameDisplay,(g_color,g_color,g_color),[i*32-1,0],[i*32-1,32*18],2)
    	if(i<19):
    		pygame.draw.line(gameDisplay,(g_color,g_color,g_color),[0,i*32-1],[32*32,32*i-1],2)


    #PLAYERS
    for player in players:
        
        
        gameDisplay.blit(imageList[0],(player.x*32, player.y*32)) #octagon
        
        
        for n in range(len(player.layout)):
            if(n!=0):
                if(n%2==1 and player.layout[n]>0):
                    imageTemp = pygame.transform.rotate(imageList[player.layout[n]*2-1], -45*(n-1))
                    gameDisplay.blit(imageTemp,(player.x*32, player.y*32))
            
                elif(player.layout[n]>0):
                    imageTemp = pygame.transform.rotate(imageList[player.layout[n]*2], -45*(n))
                    gameDisplay.blit(imageTemp,(player.x*32, player.y*32))

            else:
                gameDisplay.blit(coreImageList[player.layout[0]],(player.x*32, player.y*32))




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
