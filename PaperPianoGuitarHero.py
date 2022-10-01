#######################################################################
# Name: Ethan Hebert
# Date: 5-19-21
# Description: This code creates a little synthesizer where a user can
# select and play four different types of sound waves using their
# keyboard as the keys on a piano.
#######################################################################

#hardware -- transistor w/ GPIO
#source -> gate -> drain
#emitter -> base -> collector
#from -> through -> to


#software -- build a note

import pygame
from time import sleep
from array import array
import math

#initialize pygame mixer constants
MIXER_FREQ = 44100
MIXER_SIZE = -16
MIXER_CHANS = 1
MIXER_BUFF = 1024


#build a note class
class Note(pygame.mixer.Sound):
    def __init__(self, frequency, volume, form):
        self.frequency = frequency
        self.waveform = form
        pygame.mixer.Sound.__init__(self, buffer=self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        #really long wavelength - many samples
        #super short wavelength - few samples
        period = int(round(MIXER_FREQ/self.frequency))
        amplitude = 2**(abs(MIXER_SIZE)-1)-1

        #generate an array for this note's samples
        samples = array("h", [0]*period)

        #sin wave
        if(self.waveform == "sin"):
            for t in range(period):
                piConversion = (t/period)*(2*math.pi)
                samples[t] = int(amplitude*(math.sin(piConversion)))

        #square wave
        elif(self.waveform == "square"):
            for t in range(period):
                if(t < period/2):
                    samples[t] = amplitude
                else:
                    samples[t] = -amplitude

        #sawtooth wave
        elif(self.waveform == "sawtooth"):
            for t in range(period):
                if(t < period/2):
                    samples[t] = int(2*amplitude*(t/period))
                else:
                    samples[t] = int(2*amplitude*(t/period - 1))

        #triangle wave
        elif(self.waveform == "triangle"):
            for t in range(period):
                if(t < period/4):
                    samples[t] = int(4*amplitude*(t/period))
                elif(t < 3*period/4):
                    samples[t] = int(-4*amplitude*(t/period) + 2*amplitude) 
                else:
                    samples[t] = int(4*amplitude*(t/period - 1))
                    
        return samples

###############
###MAIN CODE###
###############
    
#initialize pygame
pygame.mixer.pre_init(MIXER_FREQ, MIXER_SIZE, MIXER_CHANS, MIXER_BUFF)

#some colors for the GUI
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 139, 110)
yellow = (255, 221, 110)
blue = (110, 180, 255)
green = (110, 255, 153)
purple = (161, 110, 255)

#status of each square being pressed
yellowPress = 0
purplePress = 0
bluePress = 0
redPress = 0

#you need a display to play sound
screen = pygame.display.set_mode((430,430))
screen.fill(black)
pygame.display.set_caption("PySynth 4X: The New Wave of Audio Synthesizers")
pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()

#some guitar hero controller stuff
joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
for joystick in joysticks:
    print(joystick.get_name())
controller1 = "computer"
strum = 0
note_list = [0, 0, 0, 0, 0] #tracks which notes you just strummed
timer = 10
note0 = 0 #tracks if each note is already playing or not
note1 = 0
note2 = 0
note3 = 0
note4 = 0

width = screen.get_width()
height = screen.get_height()
font = pygame.font.SysFont('Century Gothic', 40, bold=True)
createNotes = 0
notesCreated = 0
exitLoop = 0

#loop to check for input, change display, and play sounds
while (exitLoop == 0):

    #tracks the mouse movement in (x,y)
    mouse = pygame.mouse.get_pos()


    #display the squares and text based on if they've been selected or not and change the current sound
    #rectangle is (left, top, width, height)

    #yellow
    if (yellowPress == 1):
        pygame.draw.rect(screen, yellow, pygame.Rect(10, 10, 200, 200))
        pygame.draw.rect(screen, white, pygame.Rect(10, 10, 200, 200), 5)
        sinText = font.render('Sin', True, white)
    else:
        pygame.draw.rect(screen, black, pygame.Rect(10, 10, 200, 200))
        pygame.draw.rect(screen, black, pygame.Rect(10, 10, 200, 200), 5)
        pygame.draw.rect(screen, yellow, pygame.Rect(10, 10, 200, 200), 5)
        sinText = font.render('Sin', True, yellow)

    #purple
    if (purplePress == 1):
        pygame.draw.rect(screen, purple, pygame.Rect(220, 10, 200, 200))
        pygame.draw.rect(screen, white, pygame.Rect(220, 10, 200, 200), 5)
        squareText = font.render('Square', True, white)
    else:
        pygame.draw.rect(screen, black, pygame.Rect(220, 10, 200, 200))
        pygame.draw.rect(screen, black, pygame.Rect(220, 10, 200, 200), 5)
        pygame.draw.rect(screen, purple, pygame.Rect(220, 10, 200, 200), 5)
        squareText = font.render('Square', True, purple)

    #blue
    if (bluePress == 1):
        pygame.draw.rect(screen, blue, pygame.Rect(10, 220, 200, 200))
        pygame.draw.rect(screen, white, pygame.Rect(10, 220, 200, 200), 5)
        sawtoothText = font.render('Sawtooth', True, white)
    else:
        pygame.draw.rect(screen, black, pygame.Rect(10, 220, 200, 200))
        pygame.draw.rect(screen, black, pygame.Rect(10, 220, 200, 200), 5)
        pygame.draw.rect(screen, blue, pygame.Rect(10, 220, 200, 200), 5)
        sawtoothText = font.render('Sawtooth', True, blue)

    #red
    if (redPress == 1):
        pygame.draw.rect(screen, red, pygame.Rect(220, 220, 200, 200))
        pygame.draw.rect(screen, white, pygame.Rect(220, 220, 200, 200), 5)
        triangleText = font.render('Triangle', True, white)
    else:
        pygame.draw.rect(screen, black, pygame.Rect(220, 220, 200, 200))
        pygame.draw.rect(screen, black, pygame.Rect(220, 220, 200, 200), 5)
        pygame.draw.rect(screen, red, pygame.Rect(220, 220, 200, 200), 5)
        triangleText = font.render('Triangle', True, red)



    #if hovering over a square
    #yellow
    if ((8 <= mouse[0] <= width/2-3) and (8 <= mouse[1] <= height/2-3)):
        pygame.draw.rect(screen, white, pygame.Rect(10, 10, 200, 200), 5)
        sinText = font.render('Sin', True, white)

    #purple
    if ((width/2+3 <= mouse[0] <= width-8) and (8 <= mouse[1] <= height/2-3)):
        pygame.draw.rect(screen, white, pygame.Rect(220, 10, 200, 200), 5)
        squareText = font.render('Square', True, white)
        
    #blue
    if ((8 <= mouse[0] <= width/2-3) and (height/2+3 <= mouse[1] <= height-8)):
        pygame.draw.rect(screen, white, pygame.Rect(10, 220, 200, 200), 5)
        sawtoothText = font.render('Sawtooth', True, white)
        
    #red
    if ((width/2+3 <= mouse[0] <= width-8) and (height/2+3 <= mouse[1] <= height-8)):
        pygame.draw.rect(screen, white, pygame.Rect(220, 220, 200, 200), 5)
        triangleText = font.render('Triangle', True, white)



    #put the text onto a surface to make it visible        
    screen.blit(sinText,(width/4-25, height/4-25))
    screen.blit(squareText,(3*width/4-67, height/4-25))
    screen.blit(sawtoothText,(width/4-85, 3*height/4-30))
    screen.blit(triangleText,(3*width/4-75, 3*height/4-30))

    #update the display with changes
    pygame.display.update()
    clock.tick(60)

    
    for event in pygame.event.get():

        #closing the display
        if event.type == pygame.QUIT:
            exitLoop = 1

        #adding guitar hero controller
        if event.type == pygame.JOYDEVICEADDED:
            print("Device added")
            joysticks = []
            for i in range(pygame.joystick.get_count()):
                joysticks.append(pygame.joystick.Joystick(i))
            for joystick in joysticks:
                print(joystick.get_name())
        if event.type == pygame.JOYDEVICEREMOVED:
            print("Device removed")
            joysticks = []
            for i in range(pygame.joystick.get_count()):
                joysticks.append(pygame.joystick.Joystick(i))
            for joystick in joysticks:
                print(joystick.get_name())

        #check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            #see which square was selected
            #yellow
            if ((8 <= mouse[0] <= width/2-3) and (8 <= mouse[1] <= height/2-3)):
                yellowPress = 1
                purplePress = 0
                bluePress = 0
                redPress = 0
                
                form = "sin"
                createNotes = 1

            #purple
            if ((width/2+3 <= mouse[0] <= width-8) and (8 <= mouse[1] <= height/2-3)):
                yellowPress = 0
                purplePress = 1
                bluePress = 0
                redPress = 0
                
                form = "square"
                createNotes = 1
                 
            #blue
            if ((8 <= mouse[0] <= width/2-3) and (height/2+3 <= mouse[1] <= height-8)):
                yellowPress = 0
                purplePress = 0
                bluePress = 1
                redPress = 0
                
                form = "sawtooth"
                createNotes = 1
                  
            #red
            if ((width/2+3 <= mouse[0] <= width-8) and (height/2+3 <= mouse[1] <= height-8)):
                yellowPress = 0
                purplePress = 0
                bluePress = 0
                redPress = 1
                
                form = "triangle"
                createNotes = 1


            #create a bunch of piano notes for the current form
            if (createNotes == 1):
                E3 = Note(164.81, 1, form) #A
                F3 = Note(174.61, 1, form) #S
                F3s = Note(185.00, 1, form) #E
                G3 = Note(196.00, 1, form) #D
                G3s = Note(207.65, 1, form) #R
                A3 = Note(220.00, 1, form) #F
                A3s = Note(233.08, 1, form) #T
                B3 = Note(246.94, 1, form) #G

                C4 = Note(261.63, 1, form) #middle C - H

                C4s = Note(277.18, 1, form) #U
                D4 = Note(293.66, 1, form) #J
                D4s = Note(311.13, 1, form) #I
                E4 = Note(329.63, 1, form) #K
                F4 = Note(349.23, 1, form) #L
                F4s = Note(369.99, 1, form) #P
                G4 = Note(392.00, 1, form) #;
                G4s = Note(415.30, 1, form) #[
                A4 = Note(440.00, 1, form) #'
                A4s = Note(466.16, 1, form) #]

                pygame.mixer.stop()
                createNotes = 0
                notesCreated = 1


        #check for key presses
        if event.type == pygame.KEYDOWN and notesCreated == 1:
            if event.key == pygame.K_a:
                E3.play(-1)
            if event.key == pygame.K_s:
                F3.play(-1)
            if event.key == pygame.K_e:
                F3s.play(-1)
            if event.key == pygame.K_d:
                G3.play(-1)
            if event.key == pygame.K_r:
                G3s.play(-1)
            if event.key == pygame.K_f:
                A3.play(-1)  
            if event.key == pygame.K_t:
                A3s.play(-1)    
            if event.key == pygame.K_g:
                B3.play(-1)
            
            if event.key == pygame.K_h: #middle C
                C4.play(-1)

            if event.key == pygame.K_u:
                C4s.play(-1)   
            if event.key == pygame.K_j:
                D4.play(-1)
            if event.key == pygame.K_i:
                D4s.play(-1)
            if event.key == pygame.K_k:
                E4.play(-1)
            if event.key == pygame.K_l:
                F4.play(-1)
            if event.key == pygame.K_p:
                F4s.play(-1)
            if event.key == pygame.K_SEMICOLON:
                G4.play(-1)
            if event.key == pygame.K_LEFTBRACKET:
                G4s.play(-1)
            if event.key == pygame.K_QUOTE:
                A4.play(-1)
            if event.key == pygame.K_RIGHTBRACKET:
                A4s.play(-1)



        if event.type == pygame.KEYUP and notesCreated == 1:
            if event.key == pygame.K_a:
                E3.stop()
            if event.key == pygame.K_s:
                F3.stop()
            if event.key == pygame.K_e:
                F3s.stop()
            if event.key == pygame.K_d:
                G3.stop()
            if event.key == pygame.K_r:
                G3s.stop()
            if event.key == pygame.K_f:
                A3.stop()       
            if event.key == pygame.K_t:
                A3s.stop()    
            if event.key == pygame.K_g:
                B3.stop()
     
            if event.key == pygame.K_h: #middle C
                C4.stop()

            if event.key == pygame.K_u:
                C4s.stop()    
            if event.key == pygame.K_j:
                D4.stop()
            if event.key == pygame.K_i:
                D4s.stop()
            if event.key == pygame.K_k:
                E4.stop()
            if event.key == pygame.K_l:
                F4.stop()
            if event.key == pygame.K_p:
                F4s.stop()
            if event.key == pygame.K_SEMICOLON:
                G4.stop()
            if event.key == pygame.K_LEFTBRACKET:
                G4s.stop()
            if event.key == pygame.K_QUOTE:
                A4.stop()
            if event.key == pygame.K_RIGHTBRACKET:
                A4s.stop()

        #guitar hero controller input - the brown guitar
        for joystick in joysticks:
            if joystick.get_name() == "1-player WUSBMote v2.2":
                controller1 = "1-player WUSBMote v2.2"
        
        if controller1 == "1-player WUSBMote v2.2":
            if event.type == pygame.JOYBUTTONDOWN and notesCreated == 1:
                if event.button == 5:
                    strum = 1
                    timer = 0
                if event.button == 8:
                    strum = 1
                    timer = 0
                if event.button == 0:
                    note_list[0] = 1
                if event.button == 1:
                    note_list[1] = 1
                if event.button == 2:
                    note_list[2] = 1
                if event.button == 3:
                    note_list[3] = 1         
                if event.button == 4:
                    note_list[4] = 1

            if event.type == pygame.JOYBUTTONUP and notesCreated == 1:
                if event.button == 0:
                    note_list[0] = 0
                    note0 = 0
                    G4.stop()          #NOTES FOR COME AS YOU ARE - NIRVANA
                if event.button == 1:
                    note_list[1] = 0
                    note1 = 0
                    D4.stop()
                if event.button == 2:
                    note_list[2] = 0
                    note2 = 0
                    D4s.stop()
                if event.button == 3:
                    note_list[3] = 0
                    note3 = 0
                    E4.stop()       
                if event.button == 4:
                    note_list[4] = 0
                    note4 = 0
                    A4.stop()
                    
            #timer allows the player to hit the color note barely late and it still registers
            if timer < 8:
                if strum > 0:
                    if note_list[0] == 1:
                        if note0 == 1:
                            G4.stop()
                        G4.play(-1)
                        note0 = 1
                    if note_list[1] == 1:
                        if note1 == 1:
                            D4.stop()
                        D4.play(-1)
                        note1 = 1
                    if note_list[2] == 1:
                        if note2 == 1:
                            D4s.stop()
                        D4s.play(-1)
                        note2 = 1
                    if note_list[3] == 1:
                        if note3 == 1:
                            E4.stop()
                        E4.play(-1) 
                        note3 = 1
                    if note_list[4] == 1:
                        if note4 == 1:
                            A4.stop()
                        A4.play(-1)
                        note4 = 1

            elif timer >= 8:
                strum = 0

    timer += 1
    if timer > 1000:
        timer = 8


#once you exit the loop, quit the program
pygame.quit()

    



    
