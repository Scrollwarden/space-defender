"""
La classe du joueur

CLASSES
- Player (Entity)
"""

import pyxel
from projectile import Projectile, Lazerbeam
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
        self.lazerbeam_list = []
        self.rocket_waiter1 = 0
        self.rocket_waiter2 = 0
        self.lazerbeam_waiter = 0
        self.booster_waiter = 0
        self.anim_reacteurs = [0, True]
        self.hitbox = (-8, -8, 10, 10) # x, y, w, h

    def update(self, game_speed, vies, score):
        """met à jour tous les paramètres du vaisseau"""
        self.move(game_speed)
        self.fire(score)
        if score >= SCORE_DESTROYER-25:
            self.shield.update()
        if score >= SCORE_SPIDRONE-25:
            self.detector.update()
        self.update_projectiles(game_speed)
        self.update_animation()
        
    def draw(self, score):
        # sous le corps de l'astronef
        if score >= SCORE_LAZERBEAM:
            pyxel.rect(self.x+8, self.y-2, 5, 8, 13) # support de pointe du canon lazer
            pyxel.tri(self.x+8, self.y-2, self.x+12, self.y-2, self.x+10, self.y-5, 13) # pointe du canon lazer
            color_chargeur = 8
            if self.lazerbeam_waiter != 0:
                color_chargeur = 1
                if self.lazerbeam_waiter <= 15:
                    color_chargeur = 15-self.lazerbeam_waiter
            pyxel.rect(self.x+10, self.y-1, 1, 4, color_chargeur) # chargeur du canon lazer

        # astronef
        pyxel.rect(self.x-4, self.y+7, 3, 3+self.anim_reacteurs[0], 6) # réacteur de poupe babord
        pyxel.rect(self.x+2, self.y+7, 3, 3+self.anim_reacteurs[0], 6) # réacteur de poupe tribord
        pyxel.circ(self.x, self.y, 8, 7) # armature
        pyxel.circ(self.x+5, self.y, 2, 6) # cokpit
        pyxel.circb(self.x+5, self.y, 3, 13) # jointure cokpit
        pyxel.tri(self.x-4, self.y+6, self.x+3, self.y+6, self.x, self.y, 2) # triange coloré de poupe
        pyxel.rect(self.x, self.y-9, 1, 4, 13) # canon de proue
        # upgrade
        if score >= SCORE_DOUBLE_TIR:
            pyxel.rect(self.x+4, self.y-9, 1, 4, 13) # 2e canon de proue
        if score >= SCORE_TRIPLE_TIR:
            pyxel.rect(self.x+8, self.y-7, 1, 5, 13) # 3e canon de proue
        if score >= SCORE_ROCKET:
            pyxel.rect(self.x-6, self.y-8, 4, 10, 13) # tube lance-roquettes 1
            pyxel.rect(self.x-5, self.y-4, 1, 5, 10-self.rocket_waiter1) # chargeur tube 1
        if score >= SCORE_DOUBLE_ROCKET:
            pyxel.rect(self.x-10, self.y-4, 4, 10, 13) # tube lance-roquettes 2
            pyxel.rect(self.x-9, self.y, 1, 5, 10-self.rocket_waiter2) # chargeur tube 2
        if score >= SCORE_BOOSTER:
            pass
        if score >= SCORE_LOCKER:
            pass
        
        if score >= SCORE_DESTROYER-25:
            self.shield.draw(self.x, self.y) # Bouclier
        if score >= SCORE_SPIDRONE-25:
            self.detector.draw() # Détecteur

        for lazer in self.lazer_liste:
            lazer.draw()
        for rocket in self.rockets_list:
            rocket.draw()
        for lazerbeam in self.lazerbeam_list:
            lazerbeam.draw()

    def move(self, game_speed):
        booster = 1
        if pyxel.btnr(pyxel.KEY_EXCLAIM) and self.booster_waiter == 0:
            booster = 4
            self.booster_waiter = BOOSTER_RELOAD
        if pyxel.btn(pyxel.KEY_RIGHT) and self.x < SCREEN_WIDTH - self.hitbox[2]:
            self.x += PLAYER_SPEED * game_speed * booster
        if pyxel.btn(pyxel.KEY_LEFT) and self.x > GAME_SCREEN_WIDTH_START +- self.hitbox[0]:
            self.x -= PLAYER_SPEED * game_speed * booster
        if pyxel.btn(pyxel.KEY_DOWN) and self.y < GAME_SCREEN_HEIGHT - self.hitbox[3]:
            self.y += PLAYER_SPEED * game_speed * booster
        if pyxel.btn(pyxel.KEY_UP) and self.y > 0 - self.hitbox[1]:
            self.y -= PLAYER_SPEED * game_speed * booster

    def fire(self, score):
        """fait tirer le vaisseau, lazer, rockets, lazerbeam"""
        # lazer
        if pyxel.btnr(pyxel.KEY_SPACE):
            self.lazer_liste.append(Projectile('lazer', self.x, self.y-10, 4, -1))
            if score >= SCORE_DOUBLE_TIR:
                self.lazer_liste.append(Projectile('lazer', self.x+4, self.y-10, 4, -1))
            if score >= SCORE_TRIPLE_TIR:
                self.lazer_liste.append(Projectile('lazer', self.x+8, self.y-10, 4, -1))
        # rockets
        if pyxel.btnr(pyxel.KEY_R):
            if not self.rocket_waiter1 == 0 and self.rocket_waiter2 == 0 and score >= SCORE_DOUBLE_ROCKET:
                self.rockets_list.append(Projectile('rocket', self.x-10, self.y-10, 3, -1))
                self.rocket_waiter2 = ROCKET_RELOAD
            if self.rocket_waiter1 == 0 and score >= SCORE_ROCKET:
                self.rockets_list.append(Projectile('rocket', self.x-6, self.y-14, 3, -1))
                self.rocket_waiter1 = ROCKET_RELOAD
        # lazerbram
        if pyxel.btnr(pyxel.KEY_F) and score >= SCORE_LAZERBEAM:
            if self.lazerbeam_waiter == 0:
                self.lazerbeam_list.append(Lazerbeam('lazer', self.x+10, self.y-5, -1))
                self.lazerbeam_waiter = LAZERBEAM_RELOAD

    def update_projectiles(self, game_speed):
        for lazer in self.lazer_liste:
            lazer.update(game_speed)
            if lazer.y < -8 or lazer.target_hit:
                self.lazer_liste.remove(lazer)
        for rocket in self.rockets_list:
            rocket.update(game_speed)
            if rocket.y < -8: # la vérification target_hit à lieu dans Game pour pouvoir ajouter l'explosion
                self.rockets_list.remove(rocket)
        for lazerbeam in self.lazerbeam_list:
            lazerbeam.update_loading()
            for lazer in lazerbeam.list_lazer:
                lazer.update(game_speed)
                if lazer.y < -8 or lazer.target_hit:
                    lazerbeam.list_lazer.remove(lazer)
            if lazerbeam.state == 0 and len(lazerbeam.list_lazer) == 0:
                self.lazerbeam_list.remove(lazerbeam)

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
        
        if (pyxel.frame_count % 30 == 0) and self.lazerbeam_waiter > 0:
            self.lazerbeam_waiter -= 1