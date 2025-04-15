"""
Les différentes classes d'ennemis.

CLASSES
- Drone (Entity)
- Destroyer (Entity)

- SpieDrone (Entity)
- Fregat (Entity)
- Cruiser (Entity)
- Dreadnought (Entity)
"""

import pyxel
from sounds import Musicien
from projectile import Projectile, Lazerbeam
from constants import *
import random

DEBUGGER.set_filename('enemies.py')

class Drone:
    '''
    Entity : le Drone est l'ennemi de base.

    ATTRIBUTS
    - x : position x du Drone
    - y : position y du Drone
    - dead : si l'astronef est vivant ou non
    - anim_reacteurs : liste contenant l'état de l'animation des réacteurs et le sens de l'animation
    - hitbox : hitbox du Drone (x, y, w, h) immuable

    METHODS
    - update
    - draw
    - update_animation
    '''
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
        self.dead = False
        self.anim_reacteurs = [0, True]
        self.hitbox = (0, 0, 8, 10) # x, x+w, y, y+h

    def __str__(self):
        return f"Drone (x{self.x}, y{self.y})"

    def update(self, game_speed, score):
        """Met à jour le Drone"""
        self.y += 1 * game_speed
        if score >= SCORE_DRONE_SPEED1:
            self.y += 0.1 * game_speed
        if score >= SCORE_DRONE_SPEED2:
            self.y += 0.1 * game_speed
        if score >= SCORE_DRONE_SPEED3:
            self.y += 0.1 * game_speed
        if score >= SCORE_DRONE_SPEED4:
            self.y += 0.1 * game_speed
        self.update_animation()

    def draw(self):
        """Dessine le Drone"""
        pyxel.blt(self.x, self.y, 0, 0, 0, 8, 16, colkey=0, scale=SPACESHIP_SCALE)
        pyxel.rect(self.x+3, self.y-self.anim_reacteurs[0], 1, 2+self.anim_reacteurs[0], 10) # réacteur de poupe central
        if DEBUGGER.get_var('show hitbox'):
            hbx, hby, hbw, hbh = self.hitbox
            pyxel.rectb(self.x+hbx, self.y+hby, hbw, hbh, 8)
        
    def update_animation(self):
        """Animation des réacteurs"""
        if self.anim_reacteurs[1]:
            self.anim_reacteurs[0] += 1
            if self.anim_reacteurs[0] > 3:
                self.anim_reacteurs[1] = False
        else:
            self.anim_reacteurs[0] -= 1
            if self.anim_reacteurs[0] < 1:
                self.anim_reacteurs[1] = True


class Destroyer:
    '''
    Entity : le Destroyer est un mini-boss du jeu.

    ATTRIBUTS
    - x : position x du Destroyer
    - y : position y du Destroyer
    - active : booléen indiquant si le Destroyer est actif ou non
    - health : points de vie du Destroyer
    - dead : si l'astronef est vivant ou non
    - projectiles : liste des projectiles du Destroyer
    - hitbox : hitbox du Destroyer (x, y, w, h) immuable

    METHODS
    - create
    - update
    - draw
    - fire
    - disactive
    '''
    def __init__(self):
        self.x = 100
        self.y = -30
        self.active = False
        self.health = DESTROYER_LIFE
        self.dead = False
        self.projectiles = []
        self.shoot_state = 1
        self.hitbox = (0, 0, 16, 16) # x, y, w, h
        self.anim_reacteurs = [0, True]
        self.play_the_sound = Musicien()

    def __str__(self):
        return f"[{self.health}pv]Destroyer (x{self.x}, y{self.y})"

    def create(self):
        self.x = random.randint(GAME_SCREEN_WIDTH_START+16, SCREEN_WIDTH-16)
        self.y = random.randint(-15, -5)
        self.health = DESTROYER_LIFE
        self.active = True

    def update(self, game_speed, score):
        """met à jour la position du destroyer et le fait tirer aléatoirement"""
        if self.active:
            self.y += 1 * game_speed
            fire_rate = DESTROYER_FIRE_RATE
            if score >= SCORE_DESTROYER_FIRE_RATE:
                fire_rate = fire_rate * 2
            if random.randint(0, 1000) <= fire_rate:
                self.fire()
        self.update_animation()

    def update_projectiles(self, game_speed):
        """
        mise à jour de la position des lazers
        appelée dans Game pour éviter la disparition des lazers lors de la mort du destroyer
        """
        for destlazer in self.projectiles:
            destlazer.update(game_speed)
            if destlazer.y < -8 or destlazer.target_hit:
                self.projectiles.remove(destlazer)

    def draw(self):
        """affiche le destroyer à l'écran"""
        if self.active:
            pyxel.rect(self.x+7, self.y+4-self.anim_reacteurs[0], 2, self.anim_reacteurs[0], 10)
            pyxel.blt(self.x, self.y, 0, 16, 0, 16, 16, colkey=0, scale=SPACESHIP_SCALE)
            # barre de vie
            if self.health != DESTROYER_LIFE:
                pyxel.rect(self.x+8-(self.health//2), self.y+20, self.health, 1, 3)
        if DEBUGGER.get_var('show hitbox'):
            hbx, hby, hbw, hbh = self.hitbox
            pyxel.rectb(self.x+hbx, self.y+hby, hbw, hbh, 8)
    
    def draw_projectiles(self):
        """dessine les projectiles du destroyer. Géré séparément dans Game pour éviter la disparition des lazers lors de la mort du destroyer"""
        for projectile in self.projectiles:
            projectile.draw()

    def fire(self):
        """génère un tir du destroyer"""
        fire_all = (random.randint(0, 6) == 6)
        if fire_all or self.shoot_state == 0:
            self.play_the_sound.lazer()
            self.projectiles.append(Projectile('destlazer', self.x+5, self.y+10, 3, 1))
            self.shoot_state = 1
        elif fire_all or self.shoot_state == 1:
            self.play_the_sound.lazer()
            self.projectiles.append(Projectile('destlazer', self.x+11, self.y+10, 3, 1))
            self.shoot_state = 0

    def update_animation(self):
        """Animation des réacteurs"""
        if self.anim_reacteurs[1]:
            self.anim_reacteurs[0] += 1
            if self.anim_reacteurs[0] > 3:
                self.anim_reacteurs[1] = False
        else:
            self.anim_reacteurs[0] -= 1
            if self.anim_reacteurs[0] < 1:
                self.anim_reacteurs[1] = True

    def disactive(self):
        """détruit l'astronef"""
        self.active = False
        self.dead = False
        self.y = -30
        self.health = 0


class Cruiser(Destroyer):
    '''
    Entity : le Destroyer est un spationef avec un grand nombre de vie et qui tire des rayons lazers

    ATTRIBUTS
    - health : int, nombre de points de vie

    METHODS
    - update
    - draw
    '''
    def __init__(self):
        super().__init__()
        self.health = CRUISER_HEALTH
        self.hitbox = (0, 0, 16, 24) # x, y, w, h
        self.lazerbeam_list = []
    
    def __str__(self):
        return f"[{self.health}pv]Cruiser (x{self.x}, y{self.y})"

    def update(self, game_speed, score):
        """met à jour la position du croiseur et le fait tirer aléatoirement"""
        if self.active:
            self.y += 0.8 * game_speed
            fire_rate = CRUISER_FIRE_RATE
            if score >= SCORE_CRUISER_FIRE_RATE:
                fire_rate = fire_rate * 2
            if random.randint(0, 1000) <= fire_rate:
                self.fire()
        self.update_animation()

    def draw(self):
        """dessine le croiseur à l'écran"""
        if self.active:
            pyxel.rect(self.x+3, self.y-self.anim_reacteurs[0], 2, 2+self.anim_reacteurs[0], 10)
            pyxel.rect(self.x+11, self.y-self.anim_reacteurs[0], 2, 2+self.anim_reacteurs[0], 10)
            pyxel.blt(self.x, self.y, 0, 32, 0, 16, 24, colkey=0, scale=SPACESHIP_SCALE)
            if self.health != CRUISER_HEALTH:
                pyxel.rect(self.x+8-(self.health//2), self.y+30, self.health, 1, 3)

            for lazerbeam in self.lazerbeam_list:
                lazerbeam.draw()
    
        if DEBUGGER.get_var('show hitbox'):
            hbx, hby, hbw, hbh = self.hitbox
            pyxel.rectb(self.x+hbx, self.y+hby, hbw, hbh, 8)

    def fire(self):
        """fait tirer un rayon lazer au croiseur"""
        self.lazerbeam_list.append(Lazerbeam('destlazer', self.x+7, self.y+20, 1))
        self.play_the_sound.lazebeam_load()

    def update_projectiles(self, game_speed):
        """
        mise à jour de la position des lazers du rayon lazer
        appelée dans Game pour éviter la disparition des lazers lors de la mort du croiseur
        """
        for lazerbeam in self.lazerbeam_list:
            lazerbeam.update_loading()
            for lazer in lazerbeam.list_lazer:
                lazer.update(game_speed)
                if lazer.y < -8 or lazer.target_hit:
                    lazerbeam.list_lazer.remove(lazer)
            if lazerbeam.state == 0 and len(lazerbeam.list_lazer) == 0:
                self.lazerbeam_list.remove(lazerbeam)
        # for destlazer in self.projectiles:
        #     destlazer.update(game_speed)
        
    def create(self):
        self.x = random.randint(GAME_SCREEN_WIDTH_START+16, SCREEN_WIDTH-16)
        self.y = random.randint(-15, -5)
        self.health = CRUISER_HEALTH
        self.active = True


class Spidrone(Drone):
    pass


class Frigat:
    pass


class Dreadnought:
    '''
    Entity : le Dreadnought est un spationef gigantesque armé de lazers et de tirs.
    Plutôt que de se déplacer vers le bas de l'écran, il reste en place et doit être détruit par le joueur.
    '''
    def __init__(self):
        self.health = DREADNOUGHT_LIFE
        self.x = -100
        self.y = -64
        self.active = False
        self.dead = False
        self.projectiles = []
        self.lazerbeam_list = []
        self.pattern_state = 0
        self.pattern_phase = [0, 0]
        self.in_animation = False
        self.hitbox = (0, 0, 56*2, 16*2) # x, y, w, h
        self.anim_reacteurs = [0, True]
        self.play_the_sound = Musicien()

        self.canon_coordinates = ( # NEED TO BE SCALED
            (7, 26), (10, 24), (13, 22), (16, 20), # left wing
            (22, 16), (24, 10), (32, 10), (30, 16), # head
            (49, 26), (46, 24), (43, 22), (40, 20) # right wing
            )
        self.lazerbeam_coordinates = ((8, 16), (20, 14), (48, 16), (36, 14))

    def __str__(self):
        return f"[{self.health}pv]Dreadnought (x{self.x}, y{self.y})"

    def create(self):
        self.x = (SCREEN_WIDTH - self.hitbox[2])//2
        self.y = -64
        self.health = DREADNOUGHT_LIFE
        self.active = True
        self.in_animation = True

        DEBUGGER.msg(f'Dreadnought spawned : {self}', 'INFO')

    def update(self, game_speed, score):
        """met à jour la position du dreadnought et gère ses patterns"""
        if self.active:
            if self.y < 32 :
                self.anim_advance(game_speed)
            else:
                if 0 < self.pattern_state <= 30*2:
                    self.execute_current_pattern()
                else:
                    self.choose_new_pattern(score)
        self.update_animation()

    def anim_advance(self, game_speed):
        """fait avancer le dreadnought"""
        self.y += 0.6 * game_speed
        if self.y >= 32:
            self.in_animation = False

    def choose_new_pattern(self, score):
        """
        choisit le pattern suivant en fonction du pattern actif
        
        Niveau 1
        1. Bouge d'un côté à l'autre, en tirant périodiquement (1.1 et 1.2)
        2. Déclenche une pluie de rayons lazers après avoir choisi une position (2.1, 2.2, 2.3, 2.4 et 2.5)
        3. Avance en tirant avec les canons normaux
        Niveau 2
        4. Part d'un côté à l'autre en reculant et en faisant feu de toutes ses armes (4.1 et 4.2)
        Niveau 3
        5. Active un bouclier et change de pattern
        Niveau 4
        6. Libère une escouade de drones devant lui (6.1, 6.2, 6.3, 6.4 et 6.5)
        """
        DEBUGGER.msg('choosing a new pattern', 'MSG')
        # choose pattern
        current_pattern = self.pattern_phase[0]
        if current_pattern == 1:
            self.pattern_phase[0] = random.choice((2, 2, 3, 3, 6))
        elif current_pattern == 2:
            self.pattern_phase[0] = random.choice((1, 1, 2, 2, 3))
        elif current_pattern == 3:
            self.pattern_phase[0] = 4
        elif current_pattern == 4:
            self.pattern_phase[0] = random.choice((1, 1, 5))
        elif current_pattern == 5:
            self.pattern_phase[0] = random.choice((1, 1, 2))
        elif current_pattern == 6:
            self.pattern_phase[0] = random.choice((1, 1, 5))
        else:
            self.pattern_phase[0] = random.choice((1, 1, 2, 5))

        # choose sub-pattern if there is one
        if current_pattern in (1, 4): # left or right type pattern
            self.pattern_phase[1] = random.randint(1, 2)
        if current_pattern in (2, 6): # from specific point type pattern
            self.pattern_phase[1] = random.randint(1, 5)

        # set pattern to start
        self.pattern_state = 1
        DEBUGGER.msg(f'pattern {self.pattern_phase} should start')

    def execute_current_pattern(self):
        """Éxecute le pattern choisi."""
        self.pattern_state += 1
        if self.pattern_phase[0] == 1:
            self.execute_pattern1()
        elif self.pattern_phase[0] == 2:
            self.execute_pattern2()
        elif self.pattern_phase[0] == 3:
            self.execute_pattern3()
        elif self.pattern_phase[0] == 4:
            self.execute_pattern4()

    def execute_pattern1(self):
        """Bouge d'un côté à l'autre, en tirant périodiquement (1.1 et 1.2)"""
        if self.pattern_phase[1] == 1 and self.x > 10:
            self.x -= 1
        elif self.pattern_phase[1] == 2 and self.x < SCREEN_WIDTH-100:
            self.x += 1
        if random.randint(0, 10) >= 9:
            self.y += 1
        if random.randint(0, 100) >= 96:
            self._pattern_fire()

    def execute_pattern2(self):
        """Déclenche une pluie de rayons lazers après avoir choisi une position (2.1, 2.2, 2.3, 2.4 et 2.5)"""
        possible_moves = ((-2, 0), (2, 0), (0, 1), (0, -1), (1, 0), (-1, 0))
        move_x, move_y = possible_moves[self.pattern_phase[1]-1]
        if self.pattern_state < 30*2-15:
            self.x += move_x
            self.y += move_y
        elif self.pattern_state < 30*2-1:
            pass # stop and then fire twice
        else:
            self._pattern_fire()

    def execute_pattern3(self):
        """Avance en tirant avec les canons normaux"""
        self.y += 1
        if self.pattern_state % 4 == 0:
            self._pattern_fire()

    def execute_pattern4(self):
        """
        Part d'un côté à l'autre en reculant et en faisant feu de toutes ses armes (4.1 et 4.2)
        Avant nivau 2, revient juste en arrière.
        """
        self.y -= 2

    def update_projectiles(self, game_speed):
        """
        mise à jour de la position des lazers
        appelée dans Game pour éviter la disparition des lazers lors de la mort du dreadnought
        """
        for lazerbeam in self.lazerbeam_list:
            lazerbeam.update_loading()
            for lazer in lazerbeam.list_lazer:
                lazer.update(game_speed)
                if lazer.y < -8 or lazer.target_hit:
                    lazerbeam.list_lazer.remove(lazer)
            if lazerbeam.state == 0 and len(lazerbeam.list_lazer) == 0:
                self.lazerbeam_list.remove(lazerbeam)
        for destlazer in self.projectiles:
            destlazer.update(game_speed)
            if destlazer.y < -8 or destlazer.target_hit:
                self.projectiles.remove(destlazer)

    def draw(self):
        """affiche le destroyer à l'écran"""
        if self.active:
            pyxel.rect(self.x, self.y+0-self.anim_reacteurs[0], 2, self.anim_reacteurs[0], 10)
            pyxel.blt(self.x-16, self.y-16, 0, 0, 24, 16*4, 16*2, colkey=0, scale=SPACESHIP_SCALE*2) # scale seem centered
        if DEBUGGER.get_var('show hitbox'):
            hbx, hby, hbw, hbh = self.hitbox
            pyxel.rectb(self.x+hbx, self.y+hby, hbw, hbh, 8)
    
    def draw_projectiles(self):
        """dessine les projectiles du dreadnought. Géré séparément dans Game pour éviter la disparition des lazers lors de la mort du dreadnought"""
        for projectile in self.projectiles:
            projectile.draw()
        for lazer in self.lazerbeam_list:
            lazer.draw()

    def _pattern_fire(self):
        """génère un tir selon le pattern actif."""
        if self.pattern_phase[0] == 1:
            for x, y in self.canon_coordinates:
                if random.randint(0, 10) >= 9:
                    self.play_the_sound.lazer()
                    self.projectiles.append(Projectile('destlazer', self.x+x*2, self.y+y*2, 3, 1))
        elif self.pattern_phase[0] == 2:
            x, y = self.lazerbeam_coordinates[random.randint(0, 3)]
            self.play_the_sound.lazebeam_load()
            self.lazerbeam_list.append(Lazerbeam('destlazer', self.x+x*2, self.y+y*2, 1))
        elif self.pattern_phase[0] == 3:
            for lazer_x, lazer_y in self.canon_coordinates:
                self.play_the_sound.lazer()
                self.projectiles.append(Projectile('destlazer', self.x+lazer_x*2, self.y+lazer_y*2, 3, 1))
            lazerbeam_x, lazerbeam_y = self.lazerbeam_coordinates[random.randint(0, 3)]
            self.play_the_sound.lazebeam_load()
            self.lazerbeam_list.append(Lazerbeam('destlazer', self.x+lazerbeam_x*2, self.y+lazerbeam_y*2, 1))
        else:
            DEBUGGER.msg('No fire for current pattern', 'WARN')

    def update_animation(self):
        """Animation des réacteurs"""
        if self.anim_reacteurs[1]:
            self.anim_reacteurs[0] += 1
            if self.anim_reacteurs[0] > 3:
                self.anim_reacteurs[1] = False
        else:
            self.anim_reacteurs[0] -= 1
            if self.anim_reacteurs[0] < 1:
                self.anim_reacteurs[1] = True

    def disactive(self):
        """détruit l'astronef"""
        self.active = False
        self.dead = False
        self.y = -64
        self.x = -100
        self.health = 0
