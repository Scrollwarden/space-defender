"""
les classes liées à des fonctionnalités du joueur

CLASSES
- Shield
- Detector
"""

import pyxel
from constants import *

class Shield:
    '''
    Entity : bouclier absorbant qui évite une partie des dégâts au joueur

    ATTRIBUTS
    - active : booléen indiquant si le bouclier est actif
    - power : puissance du bouclier
    - duration : durée restante du bouclier
    - waiter : temps de recharge du bouclier

    METHODS
    - update
    - activate
    - draw
    '''
    def __init__(self):
        self.active = False
        self.power = 0
        self.duration = 0
        self.waiter = 0

    def update(self):
        """mise à jour de tous les paramètres du bouclier"""
        if pyxel.btnr(pyxel.KEY_B) and self.waiter == 0:
            self.activate()
        
        if (pyxel.frame_count % 30 == 0) and self.active:
            self.duration -= 1
            if self.duration <= 0:
                self.power -= 1
        if self.power <= 0:
            self.active = False

        if (pyxel.frame_count % 30 == 0) and self.waiter > 0:
            self.waiter -= 1

    def activate(self):
        """active le bouclier"""
        self.active = True
        self.power = SHIELD_POWER
        self.duration = SHIELD_DURATION
        self.waiter = SHIELD_RELOAD

    def draw(self, x, y):
        """dessine le bouclier en (x, y)"""
        if self.active: # faut le redessiner, il est moche là
            pyxel.rect(x+16, y-5, 2*self.power, 1, 12)
            pyxel.dither(0.5)
            pyxel.rect(x+16, y-3, self.duration, 1, 13)

            pyxel.dither(0.3)
            pyxel.circb(x, y, 11, 12)
            pyxel.circb(x, y, 10, 12)
            pyxel.dither(0.6)
            pyxel.circb(x, y, 12, 12)
            pyxel.dither(1)
    
    def draw_shield_ui(self):
        state = 'READY'
        if self.waiter > 0:
           state = self.waiter
        pyxel.text(SCREEN_WIDTH//2, SCREEN_HEIGHT-12, f'Bouclier (B) : {state}', 10)
        

class Detector:
    '''
    Entity : détecteur de danger qui encadre tous les ennemis, repère les tirs en approche et aide à la visée

    ATTRIBUTS
    - active : booléen vérifiant que le détecteur est actif
    - duration : durée restante du détecteur avant qu'il ne se coupe
    '''
    def __init__(self):
        self.active = False
        self.duration = MAX_DETECTOR_DURATION

    def update(self):
        """met à jour le détecteur"""
        if pyxel.btnr(pyxel.KEY_D):
            self.active = not self.active

        if (pyxel.frame_count % 30 == 0):
            if self.active and self.duration > 0:
                self.duration -= 1
                if self.duration == 0:
                    self.active = False
            elif not self.active and self.duration < MAX_DETECTOR_DURATION:
                self.duration += 2

    def draw(self):
        pass

    def draw_detector_ui(self):
        """
        Dessine les informations qu'affiche le détecteur.
        
        /!\ ne dessine pas la plage de dangers sur l'écran, c'est le jeu qui le fait
        """
        if self.active:
            pyxel.text(4, 18, 'DETECTOR [ACTIVE]', 11)
        
        state = 'OUT'
        if self.duration < MAX_DETECTOR_DURATION:
           state = self.duration
        pyxel.text(SCREEN_WIDTH//2, SCREEN_HEIGHT-6, f'Detector (D) : {state}', 10)