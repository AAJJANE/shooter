#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, w , h, x, y, img, speed):
       super().__init__()
       self.image = transform.scale(image.load(img), (w,h))
       self.speed = speed
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        k = key.get_pressed() # Получаем нажатую клавишу
        if k[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if k[K_d] and self.rect.x < w - 70:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(15, 20, self.rect.centerx, self.rect.top, "bullet.png", 25 )
        bullets.add(bullet)

       

score = 0
lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > h:
            lost += 1
            self.rect.y = 0 
            self.rect.x = randint(80, w - 80)  

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
     
                    

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

font.init()
font = font.SysFont('Arial', 40)

fire_sound = mixer.Sound('fire.ogg')


w, h = 700, 500
display.set_caption("Shooter")
window = display.set_mode((w,h))
bg = transform.scale(image.load("galaxy.jpg"), (w,h))
player = Player(80, 100 , 300, 400,"rocket.png", 10)


monsters = sprite.Group()
for i in range(5):
    monster = Enemy(80,50, randint(80, w - 80), -50, "ufo.png", randint(1,10))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(5):
    asteroid = Enemy(80,50, randint(80, w - 80), -50, "asteroid.png", randint(1,10))
    asteroids.add(asteroid)


bullets = sprite.Group()

life = 5

rel_time = False
num_fire = 0

run = True
finish = False
auto = False
while run :
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()

                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()
        

            if e.key == K_r:
                finish = False
                monsters.empty()
                bullets.empty()
                score = 0
                lost = 0
                for i in range(5):
                    monster = Enemy(80,50, randint(80, w - 80), -50, "ufo.png", randint(1,10))
                    monsters.add(monster)

                for i in range(5):
                        asteroid = Enemy(80,50, randint(80, w - 80), -50, "asteroid.png", randint(1,10))
                        asteroids.add(asteroid)
    
    if not finish:

        window.blit(bg, (0,0))
        
        text_count = font1.render("Счёт : " + str(score), 1 , (0,255,255))
        text_count1 = font1.render("Пропущено: " + str(lost), 1 , (0,255,255))
        lifes = font1.render("Жизни: " + str(life), 1 , (0,255,255))
        
    
        window.blit(text_count, (10, 25))
        window.blit(text_count1, (10, 50))
        window.blit(lifes, (500, 50))

        
        player.update()

        
        player.reset()
        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update() 

        if rel_time == True:
            now_start = timer()
            if now_start - last_time < 3:
                wait = font1.render("Wait reload...", 1 , (0,255,255))
                window.blit(wait, (500, 400 ))

            else:
                num_fire = 0
                rel_time = False

        cols = sprite.groupcollide(monsters, bullets, True, True)
        for c in cols:
            monster = Enemy(80,50, randint(80, w - 80), -50, "ufo.png", randint(1,10))
            monsters.add(monster)
            score += 1



        if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, asteroids, True):
            life -= 1
            lost += 1
            lifes = font1.render("Жизни: " + str(life), 1 , (0,255,255)) 
            window.blit(lifes, (500, 50))
            
        if life <= 0:
            finish = True
            text_lose = font1.render("You Lost!", 1, (0,255,255))
            window.blit(text_lose, (300, 250))

        if score >= 11:
            finish = True
            text_win = font1.render("You Won!", 1,(0,255,255))
            window.blit(text_win, (300, 250))
            window.blit(lifes, (500, 50))


        display.update()

    time.delay(100)