import pygame
import os
import json
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
# WIN2 = pygame.Surface((50,50))
pygame.display.set_caption("Space Invaders")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

SOUND = True
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# print(os.listdir())

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT,SPACESHIP_WIDTH)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT,SPACESHIP_WIDTH)),270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')), (WIDTH, HEIGHT))

def yellow_handle_movement(X,Y,yellow):
    if abs(X) > .4:
        if X > .7 and yellow.x + VEL + yellow.width < BORDER.x:
            yellow.x += VEL
        if X < -.7 and yellow.x - VEL > 0:
            yellow.x -= VEL
    if abs(Y) > .4:
        if Y > .7 and yellow.y + VEL + yellow.height < HEIGHT:
            yellow.y += VEL
        if Y < -.7 and yellow.y - VEL > 0:
            yellow.y -= VEL

def red_handle_movement(X,Y, red):
    if abs(X) > .4:
        if X < -.7 and red.x - VEL > BORDER.x + BORDER.width: # going left
            red.x -= VEL
        if X > .7 and red.x + VEL + SPACESHIP_WIDTH < WIDTH: # going right
            red.x += VEL
    if abs(Y) > .4:
        if Y < -.7 and red.y - VEL > 0: # going up
            red.y -= VEL
        if Y > .7 and red.y + VEL + SPACESHIP_HEIGHT < HEIGHT: # going down
            red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    # WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))

    # WIN2.fill(WHITE)

    # WIN.blit(WIN2, (WIDTH//2,100))

    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))


    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2,HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():

    pygame.joystick.init()

    #Initialize controller
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))

    for joystick in joysticks:
        joystick.init()
        # print(joystick.get_power_level())

    # print(joysticks)

    with open(os.path.join("ps4_keys.json"), 'r+') as file:
        button_keys = json.load(file)
    # 0: Left analog horizonal, 1: Left Analog Vertical, 2: Right Analog Horizontal
    # 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
    # analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }


    yellow = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        # print(int(clock.get_fps()))
        # print(joysticks[0].get_id())
        # print(joysticks[1].get_id())

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #cout "dzialaj"
                run = False
                # pygame.quit() optional
            
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == button_keys['x'] and event.instance_id == 0 and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x+yellow.height, yellow.y+yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    if SOUND:
                        BULLET_FIRE_SOUND.play()
                if event.button == button_keys['x'] and event.instance_id == 1 and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2, 10, 5)
                    red_bullets.append(bullet)
                    if SOUND:
                        BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                if SOUND:
                    BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                if SOUND:
                    BULLET_HIT_SOUND.play()
        
        # print(red_bullets, yellow_bullets)
        
        # print(f'X= {X}, Y= {Y}')
        X = joysticks[0].get_axis(0)
        Y = joysticks[0].get_axis(1)
        yellow_handle_movement(X,Y,yellow)

        X = joysticks[1].get_axis(0)
        Y = joysticks[1].get_axis(1)
        red_handle_movement(X,Y,red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)    
        
        winner_text = ""

        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
            # pass # someone won xd

    pygame.quit()
    # main() optional restart

if __name__ == "__main__":
    main()