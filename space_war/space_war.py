# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1077
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
TITLE = "Balloon Tower Defense"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (139, 69, 19)


# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/Cleveland.otf", 73)


# Images
ship_img = pygame.image.load('assets/images/BTD5Towers.png').convert_alpha()
laser_img = pygame.image.load('assets/images/poop.png').convert_alpha()
enemyP_img = pygame.image.load('assets/images/PinkBalloon.png').convert_alpha()
enemyY_img = pygame.image.load('assets/images/YellowBalloon.png').convert_alpha()
enemyG_img = pygame.image.load('assets/images/GreenBalloon.png').convert_alpha()
enemyB_img = pygame.image.load('assets/images/BlueBalloon.png').convert_alpha()
enemyR_img = pygame.image.load('assets/images/RedBalloon.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/bullet.png').convert_alpha() 
backround_img = pygame.image.load('assets/images/BackroundBTD.jpg').convert_alpha() 
boss_img = pygame.image.load('assets/images/Boss.png').convert_alpha()  
powerup_img = pygame.image.load('assets/images/chug.png').convert_alpha()
powerupRP_img = pygame.image.load('assets/images/RF.png').convert_alpha()
Super_img = pygame.image.load('assets/images/Super.png').convert_alpha()

# Sounds
shoot_sound = pygame.mixer.Sound('assets/sounds/Boomerang.wav')
boomboy = pygame.mixer.Sound('assets/sounds/pop.wav')
pygame.mixer.music.load('assets/sounds/fallout.ogg')

# Stages
START = 0
PLAYING = 1
LOSE = 2
WIN = 3

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask =  pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.max_health = 3
        self.health = self.max_health
        self.rapidfire_timer = 0
        self.hits = 0
        self.speed = 10
    
    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed


    def shoot(self):
        print("pew!")
        shoot_sound.play()

        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)
        
    def update(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        hit_list = pygame.sprite.spritecollide(self, powerups, True, pygame.sprite.collide_mask)

        for hit in hit_list:
            hit.apply(self)

        hit_list = pygame.sprite.spritecollide(self, bombs, True,pygame.sprite.collide_mask)
        if len(hit_list) > 0:
            self.health -= 1

        if self.rapidfire_timer > 0:
            self.rapidfire_timer -= 1
            
        if self.health == 0:
            self.kill()

        if self.rapidfire_timer == 0:
            self.image = ship.image


            
class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        
        self.image = image
        self.mask =  pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.mask =  pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 10
        
    def drop_bomb(self):
        print("bomb noise")
        shoot_sound.play()

        bomb = Bomb(bomb_img)
        self.mask =  pygame.mask.from_surface(self.image)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
        
    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)

        for hit in hit_list:
            print("boom")
            boomboy.play()
            self.health -= 1
        if self.health <= 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.mask =  pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 5

        
    def drop_bomb(self):
        print("bomb noise")
        shoot_sound.play()

        bomb = Bomb(bomb_img)
        self.mask =  pygame.mask.from_surface(self.image)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
        
    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)

        if self.health == 4:
            self.image = enemyY_img
            
        if self.health == 3:
            self.image = enemyG_img

        if self.health == 2:
            self.image = enemyB_img

        if self.health == 1:
            self.image = enemyR_img

            
        for hit in hit_list:
            print("boom")
            boomboy.play()
            self.health -= 1
        if self.health <= 0:
            self.kill()

        if len(hit_list) > 0:
            player.score += 100
            print(player.score)



class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        
        self.image = image
        self.mask =  pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.speed = 15

    def update(self):
        self.rect.y += self.speed
        
        if self.rect.top > HEIGHT:
            self.kill()

class ShootPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        
    def apply(self, ship):
        ship.rapidfire_timer = 2 * refresh_rate
        ship.image = Super_img

    def update(self):
        self.rect.y += self.speed
        
        if self.rect.top > HEIGHT:
            self.kill()

class HealthPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 9
        
        self.speed = 10
        
    def apply(self, ship):
        ship.health = 3

    def update(self):
        self.rect.y += self.speed
        
        if self.rect.top > HEIGHT:
            self.kill()
            
class Fleet():
    def __init__(self,mobs):
        self.mobs = mobs
        self.speed = 5
        self.moving_right = True
        self.drop = 30
        self.moving_right = True
        self.bomb_rate = 20
        self.boss_added = False
        
    def move(self):
        hits_edge = False

        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True
            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True
                
        if hits_edge:
            self.reverse()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop
            
    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def add_boss(self):
        boss = Boss(400, 25, boss_img)
        mobs.add(boss)
        self.boss_added = True


    def update(self):
        self.move()  
        self.choose_bomber()

        if len(mobs) == 3 and self.boss_added == False:
            self.add_boss()
    
# Game helper functions
def display_statistics():
    health_txt = FONT_XL.render(str(ship.health), 1, RED)
    screen.blit(health_txt, [80, 20])

    score_txt = FONT_XL.render(str(player.score), 1, YELLOW)
    screen.blit(score_txt, [820, 20])

def show_title_screen():
    title_text = FONT_XL.render("Balloon Tower Defense", 1, WHITE)
    screen.blit(title_text, [20, 300])

def show_win_screen():
    text1 = FONT_XL.render("You win", True, WHITE)
    text2 = FONT_XL.render("Press 'r' to restart", True, WHITE)

    screen.blit(text1, [250, 300])
    screen.blit(text2, [0, 350])

def show_lose_screen():
    text1 = FONT_XL.render("You lose", True, WHITE)
    text2 = FONT_XL.render("Press 'r' to restart", True, WHITE)

    screen.blit(text1, [250, 300])
    screen.blit(text2, [0, 350])

def draw_healthbar(player):
    height_ratio = 0.05
    ratio = player.health / player.max_health

    if ratio > .67:
        color = GREEN
    elif ratio > .34:
        color = YELLOW
    else:
        color = RED

    bar_length = ratio * (player.rect.width - 10)
    height = height_ratio *  player.rect.height

    pygame.draw.rect(screen, WHITE, [player.rect.x + 5, player.rect.bottom + 5, player.rect.width - 10, height])
    pygame.draw.rect(screen, color, [player.rect.x + 5, player.rect.bottom + 5, bar_length, height])


def setup(): 
    global stage, done, player, ship, lasers, mobs, fleet, bombs, score, powerups
    
    ''' Make game objects '''
    ship = Ship(364, 680, ship_img)

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)

    player.score = 0
    
    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    mob1 = Mob(100, 200, enemyP_img)
    mob2 = Mob(200, 200, enemyP_img)
    mob3 = Mob(300, 200, enemyP_img)
    mob4 = Mob(400, 200, enemyP_img)
    mob5 = Mob(500, 200, enemyP_img)
    mob6 = Mob(600, 200, enemyP_img)
    mob7 = Mob(700, 200, enemyP_img)
    mob8 = Mob(800, 200, enemyP_img)
    mob9 = Mob(900, 200, enemyP_img)

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9)

    powerup1 = HealthPowerUp(200, -4000, powerup_img)
    powerup2 = ShootPowerUp(600, -7000, powerupRP_img)
    
    powerups = pygame.sprite.Group()
    powerups.add(powerup1, powerup2)

    fleet = Fleet(mobs)
    
    ''' set stage '''
    stage = START
    done = False
    
def check_win():
    global stage
    if len(mobs) == 0:
        stage = WIN
    
# Game loop
pygame.mixer.music.play(-1)

setup()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
            if stage == LOSE:
                if event.key == pygame.K_r:
                    setup()
            if stage == WIN:
                if event.key == pygame.K_r:
                    setup()
                    
    pressed = pygame.key.get_pressed()
    
    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        if pressed[pygame.K_UP]:
            ship.move_up()
        elif pressed[pygame.K_DOWN]:
            ship.move_down()
            
        if ship.rapidfire_timer > 0 and pressed[pygame.K_SPACE]:
            ship.shoot()

                    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update()
        lasers.update()
        bombs.update()
        fleet.update()
        mobs.update()
        check_win()
        powerups.update()
        
    if ship.health == 0:
        stage = LOSE
        

    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.blit(backround_img, [0,0])
    lasers.draw(screen)
    bombs.draw(screen)
    player.draw(screen)
    mobs.draw(screen)
    display_statistics()
    powerups.draw(screen)
    draw_healthbar(ship)
    
    if stage == START:
        show_title_screen()

    if stage == LOSE:
        show_lose_screen()

    if stage == WIN:
        show_win_screen()

    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
