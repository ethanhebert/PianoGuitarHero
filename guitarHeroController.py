import pygame, sys
from pygame.constants import JOYDEVICEADDED

pygame.mixer.pre_init(44100, -16, 2, 256)
pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()

screen_width = 1200
screen_height = int(screen_width * 0.5)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Guitar Hero Controller")

joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
for joystick in joysticks:
    print(joystick.get_name())

looping = 1

while looping:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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

        #PLAYSTATION(R)3 Controller - the red guitar hero controller
        #1-player WUSBMote v2.2 - the brown classic guitar hero controller
        if event.type == pygame.JOYBUTTONDOWN:
            print(event)
        if event.type == pygame.JOYAXISMOTION:
            print(event)
        if event.type == pygame.JOYBUTTONUP:
            print(event)

    pygame.display.update()
    clock.tick(60)
