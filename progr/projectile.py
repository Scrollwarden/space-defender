'''
Les classes liées aux projectiles et à leurs effets

CLASSES
- Projectile (Entity)
- Explosion (Entity)
'''

import pyxel
from sounds import Musicien

class Projectile:
    '''
    Entity : les projectils sont les lazers, rockets et autres qui peuvent détruire des astronefs

    ATTRIBUTS
    - ptype : type de projectile (lazer, rocket, destlazer)
    - x : position x du projectile
    - y : position y du projectile
    - speed : vitesse du projectile
    - direction : direction du projectile (1 pour le bas, -1 pour le haut)
    - hitbox : hitbox du projectile (x, y, w, h) immuable
    - target_hit : si oui ou non le projectile a atteint une cible

    METHODS
    - update
    - draw
    '''
    def __init__(self, ptype, x, y, speed, direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.ptype = ptype
        self.hitbox = (0, 0, 1, 2) # x, y, w, h
        if self.ptype == 'rocket':
            self.hitbox = (0, 0, 2, 8)
        self.target_hit = False

    def update(self, game_speed):
        self.y += self.speed * self.direction * game_speed
        # if self.ptype == 'rocket':
        #     play_sound(SOUND_ROCKET_FLIGHT)

    def draw(self):
        if self.ptype == 'lazer':
            pyxel.rect(self.x, self.y, 1, 4, 8)
        elif self.ptype == 'rocket':
            pyxel.rect(self.x, self.y, 2, 8, 10)
        elif self.ptype == 'destlazer':
            pyxel.rect(self.x, self.y, 1, 4, 11)

class Explosion:
    '''
    Entity : les explosions sont des effets graphiques qui peuvent ou non infliger des dégâts

    ATTRIBUTS
    - x : position x de l'explosion
    - y : position y de l'explosion
    - radius : rayon de l'explosion
    - step : l'étape de l'explosion de 0 à 5
    - color : couleur finale de l'explosion
    - etype : type d'explosion (graphic ou damage)
    - hitbox : hitbox de l'explosion (x, y, w, h) immuable

    METHODS
    - update
    - draw
    '''
    def __init__(self, x, y, color=10, radius=0, etype='graphic'):
        self.x = x
        self.y = y
        self.radius = radius
        self.step = 0
        self.color = color - 4 # or 5 ?
        self.etype = etype
        self.hitbox = (-radius, -radius, 2*radius, 2*radius) # x, x+w, y, y+h

    def update(self):
        """met à jour l'explosion"""
        if (pyxel.frame_count % 2 == 0) and self.step < 5:
            self.step += 1
            self.radius += 1
            self.hitbox = (-self.radius, -self.radius, 2*self.radius+1, 2*self.radius+1)
            self.color += 1
            if self.color > 12:
                self.color = 8

    def draw(self):
        """dessine l'explosion"""
        pyxel.circb(self.x, self.y, self.radius, self.color)
        if self.etype == 'damage':
            pyxel.circ(self.x, self.y, max(0, self.radius-3), self.color-1)


class Lazerbeam:
    '''
    Entity : rayon lazer
    Créé une file de lazers d'un type donné après un temps de chargement
    '''
    def __init__(self, ltype, x, y, direction):
        self.x = x
        self.y = y
        self.ltype = ltype
        self.direction = direction
        self.state = 12 # temps de chargement
        self.list_lazer = []
        self.play_the_sound = Musicien()

    def update_loading(self):
        """mise à jour chargement du rayon lazer"""
        self.state -= 1
        if self.state == 0:
            self.fire()

    def draw(self):
        """apparition du rayonlazer à l'écran"""
        self.draw_chargement()
        for lazer in self.list_lazer:
            lazer.draw()

    def draw_chargement(self):
        """animation de chargement du rayon"""
        color = 11
        if self.ltype == 'lazer':
            color = 8
        if self.state > 0:
            pyxel.circb(self.x, self.y, self.state, color)

    def fire(self):
        """tir du lazer"""
        self.play_the_sound.lazerbeam()
        for i in range(60):
            self.list_lazer.append(Projectile(self.ltype, self.x, self.y+(self.direction*i*2), 24, self.direction))