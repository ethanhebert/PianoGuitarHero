import pygame, sys
from pygame.constants import JOYDEVICEADDED


pygame.mixer.pre_init(44100, -16, 2, 256)
pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()

screen_width = 1200
screen_height = int(screen_width * 0.5)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Controller Input")

joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
for joystick in joysticks:
    print(joystick.get_name())
try:
    controller1 = joysticks[0].get_name()
except:
    controller1 = "computer"
print("controller1:", controller1)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)

player = pygame.Rect(200, 200, 50, 50)
player_color = black
player_motion = [0,0]

player2 = pygame.Rect(600, 400, 50, 50)
player2_color = black
player2_motion = [0,0]

dpad = 0
shift = 0
color_order = ["placeholder"]
looping = 1



while looping == 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #if a joystick is added or removed during the game
        if event.type == pygame.JOYDEVICEADDED:
            print("Device added")
            joysticks = []
            for i in range(pygame.joystick.get_count()):
                joysticks.append(pygame.joystick.Joystick(i))
            for joystick in joysticks:
                print(joystick.get_name())
            try:
                controller1 = joysticks[0].get_name()
            except:
                controller1 = "computer"
            print("controller1:", controller1)
        if event.type == pygame.JOYDEVICEREMOVED:
            print("Device removed")
            joysticks = []
            for i in range(pygame.joystick.get_count()):
                joysticks.append(pygame.joystick.Joystick(i))
            for joystick in joysticks:
                print(joystick.get_name())
            try:
                controller1 = joysticks[0].get_name()
            except:
                controller1 = "computer"
            print("controller1:", controller1)

        #controls for PDP Xbox 360 Afterglow
        if controller1 == "PDP Xbox 360 Afterglow":
            if event.type == pygame.JOYBUTTONDOWN: #the buttons, a=0, b=1, x=2, y=3
                if event.button == 0:
                    color_order.append(0)
                if event.button == 1:
                    color_order.append(1)
                if event.button == 2:
                    color_order.append(2)
                if event.button == 3:
                    color_order.append(3)
            if event.type == pygame.JOYBUTTONUP: #the buttons, a=0, b=1, x=2, y=3
                for i in range(len(color_order)):
                    if color_order[i] == event.button:
                        del color_order[i]
                        break
            if event.type == pygame.JOYHATMOTION: #the d pad, returns tuple like (1,0) or (0,-1)
                player_motion[0] = event.value[0]
                player_motion[1] = -event.value[1]
                player2_motion[0] = event.value[0]
                player2_motion[1] = -event.value[1]
                dpad = 1
                if event.value == (0,0):
                    dpad = 0

            if event.type == pygame.JOYAXISMOTION and dpad == 0: #joysticks, left horiz = 0, left vert = 1, right horiz = 2, right vert = 3
                if event.axis < 2: #left joystick
                    player_motion[event.axis] = event.value
                if 1 < event.axis < 4: #right joystick
                    player2_motion[event.axis - 2] = event.value

                #if the sticks aren't pressed, don't register tiny little movements
                if abs(player_motion[0]) < 0.1:
                    player_motion[0] = 0
                if abs(player_motion[1]) < 0.1:
                    player_motion[1] = 0
                if abs(player2_motion[0]) < 0.1:
                    player2_motion[0] = 0
                if abs(player2_motion[1]) < 0.1:
                    player2_motion[1] = 0

        #controls for computer
        elif controller1 == "computer":
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    color_order.append(0)
                if event.key == pygame.K_2:
                    color_order.append(1)
                if event.key == pygame.K_3:
                    color_order.append(2)
                if event.key == pygame.K_4:
                    color_order.append(3)

                #shift moves both players with the arrows
                if event.key == pygame.K_LSHIFT:
                    shift += 1
                
                if shift > 0:
                    if event.key == pygame.K_UP:
                        player_motion[1] = -1
                        player2_motion[1] = -1
                    if event.key == pygame.K_DOWN:
                        player_motion[1] = 1
                        player2_motion[1] = 1
                    if event.key == pygame.K_LEFT:
                        player_motion[0] = -1
                        player2_motion[0] = -1
                    if event.key == pygame.K_RIGHT:
                        player_motion[0] = 1
                        player2_motion[0] = 1
                else:
                    if event.key == pygame.K_UP:
                        player2_motion[1] = -1
                    if event.key == pygame.K_DOWN:
                        player2_motion[1] = 1
                    if event.key == pygame.K_LEFT:
                        player2_motion[0] = -1
                    if event.key == pygame.K_RIGHT:
                        player2_motion[0] = 1

                    if event.key == pygame.K_w:
                        player_motion[1] = -1
                    if event.key == pygame.K_s:
                        player_motion[1] = 1
                    if event.key == pygame.K_a:
                        player_motion[0] = -1
                    if event.key == pygame.K_d:
                        player_motion[0] = 1

                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    for i in range(len(color_order)):
                        if color_order[i] == 0:
                            del color_order[i]
                            break
                if event.key == pygame.K_2:
                    for i in range(len(color_order)):
                        if color_order[i] == 1:
                            del color_order[i]
                            break
                if event.key == pygame.K_3:
                    for i in range(len(color_order)):
                        if color_order[i] == 2:
                            del color_order[i]
                            break
                if event.key == pygame.K_4:
                    for i in range(len(color_order)):
                        if color_order[i] == 3:
                            del color_order[i]
                            break

                if event.key == pygame.K_LSHIFT:
                    shift -= 1
                    
                if shift > 0:
                    if event.key == pygame.K_UP:
                        player_motion[1] = 0
                        player2_motion[1] = 0
                    if event.key == pygame.K_DOWN:
                        player_motion[1] = 0
                        player2_motion[1] = 0
                    if event.key == pygame.K_LEFT:
                        player_motion[0] = 0
                        player2_motion[0] = 0
                    if event.key == pygame.K_RIGHT:
                        player_motion[0] = 0
                        player2_motion[0] = 0
                else:
                    if event.key == pygame.K_UP:
                        player2_motion[1] = 0
                    if event.key == pygame.K_DOWN:
                        player2_motion[1] = 0
                    if event.key == pygame.K_LEFT:
                        player2_motion[0] = 0
                    if event.key == pygame.K_RIGHT:
                        player2_motion[0] = 0

                    if event.key == pygame.K_w:
                        player_motion[1] = 0
                    if event.key == pygame.K_s:
                        player_motion[1] = 0
                    if event.key == pygame.K_a:
                        player_motion[0] = 0
                    if event.key == pygame.K_d:
                        player_motion[0] = 0

                
                    
    screen.fill(white)

    #this allows the player to hit multiple color buttons and it always displays the most recect one (the last item in the color_order list)
    if color_order[len(color_order) - 1] == 0:
        current_color = green
    elif color_order[len(color_order) - 1] == 1:
        current_color = red
    elif color_order[len(color_order) - 1] == 2:
        current_color = blue
    elif color_order[len(color_order) - 1] == 3:
        current_color = yellow
    else:
        current_color = black
    player_color = current_color
    player2_color = current_color

    player.x += player_motion[0] * 10
    player.y += player_motion[1] * 10
    pygame.draw.rect(screen, player_color, player)

    player2.x += player2_motion[0] * 10
    player2.y += player2_motion[1] * 10
    pygame.draw.rect(screen, player2_color, player2)

    pygame.display.update()
    clock.tick(60)