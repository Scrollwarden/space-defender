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
from sounds import play_sound
from projectile import Projectile, Lazerbeam
from constants import *
import random

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
        self.hitbox = (0, 0, 8, 8) # x, x+w, y, y+h

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
        pyxel.rect(self.x, self.y, 8, 8, 13) # armature
        pyxel.tri(self.x+1, self.y+8, self.x+6, self.y+8, self.x+4, self.y+4, 0) # trou arrière pour les ailes
        pyxel.tri(self.x+1, self.y, self.x+6, self.y, self.x+4, self.y+4, 0) # trou avant pour les ailes
        pyxel.rect(self.x+4, self.y-self.anim_reacteurs[0], 1, 2+self.anim_reacteurs[0], 10) # réacteur de poupe central
        
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
        self.y = -10
        self.active = False
        self.health = DESTROYER_LIFE
        self.dead = False
        self.projectiles = []
        self.shoot_state = 1
        self.hitbox = (-6, -4, 14, 8) # x, y, w, h
        self.anim_reacteurs = [0, True]

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

            #self.update_projectiles(game_speed)

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
            pyxel.rect(self.x-1, self.y-5-self.anim_reacteurs[0], 3, 2+self.anim_reacteurs[0], 10) # réacteur de poupe central
            pyxel.rect(self.x-6, self.y, 12, 2, 13) # barre de soutien des ailes
            pyxel.circ(self.x, self.y, 4, 13) # armature
            pyxel.rect(self.x-6, self.y-4, 2, 8, 13) # aile babord
            pyxel.rect(self.x+6, self.y-4, 2, 8, 13) # aile tribord
            # barre de vie
            if self.health != DESTROYER_LIFE:
                pyxel.rect(self.x-(self.health//2), self.y+10, self.health, 1, 3)
    
    def draw_projectiles(self):
        """dessine les projectiles du destroyer. Géré séparément dans Game pour éviter la disparition des lazers lors de la mort du destroyer"""
        for projectile in self.projectiles:
            projectile.draw()

    def fire(self):
        """génère un tir du destroyer"""
        fire_all = (random.randint(0, 6) == 6)
        if fire_all or self.shoot_state == 0:
            play_sound(SOUND_SHOOT)
            self.projectiles.append(Projectile('destlazer', self.x-3, self.y+10, 3, 1))
            self.shoot_state = 1
        elif fire_all or self.shoot_state == 1:
            play_sound(SOUND_SHOOT)
            self.projectiles.append(Projectile('destlazer', self.x+3, self.y+10, 3, 1))
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
        """détruit le destroyer"""
        self.active = False
        self.dead = False
        self.y = -10
        self.health = DESTROYER_LIFE


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
        self.hitbox = (-6, -4, 14, 8) # x, y, w, h
        self.lazerbeam_list = []

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
            pyxel.rect(self.x-1, self.y-5-self.anim_reacteurs[0], 3, 2+self.anim_reacteurs[0], 10) # réacteur de poupe central
            pyxel.tri(self.x-6, self.y, self.x+6, self.y, self.x, self.y+9, 13) # armature de proue
            pyxel.tri(self.x-6, self.y-1, self.x+6, self.y-1, self.x, self.y-7, 13) # armature de poupe
            # barre de vie
            if self.health != CRUISER_HEALTH:
                pyxel.rect(self.x-(self.health//2), self.y+10, self.health, 1, 3)

            for lazerbeam in self.lazerbeam_list:
                lazerbeam.draw()

    def fire(self):
        """fait tirer un rayon lazer au croiseur"""
        self.lazerbeam_list.append(Lazerbeam('destlazer', self.x, self.y+10, 1))
        play_sound(SOUND_LASERBEAM_LOAD)
        # if random.randint(0, 100) == 50:
        #    self.lazerbeam_list.append(Lazerbeam('destlazer', self.x, self.y, 1))
        # else:
        #    super().fire()

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
        for destlazer in self.projectiles:
            destlazer.update(game_speed)
        
    def create(self):
        self.x = random.randint(GAME_SCREEN_WIDTH_START+16, SCREEN_WIDTH-16)
        self.y = random.randint(-15, -5)
        self.health = CRUISER_HEALTH
        self.active = True

    def disactive(self):
        """détruit le croiseur"""
        self.active = False
        self.dead = False
        self.y = -10
        self.health = CRUISER_HEALTH


class Spidrone(Drone):
    pass


class Frigat:
    pass


class Dreadnought:
    pass