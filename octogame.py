import pygametools as pt
import pygame


players=[]

class Player:
    
    SPEED=0.1


    def __init__(self, x=500, y=450, facing_right=True):
        self.x=x
        self.y=y    
        self.facing_right=facing_right
        players.append(self)


player1= Player()


pt.start(32*32, 32*18)


jump_out = False
while jump_out == False:

    if(pt.get_keypress(pygame.K_a)):
        player1.x-=Player.SPEED
        player1.facing_right=False
    if(pt.get_keypress(pygame.K_d)):
        player1.x+=Player.SPEED
        player1.facing_right=True
    

    pt.draw_rectangle(0, 0, 32*40, 32*20, (127,127,127))
    pt.draw_rectangle(0, 450, 1000, 50, (0,0,0))
    for player in players:
        name = "C:/Users/brorb/Documents/python/Octogame/Tiles/Octagame1Tiles_00.png"
        pt.show_image(image_name=name, size_x=32, size_y=32, x=0, y=0, multipler=0)
    
    


    pt.update()






pt.end_program()
