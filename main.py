import pygame
import sys
import random
import time

pygame.init()

# globals
SCREEN_WIDTH = 635
SCREEN_HEIGHT = 435
BLOCK_WIDTH = 15
BLOCK_HEIGHT = 15
DRAW_WIDTH = 100
DRAW_HEIGHT = 100
global bomb_counter
bomb_counter = 99
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Minesweeper")
background = pygame.image.load("./Sprites/background.png").convert()

# icons
full_block = pygame.image.load("./Sprites/full_block.png").convert()
empty_block = pygame.image.load("./Sprites/empty_block.png").convert()
one_block = pygame.image.load("./Sprites/1_block.png").convert()
two_block = pygame.image.load("./Sprites/2_block.png").convert()
three_block = pygame.image.load("./Sprites/3_block.png").convert()
four_block = pygame.image.load("./Sprites/4_block.png").convert()
five_block = pygame.image.load("./Sprites/5_block.png").convert()
six_block = pygame.image.load("./Sprites/6_block.png").convert()
seven_block = pygame.image.load("./Sprites/7_block.png").convert()
eight_block = pygame.image.load("./Sprites/8_block.png").convert()
boom_block = pygame.image.load("./Sprites/boom_block.png").convert()
bomb_block = pygame.image.load("./Sprites/bomb_block.png").convert()
flag_block = pygame.image.load("./Sprites/flag_block.png").convert()
bomb_for_head = pygame.image.load("./Sprites/bomb_for_head.png").convert_alpha()
bomb_for_head_rect = bomb_for_head.get_rect(center = (35,50))
clock_for_head = pygame.image.load("./Sprites/clock_for_head.png").convert_alpha()
happy_face = pygame.image.load("./Sprites/happy_face.png").convert_alpha()
happy_face_rect = happy_face.get_rect(center = (317,50))
sad_face = pygame.image.load("./Sprites/sad_face.png").convert_alpha()
sad_face_rect = sad_face.get_rect(center = (317,50))

class Block:
    """ Coordinates - x,y | status of the block (empty, 1-8 numbers, fullblock, bomb, flag, hovered mouse) | image(icon of the block). """
    def __init__(self,x,y,status,image):
        self.x = x
        self.y = y
        self.status = status
        self.image = image

def surrounding_blocks(block_list, block):
    """ Returns a list with all surrounding blocks of a given block """
    return [item for item in block_list if (item.x + 20 == block.x and item.y + 20 == block.y) or 
        (item.x == block.x and item.y + 20 == block.y) or (item.x - 20 == block.x and item.y + 20 == block.y) or 
        (item.x - 20 == block.x and item.y == block.y) or (item.x - 20 == block.x and item.y - 20 == block.y) or 
        (item.x == block.x and item.y - 20 == block.y) or (item.x + 20 == block.x and item.y - 20 == block.y) or
        (item.x + 20 == block.x and item.y == block.y)]

def set_block_status(block, numberOfBombs):
    """ Sets a single block status according to the number of surrounding bombs. Returns the block with the changed status. """
    if numberOfBombs == 0:
        block.status = "empty"
    elif numberOfBombs == 1:
        block.status = "one"
    elif numberOfBombs == 2:
        block.status = "two"
    elif numberOfBombs == 3:
        block.status = "three"
    elif numberOfBombs == 4:
        block.status = "four"
    elif numberOfBombs == 5:
        block.status = "five"
    elif numberOfBombs == 6:
        block.status = "six"
    elif numberOfBombs == 7:
        block.status = "seven"
    elif numberOfBombs == 8:
        block.status = "eight"
    return block

def initialize_all_numbers(block_list):
    """Initialize valid status for all blocks. Returns a List with all blocks initiliazed."""
    new_list = []
    i=0
    for block in block_list:
        # check if the block is a bomb
        if block.status == "bomb":
            new_list.append(block)
            i+=1
            continue
        # find all surrounding blocks
        surrBlocks = surrounding_blocks(block_list,block) 
        numberOfBombs = 0
        for item in surrBlocks:
            if item.status == "bomb":
                numberOfBombs+=1
        new_list.append(set_block_status(block_list[i],numberOfBombs))
        i+=1
    return new_list 

def define_all_fields():
    """ Initializes all block with coordinates, status and image. Returns a List with all blocks."""
    block_list = []
    # Initialize all blocks 
    for DRAW_WIDTH in range(20,620,20):
        for DRAW_HEIGHT in range(100,420,20):
            block_list.append(Block(DRAW_WIDTH,DRAW_HEIGHT,"fullblock",full_block))

    # Initialize all bombs - 99
    randList = random.sample(range(0,480),99)
    for num in randList:
        block_list[num].status = "bomb"

    # Initialize all number/empty fields
    block_list = initialize_all_numbers(block_list)

    return block_list

def find_position(x,y,block_list):
    """ Finds and returns the position(in the block array) of the block clicked by the mouse. """
    i=0
    for block in block_list:
        if x>block.x and x<block.x + 20 and y>block.y and y<block.y + 20:
            break
        i+=1
    return i

def flip_all_empty_blocks(block_list,index):
        """ When an empty block is clicked, find and open(flip) all empty blocks (and their surrouding blocks). Returns a List with all of the empty blocks opened."""
        block_list[index].image = empty_block
        index_list = [i for i in range(0,len(block_list)) if (block_list[i].x + 20 == block_list[index].x and block_list[i].y + 20 == block_list[index].y) or 
        (block_list[i].x == block_list[index].x and block_list[i].y + 20 == block_list[index].y) or (block_list[i].x - 20 == block_list[index].x and block_list[i].y + 20 == block_list[index].y) or 
        (block_list[i].x - 20 == block_list[index].x and block_list[i].y == block_list[index].y) or (block_list[i].x - 20 == block_list[index].x and block_list[i].y - 20 == block_list[index].y) or 
        (block_list[i].x == block_list[index].x and block_list[i].y - 20 == block_list[index].y) or (block_list[i].x + 20 == block_list[index].x and block_list[i].y - 20 == block_list[index].y) or
        (block_list[i].x + 20 == block_list[index].x and block_list[i].y == block_list[index].y)]
        for i in index_list:
            block_list = flip_block(block_list,i,1)
        return block_list

def flip_block(block_list,index,button):
    """ Flips(changes the image) of the block clicked according to the preset status. Also keeps track of the number of bombs remaining(by the flags placed). Returns an updated List of blocks. """
    if index>=len(block_list):
        return block_list
    global bomb_counter
    
    # Prevents the flipping of blocks with placed flag. 
    if button == 1 and block_list[index].image == flag_block:
        return block_list
    
    # Removing flags
    if button == 3 and block_list[index].image == flag_block:        
        bomb_counter+=1
        block_list[index].image = full_block
        return block_list
    
    # Sets flag image and keeps track of the remaining bombs 
    if button == 3 and block_list[index].image==full_block:
        bomb_counter-=1
        block_list[index].image = flag_block   
    # Sets images according to the preset status
    elif block_list[index].status == "empty" and block_list[index].image!=empty_block:
        block_list =flip_all_empty_blocks(block_list,index)
    elif block_list[index].status == "one":
        block_list[index].image = one_block
    elif block_list[index].status == "two":
        block_list[index].image = two_block
    elif block_list[index].status == "three":
        block_list[index].image = three_block
    elif block_list[index].status == "four":
        block_list[index].image = four_block
    elif block_list[index].status == "five":
        block_list[index].image = five_block
    elif block_list[index].status == "six":
        block_list[index].image = six_block
    elif block_list[index].status == "seven":
        block_list[index].image = seven_block
    elif block_list[index].status == "eight":
        block_list[index].image = eight_block
    elif block_list[index].status == "bomb":
        block_list[index].image = boom_block
    return block_list

def flip_all_bombs(block_list):
    i=0
    for block in block_list:
        if block.status == "bomb" and block.image!=boom_block:
            block_list[i].image = bomb_block
        i+=1
    return block_list 

def main():
    """ Main function """
    # Variables
    start_ticks = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    block_list = define_all_fields()
    game_over = False
    face_to_draw = happy_face
    face_to_draw_rect = happy_face_rect
    global bomb_counter 
    bomb_counter = 99

    # Start of the game cycle
    while True:           
        # Drawing a game 30x16
        screen.blit(background,(0,0))
        for elem in block_list:
            screen.blit(elem.image,(elem.x,elem.y))
        
        for event in pygame.event.get():
            # Checks for quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Checks for clicking of mouse buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                pos = find_position(mousePosition[0],mousePosition[1],block_list)
                if pos<len(block_list) and game_over == False:
                    block_list = flip_block(block_list,pos,event.button)
                    
                    # Checks if bomb is clicked and if yes, the game ends
                    if block_list[pos].status == "bomb" and event.button!=3 and block_list[pos].image!=flag_block:
                        block_list = flip_all_bombs(block_list)
                        face_to_draw = sad_face
                        face_to_draw_rect = sad_face_rect
                        game_over = True

            # Checks if the Emoji is clicked (restarts the game)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                if 300<=mousePosition[0]<=335 and 32<=mousePosition[1]<=66: 
                    start_ticks = pygame.time.get_ticks()
                    clock = pygame.time.Clock()
                    block_list = define_all_fields()
                    face_to_draw = happy_face
                    face_to_draw_rect = happy_face_rect
                    game_over = False
                    bomb_counter = 99
                    
        # Drawing the Header (bomb and time counter, Emoji(smiley/sad face))
        timer_font = pygame.font.SysFont("Marlett",40)
        bomb_count_font = pygame.font.SysFont("Marlett",40)
        bomb_count = bomb_count_font.render(str(bomb_counter),True,(255,10,10))
        bomb_count_rect = bomb_count.get_rect(center = (90,55))
        if game_over == False:
            timer = timer_font.render(str(int(((start_ticks - pygame.time.get_ticks())*-1)/1000)),True,(255,255,255))
        timer_rect = timer.get_rect(center = (600,50))
        clock_for_head_rect = clock_for_head.get_rect(center = (535,50))
        screen.blit(clock_for_head,clock_for_head_rect)
        screen.blit(timer,timer_rect)
        screen.blit(face_to_draw,face_to_draw_rect)
        screen.blit(bomb_for_head,bomb_for_head_rect)
        screen.blit(bomb_count,bomb_count_rect)
        
        # Updates the screen and sets fps
        clock.tick(60)
        pygame.display.flip()        

if __name__ == "__main__":
    main()