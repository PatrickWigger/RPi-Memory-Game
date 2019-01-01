import RPi.GPIO as GPIO
import time
import numpy as np

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

RB = 16 #red button
GB = 12 #green button
WB = 25 #white button
RL = 27 #red led
GL = 17 #green led
WL = 4  #white led
EL = 26 #ez led
HL = 19 #hard led
SB = 21 #start button
DB = 20 #difficulty button

#set up inputs and outputs
GPIO.setup(RB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(WB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RL, GPIO.OUT)
GPIO.setup(GL, GPIO.OUT)
GPIO.setup(WL, GPIO.OUT)
GPIO.setup(EL, GPIO.OUT)
GPIO.setup(HL, GPIO.OUT)

#global variables
mode = 0     #easy or hard mode
gp = 0       #gameplay position
key = []     #answer key
guessno = 0  #guess number
streak = 0   #streak amount

#function resets the global variables
def reset():
    global mode
    mode = 0
    global gp
    gp = 0
    global key
    key = []
    global guessno
    guessno = 0

#turns on the green LED
def green_light():
    GPIO.output(GL, GPIO.HIGH)
    GPIO.output(RL, GPIO.LOW)
    GPIO.output(WL, GPIO.LOW)
     
#turns on the red LED     
def red_light():
    GPIO.output(GL, GPIO.LOW)
    GPIO.output(RL, GPIO.HIGH)
    GPIO.output(WL, GPIO.LOW)

#turns on the white LED
def white_light():
    GPIO.output(GL, GPIO.LOW)
    GPIO.output(RL, GPIO.LOW)
    GPIO.output(WL, GPIO.HIGH)

#turns off all LEDs
def pause_time():
    GPIO.output(GL, GPIO.LOW)
    GPIO.output(RL, GPIO.LOW)
    GPIO.output(WL, GPIO.LOW)

#enables easy mode
def easymode():
    GPIO.output(HL, GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(EL, GPIO.HIGH)
    time.sleep(0.01)
    global mode
    mode = 0
    print('Easy Mode Enabled')

#enabled hard mode
def hardmode():
    GPIO.output(EL, GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(HL, GPIO.HIGH)
    time.sleep(0.01)
    global mode
    mode = 1
    print('Hard Mode Enabled')

#prepares a new game, defaults to easy mode
def startup():
    GPIO.output(WL, GPIO.LOW)
    GPIO.output(GL, GPIO.LOW)
    GPIO.output(RL, GPIO.LOW)
    easymode()
    print('To start a new MEMORY GAME, press the BLUE button')
    print('To toggle difficulty, use BLACK button')

#win circumstance
def win():
    reset()
    print('You have WON the GAME!')
    global streak
    streak += 1
    print('Streak: {}'.format(streak))
    for i in range(10):
        white_light()
        time.sleep(0.1)
        green_light()
        time.sleep(0.1)
        red_light()
        time.sleep(0.1)
    pause_time()
    startup()

#losing circumstance
def lose():
    global streak
    streak = 0
    global mode
    if mode == 0:
        print('You have lost the game on EASY mode...really?')
    elif mode == 1:
        print('You have lost the game, maybe try EASY mode?')
    reset()
    startup() 

#checks the answer input
def checkanswer(x):
    global guessno
    global key
    print('Input Recieved')
    
    if x == key[guessno]:
        guessno += 1
        if guessno == len(key):
            win()
    else:
        lose()
    
def ezgame():
    global gp
    gp = 1
    randnums = np.random.randint(0,3,5)
    global key
    key = randnums
    
    i = 0
    while i < len(randnums):
        if randnums[i] == 0:
            red_light()
        elif randnums[i] == 1:
            green_light()
        elif randnums[i] == 2:
            white_light()
        
        time.sleep(1)
        pause_time()
        time.sleep(0.5)
        i += 1
    gp = 2

def hardgame():
    global gp
    gp = 1
    randnums = np.random.randint(0,3,8)
    global key
    key = randnums
    
    i = 0
    while i < len(randnums):
        if randnums[i] == 0:
            red_light()
        elif randnums[i] == 1:
            green_light()
        elif randnums[i] == 2:
            white_light()
        
        time.sleep(1)
        pause_time()
        time.sleep(0.3)
        i += 1
    gp = 2


startup()
while True:
    st = GPIO.input(SB)
    dif_in = GPIO.input(DB)
    wb_in = GPIO.input(WB)
    gb_in = GPIO.input(GB)
    rb_in = GPIO.input(RB)
    
    if dif_in == False:
        #checks whether or not the game has started
        if gp == 0:
            if mode == 0:
                hardmode()
            elif mode == 1:
                easymode()
        else:
            print('Difficulty cannot be changed during the game!')
        time.sleep(0.5)    

    if st == False:
        print('Game Beginning in 3 seconds!')
        time.sleep(3)
        if mode == 0:
            ezgame()
        elif mode == 1:
            hardgame()
        time.sleep(.03)
        print('Input your answer now!')
        
    if wb_in == False:
        if gp == 2:
            checkanswer(2)
        else:
            print('Cannot enter answer at this time')
        time.sleep(0.2)
        
    if gb_in == False:
        if gp == 2:
            checkanswer(1)
        else:
            print('Cannot enter answer at this time')
        time.sleep(0.2)
        
    if rb_in == False:
        if gp == 2:
            checkanswer(0)
        else:
            print('Cannot enter answer at this time')
        time.sleep(0.2)
        
        
        
    
