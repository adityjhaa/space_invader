import pygame
import random
import math
from pygame import mixer

pygame.init()

mixer.music.load('background.mp3')
mixer.music.play(-1)

#set the screen size
screen = pygame.display.set_mode((1200,1000))

#background image
background = pygame.image.load('background.png')

#title
pygame.display.set_caption("Space Invaders")

#the spaceship
playerimg = pygame.image.load('spaceship.png')
playerx = 536.0
playery = 850.0
playerx_change = 0

def player(x,y):
    screen.blit(playerimg,(x,y))

#the enemies
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
for i in range(5):
    enemyimg.append(pygame.image.load('ufo.png'))
    enemyx.append(random.randint(0,1136))
    enemyy.append(0)
    enemyx_change.append(1.5)
    enemyy_change.append(0)

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

#the bullets
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 850
bullety_change = 7
bullet_state = "ready"

def firebullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg,(x+48,y+1))


def iscollision(x1,y1,x2,y2):
    dist = math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))
    if dist <64: return True
    else: return False

score = 0

score_font = pygame.font.Font('freesansbold.ttf',48)
def show_score():
    score_text = score_font.render('Score : ' + str(score), True, (255,255,255))
    screen.blit(score_text,(500,520))

over_font = pygame.font.Font('freesansbold.ttf',72)
def game_over():
    over_text = over_font.render('GAME OVER', True, (255,255,255))
    screen.blit(over_text,(378,450))

running = True

while running:

    screen.fill((0,0,0))
    
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
    
        if event.type==pygame.QUIT:
            running = False
        
        
        if event.type == pygame.KEYDOWN:
    
            if event.key == pygame.K_LEFT:
                playerx_change = -2
    
            if event.key == pygame.K_RIGHT:
                playerx_change = 2
    
            if event.key == pygame.K_SPACE:
    
                if bullet_state == "ready":
                    bulletx=playerx
                    firebullet(bulletx,bullety)
                    bullet_sound = mixer.Sound('bullet.wav')
                    bullet_sound.play()
        
        if event.type==pygame.KEYUP:
    
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
    
    playerx +=playerx_change
    if playerx<=0:
        playerx=0
    elif playerx>=1072:
        playerx=1072

    
    if bullety<=0:
        bullety=850
        bullet_state="ready"
    
    if bullet_state=="fire":
        firebullet(bulletx,bullety)
        bullety -= bullety_change

    for i in range(5):
        
        if enemyy[i] >= 750:
            for j in range(5):
                enemyy[j]=2000
            playery = 2000
            bullet_state="over"
            game_over()
            show_score()
            pygame.mixer.music.pause()
            break

        enemyx[i] +=enemyx_change[i]
        if enemyx[i]<=0:
            enemyx[i]=0
            enemyx_change[i]*=-1
            enemyy[i]+=40
        elif enemyx[i]>=1072:
            enemyx[i]=1072
            enemyx_change[i]*=-1
            enemyy[i]+=40

        collision = iscollision(enemyx[i]+32,enemyy[i]+32,bulletx+16,bullety)


        if collision:
            bullety=850
            bullet_state="ready"
            score += 1
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
            enemyx[i] = random.randint(0,1136)
            enemyy[i] = 0


        enemy(enemyx[i],enemyy[i],i)

    player(playerx,playery)
    pygame.display.update()


