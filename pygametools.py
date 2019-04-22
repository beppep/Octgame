import time
import random
import pygame
import math
pygame.init()

clock = pygame.time.Clock()

class InteractiveBox():
    """
    interactive box wich can check if pressed and return bool or activate function
    """
    def __init__(self, x=100, y=100, size_x=100, size_y=100, size_text=30, color_text=(255,0,0), color_box = (255,255,255), text="not defined", centered=False, function=False):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.color_text = color_text
        self.color_box = color_box
        self.size_text = size_text
        self.text = text
        self.centered = centered
        self.function = function


    def draw(self, text=False, color_text=False, color_box=False):
        if not(text):
            text = self.text

        if not(color_text):
            color_text = self.color_text

        if not(color_box):
            color_box = self.color_box
        
        rect_x = self.x
        rect_y = self.y
        
        if self.centered:
            text_x = self.x
            text_y = self.y
        else:
            text_x = self.x + self.size_x/2.0 
            text_y = self.y + self.size_y/2.0 

            
        draw_rectangle(x=rect_x, y=rect_y, size_x=self.size_x, size_y=self.size_y, color=color_box, border=0, centered=self.centered)

        if text:
            display_text(x=text_x, y=text_y, text=text, size=self.size_text, color=color_text, centered=True)


    def pressed(self):
        if self.centered:
            rect_x = self.x - self.size_x/2.0 
            rect_y = self.y - self.size_y/2.0
        else:
            rect_x = self.x
            rect_y = self.y
            
        if get_press_in_region(key=0, x=rect_x, y=rect_y, x1=rect_x+self.size_x, y1=rect_y+self.size_y):
            return True
        return False


    def pressed_activate(self, func_variables):
        if self.centered:
            rect_x = self.x - self.size_x/2.0 
            rect_y = self.y - self.size_y/2.0
        else:
            rect_x = self.x
            rect_y = self.y
            
        if get_press_in_region(key=0, x=rect_x, y=rect_y, x1=rect_x+self.size_x, y1=rect_y+self.size_y):
            return self.function(func_variables)
        
        return False
    



def start(display_width=1000,display_height=1000, speak=False, import_pickle=False, controll=False, window=True):
    """
    start pygame by initializing it and setting up the pygame window, import extra libraries
    """
    
    if window:
        global gameDisplay
        gameDisplay = pygame.display.set_mode((display_width,display_height))

    if speak:
        global Translator
        global TemporaryFile
        global gTTS
        from googletrans import Translator
        from tempfile import TemporaryFile
        from gtts import gTTS
    if import_pickle:
        global pickle
        import pickle
    if controll:
        pass


def draw_rectangle(x=100, y=100, size_x=100, size_y=100, color=(255,0,0), border=0, centered=False):
    """
    draw a rectangle on the pygame screen
    """
    if centered:
        x = x - size_x/2
        y = y - size_y/2
    
    pygame.draw.rect(gameDisplay, color, (x, y, size_x, size_y),border)


def draw_circle(x=100, y=100, size=50, color=(255,0,0)):
    """
    draw a circle on the screen with the x, y corresponding to the center
    """
    pygame.draw.circle(gameDisplay, color, (x, y),size)


def fill(color=(0,0,0)):
    """
    fill the whole screen
    """
    
    gameDisplay.fill(color)

def rot_center(image, angle):
    """rotate a Surface, maintaining position."""

    loc = image.get_rect().center  #rot_image is not defined 
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite

def show_image(image_name=False, image=False, size_x=0, size_y=0, x=100, y=100, multipler=0, mirrorx=False, mirrory=False):
    """
    import and show image that is in your directory
    """
    if image_name:
        try:
            image = pygame.image.load(image_name)
        except:
            print("error: wrong image name, make sure to have the right name and include type, ex .png ")
            pygame.quit()
            time.sleep(100)
        
        if size_x:
            image = pygame.transform.scale(image, (size_x, size_y))
        
    if multipler:
        image_size = image.get_size()
        size_x = image_size[0]*multipler
        size_y = image_size[1]*multipler
        
        image = pygame.transform.scale(image, (size_x, size_y))
        
    elif size_x:
        image_size = image.get_size()
        size_y = int((float(size_x)/image_size[0])*image_size[1])
        
        image = pygame.transform.scale(image, (size_x, size_y))
    
    
    image=pygame.transform.flip(image,mirrorx,mirrory) #godmorgon!
    
    
    gameDisplay.blit(image,(x, y))
    #pygame.display.update()


def get_image(image_name=False, size_x=0, size_y=0, multipler=0):
    try:
        image = pygame.image.load(image_name)
    except:
        print("error: wrong image name, make sure to have the right name and include type, ex .png ")
        pygame.quit()
        time.sleep(100)
    if multipler:
        image_size = image.get_size()
        size_x = image_size[0]*multipler
        size_y = image_size[1]*multipler
        
        image = pygame.transform.scale(image, (size_x, size_y))
        
    elif size_x:
        image_size = image.get_size()
        size_y = (size_x/image_size[0])*image_size[1]
        
        image = pygame.transform.scale(image, (size_x, size_y))

    return image
    



def display_text(text="not defined", x=100, y=100, size=30, color=(255,0,0), font_type='consolas', centered=False):
    """
    display text on pygame window
    """

    if centered:
        text_x = x + - len(text)*size*0.285
        text_y = y - size*0.6
        x=int(text_x)
        y=int(text_y)
        font_type='consolas'
    
    myfont = pygame.font.SysFont(font_type, size)
    textsurface = myfont.render(text, False, color)
    gameDisplay.blit(textsurface,(x,y))


def display_non_ascii_text(text="not defined", x=100, y=100, size=30, color=(255,255,255), font_type='irohamarumikami'):
    """
    display non ascii characters on pygame window with x and y being the top left corner of first letter, default japanese
    make sure you have a font that supports the characters
    """
    
    try:
        #convertes the japanese text to unicode so that it can be displayed
        japanese_line = unicode(text, "utf-8")
        
    except UnicodeDecodeError:
        #print line_num
        print("UnicodeDecodeError: " + text)
        return False

    #displayes the characters, make sure you have a font that supports them
    display_text(text=japanese_line, x=x, y=y, size=size, color=color, font_type=font_type)
    return True




def speak(text, lang='en'):
    """
    read inserted text in target languange
    
    needs start(speak=True)
    """
    
    try:
        translator = Translator()
        #creates the audio
        tts = gTTS(text=translator.translate(text, dest=lang).text, lang=lang)
        
        #creates a temporary file so that audio can be loaded with pygame
        sf = TemporaryFile()
        tts.write_to_fp(sf)
        sf.seek(0)
        
        #loades the audio with pygame
        pygame.mixer.music.load(sf)

        #plays the audio
        pygame.mixer.music.play()
    except Exception:
        raise

def get_speaker_playing():
    """
    see if the pygame.mixer.music is playing
    """

    if pygame.mixer.music.get_busy():
        return True
    else:
        return False



def save_data(data, filename="python_saves"):
    """
    save data to file using pickle
    keep in mind that this will overwrite everything in that file

    needs start(install_pickle=True)
    """

    try:
        pickle_info = pickle.dumps(data)
        with open(filename, 'w+') as myfile:
            myfile.write(pickle_info)
    except NameError:
        print("ERROR: you have not enabled pickle in start function")
        raise


def load_data(filename):
    """
    load saved data from file
    make sure the data is pickled, can be done by saving it using toolbox

    needs start(install_pickle=True)
    """
    try:
        with open(filename, 'r') as myfile:
            pickle_info = myfile.read()

        data = pickle.loads(pickle_info)
        return data
    except NameError:
        print("ERROR: you have not enabled pickle in start function")
        raise
    



def get_mouse_pos():
    """
    return mouse pos on the pygame window
    """
    
    pygame.event.get()
    x, y = pygame.mouse.get_pos()
    return x, y


def get_left_click():
    """
    see if left mouse button is pressed down
    """
    
    mouse_press = pygame.mouse.get_pressed()
    if mouse_press[0]:
        return True
    else:
        return False


def get_right_click():
    """
    see if right mouse button is pressed down
    """
    
    mouse_press = pygame.mouse.get_pressed()
    if mouse_press[2]:
        return True
    else:
        return False


def get_mouse_press():
    """
    see if right or left mouse button is pressed down
    """
    mouse_press = pygame.mouse.get_pressed()
    if mouse_press[2] or mouse_press[0]:
        return True
    else:
        return False


def get_press_in_region(key=0, x=0, y=0, x1=100, y1=100):
    """
    see if a mouse is pressed down in specific region of the pygame screen, key: 0:left click, 1:middle click, 2:right click
    """
    
    if key < 3:
        press = pygame.mouse.get_pressed()
    else:
        press = pygame.key.get_pressed()
    if press[key]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if x < mouse_x < x1 and y < mouse_y < y1:
            return True
    return False
    

def get_keypress(key=pygame.K_a):
    """
    see if a key on the keyboard is pressed down

    usage:
    insert key=pygame.K_ followed by desired key, keys other than the numbers and letters are all caps, ex. K_SPACE, K_ESC
    """
    
    keys = pygame.key.get_pressed()
    if keys[key]:
        return True
            
    return False




def sustain(end_script=True, tid=100000000000):
    """
    keep pygame window alive and the script idle for infinite or set period of time
    """
    
    quit_loop = time.time() + tid
    while quit_loop > time.time():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_loop = time.time()
    if end_script:
        end_program()


def update():
    """
    update the screen, all eventes (keyboard, mouse etc.) and make sure that pygame window dont crash
    """
    
    jump_out = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jump_out = True
            
    if jump_out:
        end_program()
        
    pygame.display.update()


def end_program():
    """
    close pygame window and end the program
    """
    
    print("ending program")
    pygame.display.quit()
    print("pygame shut down")
    quit()




def rotate_around_point(x=100, y=100, rotate_center_x=200, rotate_center_y=200, angle=0):
    """
    rotate around a point
    """
    
    relative_x = x - rotate_center_x + 0.001
    relative_y = y - rotate_center_y + 0.001

    angle = math.radians(angle)
                                                                                                                                                                                                                                                                                                                                                                                                                            

    if relative_y < 0:
        angle_in_x = (math.atan((relative_x/relative_y)) + angle + (math.pi))%(2*math.pi)
    else:
        angle_in_x = (math.atan((relative_x/relative_y)) + angle + (2*math.pi))%(2*math.pi)
    
    hyp = (relative_x*relative_x + relative_y*relative_y)**(0.5)

    rotated_relative_x = math.sin(angle_in_x)*hyp
    rotated_relative_y = math.cos(angle_in_x)*hyp
    
    rotated_x, rotated_y = rotated_relative_x + rotate_center_x, rotated_relative_y + rotate_center_y

    return rotated_x, rotated_y
