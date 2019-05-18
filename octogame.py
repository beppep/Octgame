#import pygametools as pt
import pygame
import math
import time
import random

controls=[pygame.K_s,pygame.K_w,pygame.K_e,pygame.K_d,pygame.K_c,pygame.K_x,pygame.K_z,pygame.K_a,pygame.K_q]

imageList = []
coreImageList = []


for i in range(15):
	name = "Tiles/Octagame1Tiles_" + "0"*(i<10) + str(i) + ".png"
	imageList.append(pygame.image.load(name))
for i in range(4):
	name = "Tiles/Octagame2Tiles_" + str(i) + ".png" #lol nloel dom heter inte 00 01 här
	coreImageList.append(pygame.image.load(name))

#8 1 2
#7 0 3
#6 5 4


#0=Broken
#1=Wheel
#2=Shield
#3=Laser
#4=Teleport
#5=BackBurner™
#6=Borr
#7=Bomb





#0=broken?
#1=spin right
#2=spin left
#3=flip horizontal

players = []
projectiles = []
global playerTurn
global spacePressed
playerTurn = False

spacePressed = True
class Projectile:
    """docstring for Projectile"""
    def __init__(self,x, y,projectile_type,lifespan,dirX=0,dirY=0):
        self.life = lifespan
        self.projectile_type = projectile_type
        self.x=x
        self.y=y
        self.dirX=dirX
        self.dirY=dirY
        self.owner=players[playerTurn]
        projectiles.append(self)
        

    def aging(self):
        self.life-=1
        if(not isInObject(self.x+self.dirX,self.y+self.dirY)):
            self.x+=self.dirX
            self.y+=self.dirY
        if(not self.life):
            self.explode()

    def explode(self):
        if(self.projectile_type=="bomb"):
            pygame.draw.rect(gameDisplay,(255,100,120),[32*(self.x-1),32*(self.y-1),32*3,32*3],0)
            for i in range(1,8+1):
                dirX,dirY = slotToDir(i)
                newx,newy = [dirX+self.x,dirY+self.y]
                for player in players:
                    if(player.x==newx and player.y==newy):
                        player.hurt(oppositeSlot(dirToSlot(dirX,dirY)))
            projectiles.remove(self)
        if(self.projectile_type=="teleport"):
            self.owner.x=self.x
            self.owner.y=self.y
            projectiles.remove(self)
                


            

        
class Player:

    def __init__(self, x=1, y=1, layout=False):
        if(not layout):
            self.layout=[1]+[random.randint(1,7) for i in range(8)]
        else:
            self.layout = layout
        self.x=x
        self.y=y
        
        self.dirX=0
        self.dirY=0
        
        players.append(self)

    def hurt(self,slot):
        print("Hurt")
        if(self.layout[slot] == 2):
            print("Ha, shield")
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
        global spacePressed
        opponent = players[not playerTurn]
        spacePressed=False
        #print("Use","playerturn", playerTurn,"slot",slot,"weapon",self.layout[slot])
        #SET DIRECTIONS
        
        self.dirX,self.dirY=slotToDir(slot)
        newx = self.x + self.dirX
        newy = self.y + self.dirY

        #DO ACTION

        if(not(self.dirX==0 and self.dirY==0)):

            #DO WEAPON ACTION
            
            if (self.layout[slot] == 0): #BROKEN
                pass
            if (self.layout[slot] == 1): #WHEEL
                
                if(newy>=0 and newy<18 and newx>=0 and newx<32 and not(isInObject(newx,newy))):
                    self.x = newx
                    self.y = newy
                    #print("move",dirX,dirY)
            if (self.layout[slot] == 3): #GUN
                #print("shoot")

                pygame.draw.line(gameDisplay,(255,100,120),[self.x*32+16,self.y*32+16],[self.x*32+self.dirX*32*32+16,self.y*32+self.dirY*32*32+16],2)
                if(math.atan2(-self.dirY,-self.dirX) == math.atan2(self.y-opponent.y,self.x-opponent.x)):
                    opponent.hurt(oppositeSlot(slot))

            if (self.layout[slot] == 4): #Teleport
                if(not isInObject(self.x + self.dirX, self.y + self.dirY)):
                    Projectile(self.x + self.dirX, self.y + self.dirY,"teleport",3,self.dirX,self.dirY)        
            

            if (self.layout[slot] == 5): #BACKBURNER™
                renewx = self.x - self.dirX
                renewy = self.y - self.dirY
                if(renewy>=0 and renewy<18 and renewx>=0 and renewx<32 and not(isInObject(newx,newy))):
                    self.x = renewx
                    self.y = renewy

            if (self.layout[slot] == 6): #MELEE
                pygame.draw.rect(gameDisplay,(255,100,120),[32*(self.x+self.dirX),32*(self.y+self.dirY),32,32],0)
                if(newx==opponent.x and newy==opponent.y):
                    opponent.hurt(oppositeSlot(slot))
                    opponent.hurt(oppositeSlot(slot))

            if (self.layout[slot] == 7): #BOMB
                if(isInObject(self.x + self.dirX*2, self.y + self.dirY*2)):
                    Projectile(self.x + self.dirX*2, self.y + self.dirY*2,"bomb",3)


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
        playerTurn = not playerTurn
        
def rotateList(l,iterations): 
    for i in range(iterations):
        l=[l.pop(0)]+[l[j-1] for j in range(len(l))]
    return l # returns rotated list

def flipList(l):
    return [l.pop(0)] + [l[len(l)-j-4] for j in range(len(l))]

def slotToDir(slot):
    datas = [(0,0),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)] 
    return( datas[slot] )

def dirToSlot(dirX,dirY):
    datas = [(0,0),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)] 
    return datas.index((dirX,dirY))

def isInObject(x,y):
    for obj in projectiles+players:
        if(obj.x==x and obj.y==y):
            return True
   # for obj in players:
    #    if(obj.x==x and obj.y==y):
    #        return True
    return False

def oppositeSlot(slot):
    return (slot-4-1)%8+1

player1=Player(2,1)
player2=Player(1,2)


global gameDisplay
gameDisplay = pygame.display.set_mode((32*32, 32*18))

jump_out = False
while jump_out == False:

    #INPUT
    bg_color=50*(spacePressed)+150
    gameDisplay.fill([bg_color]*3)
    keys = pygame.key.get_pressed()
    for i in range(len(controls)):

    	if(keys[controls[i]] and spacePressed):
    		#print("slot", i)
    		players[playerTurn].use(i)
    if((not spacePressed) and keys[pygame.K_SPACE]):
        spacePressed = True
        for projectile in projectiles:
            projectile.aging()


       		
       
    #GRAPHICS
    


    #GRID
    g_color=50*(spacePressed)+100
    for i in range(33):
    	pygame.draw.line(gameDisplay,(g_color,g_color,g_color),[i*32-1,0],[i*32-1,32*18],2)
    	if(i<19):
    		pygame.draw.line(gameDisplay,(g_color,g_color,g_color),[0,i*32-1],[32*32,32*i-1],2)


    #PLAYERS
    for player in players:
        
        if(playerTurn== players.index(player)):
            gameDisplay.blit(imageList[0],(player.x*32, player.y*32)) #octagon         
        else:
            gameDisplay.blit(coreImageList[0],(player.x*32, player.y*32)) #octagon

        
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

    for projectile in projectiles:
        gameDisplay.blit(imageList[0],(projectile.x*32, projectile.y*32))


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
