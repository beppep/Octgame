import pygametools as pt
import pygame


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
playerTurn = 0

class Player:


    def __init__(self, x=1, y=1, layout=[1,1,0,0,0,0,0,0,0]):
        self.x=x
        self.y=y
        self.layout = layout
        players.append(self)

    def Use(self, slot):
        if(slot == 2 or slot == 3 or slot == 4):
            dirX = 1
        if(slot == 6 or slot == 7 or slot == 8):
            dirX = -1
        if(slot == 1 or slot == 2 or slot == 8):
            dirY = 1
        if(slot == 4 or slot == 5 or slot == 6):
            dirY = -1
        
        if (layout[slot] == 0):
            pass
        if (layout[slot] == 1):
            x+=dirX
            y+=dirY
        if (layout[slot] == 2):
            pass

            
player1=Player(0,0,[1,1,0,0,1,0,0,0,1,0])
player2=Player(1,2,[1,1,0,0,0,1,1,1,0,0])


pt.start(32*32, 32*18)


jump_out = False
while jump_out == False:

    if(pt.get_keypress(pygame.K_w)):
       players[playerTurn].Use(1)
       
    
    
    pt.draw_rectangle(0, 0, 32*32, 32*18, (127,127,127))
    for player in players:
        name = "Tiles/Octagame1Tiles_00.png"
        pt.show_image(image_name=name, size_x=32, size_y=32, x=player.x*32, y=player.y*32) #main body sprite

        for slot in player.layout:
            name = "Tiles/Octagame1Tiles_01.png"
            pt.show_image(image_name=name, size_x=32, size_y=32, x=player.x*32, y=player.y*32) #ROTATE
            
    
    






    pt.update()


pt.end_program()
