from pygame import *
from  random import randint
from time import sleep

level = 0
hard = 0

mixer.init()
fire_sound = mixer.Sound('fire.ogg')
probitie_sound = mixer.Sound('probitie.ogg')
img_back = "galaxy.png"
img_hero = "rocket.jpg"
img_enemy = "ufo.png"
img_bullet = 'bullet.png'

font.init()
font2 = font.Font(None, 36)
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!!', True, (0, 255, 0))
lose = font1.render('YOU LOSE!!', True, (255, 0, 0))

score = 0
lost = 0
goal = 30
max_lost = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1
            probitie_sound.play()

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


print("введите нужное число очков для победы, и пропусков для пройгрыша \n по умолчанию стоит 30; 3 \n -1 очков для выйгрыша - бесконечный режим ( набивай очки сколько хочешь) \n -1 пропусков - бесконечность жизней (пропускай сколько хочешь) ")
goal = int(input('кол-во очков для победы \n'))
max_lost = int(input('кол-во пропусков для пройгрыша \n'))

win_width = 700
win_height = 500
display.set_caption('Драка Roblox Queen с анансом и майонезом')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint( 80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

finish = False
biba_kolonizator = True
while biba_kolonizator:
    for e in event.get():
        if e.type == QUIT:
            biba_kolonizator = False
        elif e.type == MOUSEBUTTONDOWN:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background, (0, 0))

        text = font2.render('Счёт:' +str(score), 1, (0, 0, 0))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (0, 0, 0))
        window.blit(text_lose, (10, 50))

        ship.update()
        monsters.update()

        ship.reset()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint( 80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if lost == max_lost:
            window.blit(lose, (250, 250))
            finish = True
        
        if score == goal:
            window.blit(win, (250, 250))
            finish = True

        display.update()
    time.delay(20)
#