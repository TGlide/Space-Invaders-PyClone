from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.sound import *
from PPlay.font import *
from time import sleep, time
from os import getcwd
from random import choice, randint
from helpers import *


def play(wn, dif):
    class Ship:
        def __init__(self, x, y):
            self.sprite = Sprite(get_asset("ship.png"), 1, size=(
                int(80*(wn.width/1366)), int(85*(wn.height/768))))

            self.x = x - self.sprite.width/2
            self.y = y - self.sprite.height/2

            self.speed = 0
            self.max_speed = [600, 500, 250][dif-1]
            self.accel = 2000

            self.bullets = []
            self.b_timer = time()
            self.interval = [0.5, 0.75,  1][dif-1]
            self.max_bullets = [3, 2, 1][dif-1]

            self.lives = 3

            self.dead = False
            self.dead_timer = None

            self.shoot_sound = Sound(get_asset("shoot.ogg"))

        def move_key_x(self):
            if Window.get_keyboard().key_pressed("left"):
                if self.speed > -self.max_speed:
                    self.speed -= self.accel * wn.delta_time()
            elif Window.get_keyboard().key_pressed("right"):
                if self.speed < self.max_speed:
                    self.speed += self.accel * wn.delta_time()
            else:
                if self.speed > 0:
                    self.speed -= self.accel * wn.delta_time()
                elif self.speed < 0:
                    self.speed += self.accel * wn.delta_time()
            self.x += self.speed*wn.delta_time()
            if self.x + self.sprite.width > wn.width:
                self.x = wn.width - self.sprite.width
                self.speed = 0
            elif self.x < 0:
                self.x = 0
                self.speed = 0

        def draw(self):
            self.sprite.draw()

        def update(self):
            self.sprite.set_position(self.x, self.y)

            for b in self.bullets[:]:
                b.update()
                if b.despawn:
                    self.bullets.remove(b)
                else:
                    b.draw()

        def shoot(self):
            if Window.get_keyboard().key_pressed("space"):
                if len(self.bullets) < self.max_bullets and time() - self.b_timer >= self.interval:
                    self.bullets.append(
                        Bullet(self.x + self.sprite.width/2, self.y, origin="ship"))
                    self.b_timer = time()
                    self.shoot_sound.play()

        def bullet_hit(self, enemy_horde):
            for b in enemy_horde.bullets:
                if self.sprite.collided(b.sprite):
                    self.dead = True
                    self.lives -= 1
                    self.dead_timer = time()
    class Bullet:
        def __init__(self, x, y, origin):
            self.sprite = Sprite(get_asset("bullet.png"), 1, size=(10, 10))

            self.x = x - self.sprite.width/2
            self.y = y + self.sprite.height

            self.speed = 400 * [-1, 1][origin == "ship"]

            self.despawn = False

        def update(self):
            self.y -= self.speed * wn.delta_time()
            if self.y <= 0 or self.y + self.sprite.height > wn.height:
                self.despawn = True
            self.sprite.set_position(self.x, self.y)

        def draw(self):
            self.sprite.draw()

    class Enemy(Sprite):
        sound = Sound(get_asset("fastinvader1.ogg"))
        def __init__(self):
            Sprite.__init__(self, get_asset("alien.png"), 1)
            self.bullet = None

        def shoot(self):
            if self.bullet and self.bullet.despawn:
                del(self.bullet)
                self.bullet = None
            if not self.bullet:
                if randint(0, 10000) > 9990:
                    self.bullet = Bullet(self.x + self.width/2, self.y + self.height, origin="alien")
                    return self.bullet

    class EnemyHorde:
        def __init__(self, x, y, rows, columns, interval_change=0):
            self.sprite_img = get_asset("alien.png")
            self.base = Sprite(self.sprite_img, 1)

            self.enemies = [[Enemy() for c in range(columns)]
                            for r in range(rows)]
            self.enemies_left = rows*columns

            self.rows = rows
            self.columns = columns

            self.direction = 1  # 0 == Left, 1 == Right
            self.dist_to_move = [20, 25, 30][dif-1]
            self.interval = [0.4, 0.3, 0.25][dif-1] - interval_change
            self.interval_dif = self.interval/10
            self.min_interval = 0.075
            self.time = time()

            self.bullets = []
            self.max_bullets = [1,2,3][dif-1]

            self.set_pos(x, y)

        def draw(self):
            """Draws all enemies from self.enemies to window"""
            for r in range(self.rows):
                for c in range(self.columns):
                    if self.enemies[r][c] != 0:
                        self.enemies[r][c].draw()
            
            for b in self.bullets[:]:
                if b:
                    if b.despawn:
                        self.bullets.remove(b)
                    b.update()
                    b.draw()

        def bullet_hit(self, ship):
            """Eliminates hit eneimes"""
            enemy_count = 0

            for r in range(self.rows):
                for c in range(self.columns):
                    if self.enemies[r][c] != 0:
                        for bullet in ship.bullets[:]:
                            if self.enemies[r][c].collided(bullet.sprite):
                                self.enemies[r][c] = 0
                                ship.bullets.remove(bullet)
                                enemy_count += 1
                                self.enemies_left -= 1
                                break
            return enemy_count

        def set_pos(self, x, y):
            """Set positions of all enemies based on x, y of horde"""
            self.x = x
            self.y = y
            for r in range(self.rows):
                for c in range(self.columns):
                    if self.enemies[r][c] != 0:

                        self.enemies[r][c].set_position(
                            x+(self.base.width * c) + 50*c, y+(self.base.height*r) + 10*r)

        def enemyRight(self):
            """Returns the enemy at the rightmost position"""
            row = -1
            column = -1
            for r in range(self.rows):
                rl = self.enemies[r]
                big = max([rl.index(i) for i in rl if i != 0] + [-1])
                if big > column:
                    column = big
                    row = r
            return self.enemies[row][column]

        def enemyLeft(self):
            """Returns the enemy at the leftmost position"""
            row = self.rows
            column = self.columns
            for r in range(self.rows):
                rl = self.enemies[r]
                small = min([rl.index(i)
                             for i in rl if i != 0] + [self.columns])
                if small < column:
                    column = small
                    row = r
            return self.enemies[row][column]

        def move(self):
            if time() - self.time >= self.interval and self.enemies_left != 0:
                self.time = time()
                Enemy.sound.play()
                if self.enemyRight().x + self.base.width > wn.width or self.enemyLeft().x < 0:
                    self.interval = (self.interval - self.interval_dif if self.interval >
                                      self.min_interval else self.min_interval)
                                      
                    self.direction = (self.direction + 1) % 2
                    self.set_pos(
                        self.x + [-self.dist_to_move, self.dist_to_move][self.direction], self.y + 10)
                else:
                    self.set_pos(
                        self.x + [-self.dist_to_move, self.dist_to_move][self.direction], self.y)
        
        def shoot(self):
            for c in range(self.columns):
                for r in range(self.rows-1, -1, -1):
                    if len(self.bullets) >= self.max_bullets:
                        break
                    if type(self.enemies[r][c]) == Enemy:
                        b = self.enemies[r][c].shoot()
                        if b:
                            self.bullets.append(b)
                        break

    class Score:
        def __init__(self):
            self.score = "0"

            self.font = Font("0" * (4-len(self.score)) + self.score,
                             font_family=font_path("arcadeclassic"),
                             size=70,
                             color=(255, 255, 255),
                             local_font=True)

            self.font.set_position(wn.width/2 - self.font.width/2, 10)

        def add(self, n):
            self.score = str(int(self.score) + n)
            self.font.change_text("0" * (4-len(self.score)) + self.score)
            self.font.set_position(wn.width/2 - self.font.width/2, 10)

    ########
    # Main #
    ########
    fundo = GameImage(get_asset("bg.jpeg"), size=(wn.width, wn.height))
    ship = Ship(wn.width/2, wn.height - 100)
    score = Score()
    horde = EnemyHorde(10, score.font.y + score.font.height + 10, 5, 7)
    wave = 1
    wave_text = Font("Wave %d" % wave, font_family=font_path("arcadeclassic"), color=(255,255,255), local_font=True, aa=True, size=42)
    
    wave_text.set_position(wn.width/2 - wave_text.width/2, wn.height/2 - wave_text.height/2)
    wave_text_timer = time()

    while True:
        if Window.get_keyboard().key_pressed("esc"):
            return

        if horde.enemies_left <= 0:
            ship.sprite.set_position(wn.width/2 - ship.sprite.width/2, wn.height - 100)
            horde = EnemyHorde(10, score.font.y + score.font.height + 10, 5, 7, interval_change=0.1*(wave-1))
            wave += 1
            wave_text.change_text("Wave %d" % wave)
            wave_text_timer = time()

        fundo.draw()

        if time() - wave_text_timer < 5:
            wave_text.draw()
        elif ship.dead:
            if time() - ship.dead_timer >=3:
                ship.dead = False
            horde.bullets = []
            ship.bullets = []
            ship.draw()
            horde.draw()
            score.font.draw()

        else:
            ship.move_key_x()
            ship.bullet_hit(horde)
            ship.shoot()
            ship.update()
            ship.draw()

            killed = horde.bullet_hit(ship)
            score.add(5*killed)
            horde.move()
            horde.shoot()
            horde.draw()

            score.font.draw()

        wn.update()


if __name__ == "__main__":
    wn = Window(1200,900)
    dif = 1
    play(wn, dif)
