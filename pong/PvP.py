import pygame
import os
from pygame import mixer
pygame.font.init()
pygame.mixer.init()
WIDTH , HEIGHT = 900 , 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pongers")
mixer.music.load(os.path.join('Assets','music2.mp3'))
mixer.music.set_volume(0.1)
mixer.music.play(-1)

BLACK  = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)

FPS = 60

BALL_COLLIDE_SOUND = pygame.mixer.Sound(os.path.join('Assets','boing.mp3'))
GOAL_SOUND = pygame.mixer.Sound(os.path.join('Assets','Collision.mp3'))

PADDLE_WIDTH = 15
PADDLE_HEIGHT = 50
BALL_BLOCK = 20

BORDER = pygame.Rect(WIDTH/2 - 5,0,10,HEIGHT)

GOAL_LEFT = pygame.USEREVENT + 2
GOAL_RIGHT = pygame.USEREVENT + 3

VEL = 10
BALL_VEL = 4

SCORE_FONT = pygame.font.Font(os.path.join('Assets','INVASION2000.ttf'),30)
TITLE_FONT = pygame.font.Font(os.path.join('Assets','INVASION2000.ttf'),50)

ball_x = WIDTH / 2
ball_y = HEIGHT / 2

left = pygame.Rect(100,100,PADDLE_WIDTH,PADDLE_HEIGHT)
right = pygame.Rect(800,100,PADDLE_WIDTH,PADDLE_HEIGHT)

def handle_left_movement(keys_pressed,left):
    if keys_pressed[pygame.K_s] and left.y + VEL + left.height < HEIGHT:
        left.y += VEL
    if keys_pressed[pygame.K_w] and left.y - VEL > 0:
        left.y -= VEL
def handle_right_movement(keys_pressed,right):
    if keys_pressed[pygame.K_DOWN]and right.y + VEL + right.height < HEIGHT:
        right.y += VEL
    if keys_pressed[pygame.K_UP]and right.y - VEL > 0:
        right.y -= VEL
    
class Ball():
    def __init__(self,x,y):
        self.reset(x,y)
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > HEIGHT:
            self.speed_y *= -1

        if self.rect.colliderect(left):
            BALL_COLLIDE_SOUND.play()
            self.speed_x *= -1
            self.speed_y *= -1
        if self.rect.colliderect(right):
            BALL_COLLIDE_SOUND.play()
            self.speed_x *= -1
            self.speed_y *= -1

        if self.rect.left < 0:
            pygame.event.post(pygame.event.Event(GOAL_RIGHT))
        if self.rect.right > WIDTH:
            pygame.event.post(pygame.event.Event(GOAL_LEFT))

    def reset(self,x,y):
        self.x = x
        self.y = y
        self.ball_rad = 8
        self.rect = pygame.Rect(self.x,self.y,self.ball_rad * 2,self.ball_rad * 2)
        self.speed_x = -BALL_VEL
        self.speed_y = BALL_VEL
    def draw(self):
        pygame.draw.circle(WIN,WHITE,(self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)




def draw_window(left,right,ball,rscore,lscore):
    WIN.fill(BLACK)
    lscr = SCORE_FONT.render(f'Score: {lscore}',True,WHITE)
    rscr = SCORE_FONT.render(f'Score: {rscore}',True,WHITE)
    tit = TITLE_FONT.render('PONGERS',True,WHITE)
    WIN.blit(lscr, (10,10))
    WIN.blit(rscr,(WIDTH-rscr.get_width() - 10,10))
    WIN.blit(tit,(WIDTH/2-tit.get_width() / 2,0))
    pygame.draw.rect(WIN,WHITE,BORDER)
    pygame.draw.rect(WIN,WHITE,[left.x,left.y,PADDLE_WIDTH,PADDLE_HEIGHT])
    pygame.draw.rect(WIN,WHITE,[right.x,right.y,PADDLE_WIDTH,PADDLE_HEIGHT])
    ball.draw()
    pygame.display.update()
def game():
    global left
    global right
    run = True
    clock = pygame.time.Clock()
    ball = Ball(WIDTH/2, HEIGHT / 2)
    rscore = 0
    lscore = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == GOAL_RIGHT:
                GOAL_SOUND.play()
                rscore += 1
                pygame.time.delay(1000)
                ball.reset(ball_x,ball_y)
            if event.type == GOAL_LEFT:
                GOAL_SOUND.play()
                lscore += 1
                pygame.time.delay(1000)
                ball.reset(ball_x,ball_y)
            

        keys_pressed = pygame.key.get_pressed()
        handle_left_movement(keys_pressed,left)
        handle_right_movement(keys_pressed,right)
        ball.move()
        draw_window(left,right,ball,rscore,lscore)
if __name__ == '__main__':
    game()