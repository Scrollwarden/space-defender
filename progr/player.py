"""
La classe du joueur

CLASSES
- Player (Entity)
"""

import pyxel
from projectile import Projectile
from gadgets import Shield, Detector
from constants import *

class Player:
    '''
    Boundary : le vaisseau contrôlé par le joueur

    ATTRIBUTS
    - x : la position x du vaisseau
    - y : la position y du vaisseau
    - shield : le bouclier du vaisseau
    - detector : le détecteur du vaisseau
    - lazer_liste : la liste des lasers tirés par le vaisseau
    - rockets_list : la liste des roquettes tirées par le vaisseau
    - rocket_waiter : le temps d'attente entre chaque tir de roquette
    - anim_reacteurs : liste contenant l'état de l'animation des réacteurs et le sens de l'animation
    - hitbox : la hitbox du vaisseau (x, y, w, h) immuable
    '''
    def __init__(self):
        self.x = START_POSITION_X
        self.y = START_POSITION_Y
        self.shield = Shield()
        self.detector = Detector()
        self.lazer_liste = []
        self.rockets_list = []
        self.rocket_waiter1 = 0
        self.rocket_waiter2 = 0
        self.anim_reacteurs = [0, True]
        self.hitbox = (-8, -8, 10, 10) # x, y, w, h

    def update(self, game_speed, vies, score):
        self.move(game_speed)
        self.fire(score)
        if score >= SCORE_DESTROYER-25:
            self.shield.update()
        if score >= SCORE_SPIDRONE-25:
            self.detector.update()
        self.update_projectiles(game_speed)
        self.update_animation()

        # pour éviter les collisions fantomes sur les écrans de mort
        if vies < -2000:
            self.y = -100

    def draw(self, score):
        pyxel.rect(self.x-4, self.y+7, 3, 3+self.anim_reacteurs[0], 6) # réacteur de poupe babord
        pyxel.rect(self.x+2, self.y+7, 3, 3+self.anim_reacteurs[0], 6) # réacteur de poupe tribord
        pyxel.circ(self.x, self.y, 8, 7) # armature
        pyxel.tri(self.x-4, self.y+6, self.x+3, self.y+6, self.x, self.y, 2) # détail
        pyxel.rect(self.x, self.y-9, 1, 4, 13) # canon de proue
        # upgrade
        if score >= 100:
            pyxel.rect(self.x-6, self.y-8, 4, 10, 13) # [upgrade](niv1) tube lance-roquettes
            pyxel.rect(self.x-5, self.y-4, 1, 5, 10-self.rocket_waiter1) # chargeur tube 1
        if score >= 200:
            pyxel.rect(self.x+4, self.y-9, 1, 4, 13) # [upgrade](niv2) 2e canon de proue
        if score >= 300:
            pyxel.rect(self.x-10, self.y-4, 4, 10, 13) # [upgrade](niv3) 2e tube lance-roquettes
            pyxel.rect(self.x-9, self.y, 1, 5, 10-self.rocket_waiter2) # chargeur tube 2
        if score >= 400:
            pyxel.rect(self.x+8, self.y-7, 1, 5, 13) # [upgrade](niv4) 3e canon de proue
        
        if score >= SCORE_DESTROYER-25:
            self.shield.draw(self.x, self.y) # [upgrade](75% niv1) Bouclier
        if score >= SCORE_SPIDRONE-25:
            self.detector.draw() # [upgrade](75% niv3) Détecteur

        for lazer in self.lazer_liste:
            lazer.draw()
        for rocket in self.rockets_list:
            rocket.draw()

    def move(self, game_speed):
        if pyxel.btn(pyxel.KEY_RIGHT) and self.x < SCREEN_WIDTH - self.hitbox[2]:
            self.x += PLAYER_SPEED * game_speed
        if pyxel.btn(pyxel.KEY_LEFT) and self.x > GAME_SCREEN_WIDTH_START +- self.hitbox[0]:
            self.x -= PLAYER_SPEED * game_speed
        if pyxel.btn(pyxel.KEY_DOWN) and self.y < GAME_SCREEN_HEIGHT - self.hitbox[3]:
            self.y += PLAYER_SPEED * game_speed
        if pyxel.btn(pyxel.KEY_UP) and self.y > 0 - self.hitbox[1]:
            self.y -= PLAYER_SPEED * game_speed

    def fire(self, score):
        """fait tirer le vaisseau, lazer et rockets"""
        # lazer
        if pyxel.btnr(pyxel.KEY_SPACE):
            self.lazer_liste.append(Projectile('lazer', self.x, self.y-10, 4, -1))
            if score >= 200:
                self.lazer_liste.append(Projectile('lazer', self.x+4, self.y-10, 4, -1))
            if score >= 400:
                self.lazer_liste.append(Projectile('lazer', self.x+8, self.y-10, 4, -1))
        # rockets
        if pyxel.btnr(pyxel.KEY_R):
            if not self.rocket_waiter1 == 0 and self.rocket_waiter2 == 0 and score >= 300:
                self.rockets_list.append(Projectile('rocket', self.x-10, self.y-10, 3, -1))
            if self.rocket_waiter1 == 0 and score >= 100:
                self.rockets_list.append(Projectile('rocket', self.x-6, self.y-14, 3, -1))
                self.rocket_waiter1 = ROCKET_RELOAD

    def update_projectiles(self, game_speed):
        for lazer in self.lazer_liste:
            lazer.update(game_speed)
            if lazer.y < -8 or lazer.target_hit:
                self.lazer_liste.remove(lazer)
        for rocket in self.rockets_list:
            rocket.update(game_speed)
            if rocket.y < -8: # la vérification target_hit à lieu dans Game pour pouvoir ajouter l'explosion
                self.rockets_list.remove(rocket)

    def update_animation(self):
        """Animation des réacteurs et timer des rockets"""
        self.anim_reacteurs[0]
        if self.anim_reacteurs[1]:
            self.anim_reacteurs[0] += 1
            if self.anim_reacteurs[0] > 3:
                self.anim_reacteurs[1] = False
        else:
            self.anim_reacteurs[0] -= 1
            if self.anim_reacteurs[0] < 1:
                self.anim_reacteurs[1] = True

        if (pyxel.frame_count % 30 == 0) and self.rocket_waiter1 > 0:
            self.rocket_waiter1 -= 1

        if (pyxel.frame_count % 30 == 0) and self.rocket_waiter2 > 0:
            self.rocket_waiter2 -= 1