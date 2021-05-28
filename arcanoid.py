from pygame import *
from time import time as timer

 
Lives = 3
Score = 0
Combo = 0

speed_y = 5
speed_x = 5

game = True
clock = time.Clock()
FPS = 144


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 1085:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 1085:
            self.rect.x += self.speed

class Ball(GameSprite):
    def update(self):
        pass


bricks = sprite.Group()
brick_x = 0
brick_y = 0
for i in range(5):
    for j in range(10):
        brick = GameSprite('brick.png', brick_x, brick_y, 128, 32, 0)
        bricks.add(brick)
        brick_x += 128
    brick_y += 32
    brick_x -= 10 * 128


window = display.set_mode((1280,720))
display.set_caption('Arcanoid')
background = transform.scale(image.load('background.png'), (1280, 720))
paddle = Player('paddle.png', 640, 650, 200, 65, 6)
ball = Ball('Ball.png', 610, 380, 50, 50, 1)

balls = sprite.Group()
balls.add(ball)

font.init()
font2 = font.SysFont('Arial', 24)

#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False    
    score_text = font2.render('Счет: ' +str(Score), 1, (255,255,255))
    combo_text = font2.render('Комбо: '+str(Combo), 1, (255, 255, 255))       
    lives_text = font2.render('Жизни: '+str(Lives), 1, (255, 255, 255))        
    window.blit(background,(0,0))
    #window.blit(combo_text, (10,20))
    paddle.update()
    paddle.reset()
    ball.reset()
    ball.update()
    bricks.update()
    bricks.draw(window)
    window.blit(score_text, (10,0))
    window.blit(lives_text,(10,20))
    display.update()
    if game == True:
        ball.rect.x += speed_x
        ball.rect.y += speed_y
        if ball.rect.y < 0:
            speed_y *= -1
        if ball.rect.x < 0:
            speed_x *= -1
        if ball.rect.x > 1280:
            speed_x *= -1
        if ball.rect.y >= 720:
            ball.rect.y = 300
            ball.rect.x = 610
            speed_x = 3
            speed_x = 3
            Lives -= 1
        if sprite.collide_rect(ball, paddle):
            speed_y *= -1
        if sprite.spritecollide(ball, bricks, True):
            speed_y *= -1
            speed_x *= 1
            bricks.remove(brick)
            Score += 1
        if Lives <= 0:
            quit()
        
        if Score == 43:
            time.delay(5000)
            quit()
    clock.tick(FPS)