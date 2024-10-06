"""
Les différentes classes d'ennemis.

CLASSES
- Drone (Entity)
- Destroyer (Entity)

- SpieDrone (Entity) devlopment 1.1
- Turret (Entity) devlopment 1.2
- Crusader (Entity) devlopment 1.5
"""

import pyxel
from projectile import Projectile
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

    def update(self, game_speed):
        """Met à jour le Drone"""
        self.y += 1 * game_speed
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
        self.shoot_state = 0
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
            if score >= 300:
                # niveau 3 : le destroyer tire plus souvent
                fire_rate += 10
            if random.randint(0, 1000) <= fire_rate:
                self.fire()

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
            pyxel.rect(self.x, self.y-4-self.anim_reacteurs[0], 2, 3+self.anim_reacteurs[0 ], 10) # réacteur de poupe central
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
        if fire_all or self.shoot_state == 0: # doesn't work
            self.projectiles.append(Projectile('destlazer', self.x-3, self.y+10, 3, 1))
            self.shoot_state = 1
        if fire_all or self.shoot_state == 1:
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