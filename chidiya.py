import pygame
import random
from pygame.locals import *
import sys

"SOME GLOBAL VARIABLE"
FPS = 40
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
"ITS USE TO INTIALIZE THE WINDOW OR SCREEN OF RESPECTIVE HEIGHT"
GROUND = SCREEN_HEIGHT * 0.80
GAME_IMAGES = {}
GAME_SOUNDS = {}
PLAYER = "picutures/flappy.png"
BACKGROUND = "picutures/first.jpg"
PIPE = "picutures/pipe2.0.png"

# -----------------------------------------------------------------------THIS IS THE WELCOME SCCREEN OF THE GAME---------------------------------------------------------
def welcomescreen():
    Playerx = int(SCREEN_WIDTH/4)
    Playery = 250
    messagex = int((SCREEN_WIDTH - GAME_IMAGES["message"].get_width())/2)
    messagey = int((SCREEN_HEIGHT - GAME_IMAGES["message"].get_height())/2)
    Playery = int((SCREEN_HEIGHT * 0.15))
    basex = 0
    
    while True:
        for event in pygame.event.get():
            """ 8THIS pygame.event.get() WILL TELL USE THAT WHICH KEY IS BEING TOUCH FROM THE
                USER"""
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                """THIS EVENT MEANS IF event.type == QUIT MEANS IF YOU CLICK CROSS ON WINDOW
                    AND event.type == KEYDOWN (MEANS KI BUTTON DABANE PAR) AND event.key == K_ESCAPE 
                    (DABAYA GYA BUTTON ESCAPE HAI) MEANS IF YOU PRESS ESCAPE
                    KEY THEN THE GAME WILL BE CLOSED"""
                pygame.quit()
                sys.exit()
                
            elif event.type == KEYDOWN and ( event.key == K_SPACE or event.key == K_UP):
                return
            
            else:
                SCREEN.blit(GAME_IMAGES["background"],(0,0))
                SCREEN.blit(GAME_IMAGES["player"],(Playerx,Playery))
                SCREEN.blit(GAME_IMAGES["message"],(messagex,messagey))
                SCREEN.blit(GAME_IMAGES["base"],(basex,GROUND))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                
#------------------------------------------------------------------------------THIS IS THE GAME OVER FUCNTION -----------------------------------------------------------

def iscollide(playerx,playery,upper_pipes,lower_pipes):
    
    if playery>GROUND - 80 or playery < 0:
        GAME_SOUNDS['die'].play()
        return True
    
    for pipe in upper_pipes:
        if (playery < 500 + pipe['y'] and abs(playerx -pipe['x']) < 60):
            GAME_SOUNDS['die'].play()
            return True
        
    for pipe in lower_pipes:
        if ((playery + GAME_IMAGES['player'].get_height()) > pipe['y'] and abs(playerx- pipe['x']) < 60):
            GAME_SOUNDS['die'].play()
            return True
        
    return False

# ---------------------------------------------------------------------THIS IS THE MAIN GAME FUNCTION--------------------------------------------------------------------

def maingame():
    score = 0
    playerx = int(SCREEN_WIDTH/4) 
    playery = 250
    basex = 0
    
    "LOGIC BEHIND RANDOM PIPE"
    pipe1 = get_random_pipe()
    pipe2 = get_random_pipe()
    
    """ AS YOU CAN SEE THAT THE BOTH pipe1 AND pipe2 RETURN THE LIST IN WHICH FIRST DICTONARY IS 
        IS FOR THE UPPER PIPE AND SECOND DICTONARY IS FOR THE LOWER PIPE """
    upper_pipes = [
        {'x': SCREEN_HEIGHT + 200, 'y': pipe1[0]['y'], 'scored': False},
        {'x': SCREEN_HEIGHT + 200 + (SCREEN_WIDTH / 2), 'y': pipe2[0]['y'], 'scored': False}
    ]

    lower_pipes = [
        {'x': SCREEN_HEIGHT + 200, 'y': pipe2[1]['y'], 'scored': False},
        {'x': SCREEN_HEIGHT + 200 + (SCREEN_WIDTH / 2), 'y': pipe2[1]['y'], 'scored': False}
    ]
    # pipe_velocityX = -5
    player_velocityY = -9
    playerMax_velocity = 10
    playerMin_velocity = -8
    playerAccY = 1
    PlayerFlap_velocity = -8
    playerFlap = False 
    
    " THIS IS THE MAIN WHILE LOOP FOR THE GAME"
    while True:
        # GAME_SOUNDS['main'].play()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN or (event.key == K_BACKSPACE  or event.key == K_UP):
                if playery > 0:
                    player_velocityY = PlayerFlap_velocity
                    playerFlap = True
                    GAME_SOUNDS['jump'].play()
                    
        crash_Test = iscollide(playerx,playery,upper_pipes,lower_pipes)
        if crash_Test :   #IF crash_Test RETURN TRUE IF THE PLAYER IS CRASHED
            return        
                
        if player_velocityY < playerMax_velocity and not playerFlap:
            player_velocityY += playerAccY
            
        if playerFlap:
            playerFlap = False
        
        player_H =  GAME_IMAGES['player'].get_height()
        playery = playery + min(player_velocityY,GROUND - playery -player_H)
        
        
        "TO INCREASE THE SPEED WE ALSO HAVE TO CHNAGE THE DISTANCE OF THE UPCOMMING PIPE"
        if score <= 10:
            pipe_velocityX = -6
            distance = 8

        elif 11 <= score <= 20:
            pipe_velocityX = -8
            distance = 10

        elif 21 <= score <= 30:
            pipe_velocityX = -10
            distance = 12

        else:
            pipe_velocityX = -12
            distance = 15

        "FOR MOVING PIPES TO LEFT"
        for upperpipe,lowerpipe in zip(upper_pipes,lower_pipes):
            upperpipe['x'] += pipe_velocityX
            lowerpipe['x'] += pipe_velocityX

    
        "ADDING NEW PIPES"
        if 0 < upper_pipes[0]['x'] < distance:
            new_pipes = get_random_pipe()
            upper_pipes.append(new_pipes[0])
            lower_pipes.append(new_pipes[1])
        
        "NOW REMOVING THE PIPE FORM THE SCREEN"
        if upper_pipes[0]['x'] < -GAME_IMAGES['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)
        
        
        SCREEN.blit(GAME_IMAGES['background'],(0,0))
        x = GAME_IMAGES['pipe'][0]
        y = GAME_IMAGES['pipe'][1]
        small_pipe1 = pygame.transform.scale(x,(100,500))
        small_pipe2 = pygame.transform.scale(y,(100,500))
        """TIP WHEN YOU ARE PUTTING THE IMAGE INSIDE THE LIST THEN YOU SHOULD GIVE SIZE TO YOU IMAGE IF YOU DO SO THNE YOU DO NOT HAVE TO RESIZE IT AGAIN 
            AND REMEMBER THE get_height and get_width RETURN OF THE ACUTAL IMAGE
        """
        for upperpipe,lowerpipe in zip(upper_pipes,lower_pipes):
            SCREEN.blit(small_pipe1,(upperpipe['x'],upperpipe['y']))
            SCREEN.blit(small_pipe2,(lowerpipe['x'],lowerpipe['y']))
            
        SCREEN.blit(GAME_IMAGES['base'],(basex,GROUND))
        SCREEN.blit(GAME_IMAGES['player'],(playerx,playery))

#--------------------------------------------------------------------------FOR PRINTING THE SCORE-------------------------------------------------------------------------

        playerMidPos = playerx + GAME_IMAGES['player'].get_width()/2
        
        "THIS IS THE CENTER OF THE BIRD AS YOU CAN SEE WE ADD HALF WIDTH IN THE POSITION"         
        for pipe in lower_pipes:
            pipeMidPos = pipe['x'] + GAME_IMAGES['pipe'][1].get_width()/2
            #FOR THE POINTS 
            if pipeMidPos <= playerMidPos < pipeMidPos + 100 and not pipe['scored']:
                """IMPORTANT CONCEPT
                AS YOU CAN THAT OUR GAME FPS IS 38 SO MEANS OUR LOOP RUN 38 TIMES AND CHECK ALL THE CONDITIONS MEANS THE SCORING CONDTION ALSO BE CHECKED 38 TIMES
                SO WE HAVE TO MAKE SURE THAT THE SCORE IS NOT INCREMENTED 38 TIMES SO WE MAKE A FLAG THAT IS WE ADD THE THIRD ELEMENT IN THE get_random_pipe WITH 
                THE KEY scored WHICH IS INITIALLY FALSE NOW WHEN THE FIRST TIME THE CONDITION IS CHECKED THEN IT BECOME TRUE NOW ID THE CONDTION IS CHEKED AGAIN THE
                SCORE IS NOT INCREMENTED
                """
                score +=1
                pipe['scored'] = True
                print(f"score is {score}")
                GAME_SOUNDS['point'].play()
        #THIS WILL CONVERT DOUBLE OR TRIPLE NUMBER INTO THE LIST LIKE 34 IN TO [3,4]
        mydigits = [int(x) for x in list(str(score))]   
        width = 0 
        for digits in mydigits:
            
            width += GAME_IMAGES['number'][digits].get_width()
        middle = (SCREEN_WIDTH - width)/2
        
        for digits in mydigits:
            SCREEN.blit(GAME_IMAGES['number'][digits],(middle,20))
            middle += GAME_IMAGES['number'][digits].get_width()
            
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        """THIS MEANS THAT OUR WHILE LOOP RUNS 38 TIMES PER SECOND/FRAME"""
    
#------------------------------------------------------------------------THIS WILL GENERATE THE RANDOM PIPE---------------------------------------------------------------

def get_random_pipe():
    pipe_height = 500
    middle_space = SCREEN_HEIGHT / 4
    y2_lowerPipe = middle_space + random.randrange(0, int(SCREEN_HEIGHT - GAME_IMAGES['base'].get_height() - 1.2 * middle_space) + random.randrange(0, 100)) + 100
    pipeX = SCREEN_WIDTH + 10
    y1_upperPipe = pipe_height - y2_lowerPipe + middle_space
    
    pipe = [
        {'x': pipeX, 'y': -y1_upperPipe, 'scored': False},  # Added 'scored' key
        {'x': pipeX, 'y': y2_lowerPipe, 'scored': False}   # Added 'scored' key
    ]
    return pipe

def main():
    
    pygame.init()                                    #THIS INTIALIZE THE pygame ALL MODULES
    pygame.display.set_caption("FLAPPY BIRD")
# -------------------------------------------------------------------FILLING IMAGES IN THOSE EMPTY DICTONARIES------------------------------------------------------------

    GAME_IMAGES['number'] = (
        pygame.transform.scale(pygame.image.load("picutures/0.png"),(60,80)).convert_alpha(),
        pygame.transform.scale(pygame.image.load("picutures/1.png"),(60,80)).convert_alpha(),
        pygame.transform.scale(pygame.image.load("picutures/2.png"),(60,80)).convert_alpha(),
        pygame.transform.scale(pygame.image.load("picutures/3.png"),(60,80)).convert_alpha(),
        pygame.transform.scale(pygame.image.load("picutures/4.png"),(60,80)).convert_alpha(),
        pygame.transform.scale(pygame.image.load("picutures/5.png"),(60,80)).convert_alpha(),
        pygame.transform.scale(pygame.image.load("picutures/6.png"),(60,80)).convert_alpha(),
        pygame.transform.scale(pygame.image.load("picutures/7.png"),(60,80)).convert_alpha(),
        pygame.transform.scale(pygame.image.load("picutures/8.png"),(60,80)).convert_alpha(),
        pygame.transform.scale(pygame.image.load("picutures/9.png"),(60,80)).convert_alpha(),
    )
    
    GAME_IMAGES['base'] = (
        pygame.image.load("picutures/base2.0.png").convert_alpha()
    )
    
    GAME_IMAGES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )
    
# ---------------------------------------------------------------RESSIZING THE SCREEN FOR THE ACTAUL GAME SCREEN----------------------------------------------------------

    new_bg = pygame.image.load(BACKGROUND).convert_alpha()
    new_bg = pygame.transform.scale(new_bg,(SCREEN_WIDTH,SCREEN_HEIGHT - 150))
    GAME_IMAGES['background'] = new_bg
    
    new_player = pygame.image.load(PLAYER).convert_alpha()
    new_player = pygame.transform.scale(new_player,(60,70))
    GAME_IMAGES['player'] = new_player
    
    new_msg = pygame.image.load("picutures/pngwing.com.png").convert_alpha()
    new_msg = pygame.transform.scale(new_msg,(400,300))
    GAME_IMAGES['message'] = new_msg
    
#-------------------------------------------------------------------------------SOUND EFFECT----------------------------------------------------------------------------

    GAME_SOUNDS['die'] = pygame.mixer.Sound("audio/die.mp3")
    GAME_SOUNDS['always'] = pygame.mixer.Sound("audio/main.mp3")
    GAME_SOUNDS['jump'] = pygame.mixer.Sound("audio/jump.mp3")
    GAME_SOUNDS['point'] = pygame.mixer.Sound("audio/coin.mp3")
    GAME_SOUNDS['main'] = pygame.mixer.Sound("audio/main.mp3")
    
    
# -----------------------------------------------------------------------------ACTAUL TWO MAIN GAMEFUNTION--------------------------------------------------------------
# FIRST IS THE WELCOME SCREEN MEANS WHEN THE GAME IS NOT START THE HOW THE SCREEN LOOKS AND MAINGAME IS THE AFTER THE GAME START
    while True:
        welcomescreen()
        maingame()
FPSCLOCK = pygame.time.Clock()                   # THIS IS FOR THE CONTROLLING THE FPS

if __name__ == "__main__":
    main()