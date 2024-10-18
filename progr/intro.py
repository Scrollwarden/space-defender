"""
Le fichier qui contiens l'écran d'accueil du jeu et les écrans de lancement

CLASSES
- MainsScreen
"""

import pyxel
from sounds import play_sound
from constants import *

class MainScreen:
    '''
    Contrôleur : Écran d'accueil du jeu

    ATTRIBUTES

    METHODS
    - update
    - draw
    '''
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class LaunchingScreen:
    '''
    Entité : les écrans de lancement du jeu

    ATTRIBUTES
    - duration (int) : la durée totale d'affichage de cet écran
    - progress (int) : la progression de l'animation
    - step (int) : les étapes de l'affichage du titre

    METHODS
    - update
    - draw
    '''
    def __init__(self):
        self.duration = 80
        self.progress = 0
        self.step = 0

    def draw(self):
        """dessine l'écran de lancement"""
        if self.step <= 20:
            pyxel.load(LOGO_STUDIO)
            pyxel.blt((SCREEN_WIDTH//2)-8*6, (SCREEN_HEIGHT//2)-8*3, 0, 0, 0, 8*12, 8*5)
        elif self.step <= 30:
            pyxel.rect(0, 0, SCREEN_WIDTH, (SCREEN_HEIGHT//20)*(self.step-19), 0)
            pyxel.rect(0, SCREEN_HEIGHT-((SCREEN_HEIGHT//20)*(self.step-19)), SCREEN_WIDTH, (SCREEN_HEIGHT//20)*(self.step-20), 0)
        elif self.step <= 40:
            pyxel.text((SCREEN_WIDTH//2)-25*2, (SCREEN_HEIGHT//2)-20, 'DANS UN DELIRE LOINTAIN\n    TRES LOINTAIN...', 6)
        elif self.step <= 50:
            pyxel.rect(0, 0, SCREEN_WIDTH, (SCREEN_HEIGHT//20)*(self.step-39), 0)
            pyxel.rect(0, SCREEN_HEIGHT-((SCREEN_HEIGHT//20)*(self.step-39)), SCREEN_WIDTH, (SCREEN_HEIGHT//20)*(self.step-40), 0)
        elif self.step <= 58:
            pyxel.text(5+self.step, 76+5*0, "  ||   |||      ||     ||||   |||||", COLOR_TITLE_SPACE)
            pyxel.text(5+self.step, 76+5*1, " |     |  |    |  |    |      |", COLOR_TITLE_SPACE)
            pyxel.text(5+self.step, 76+5*2, "  |    |||    ||||||   |      |||", COLOR_TITLE_SPACE)
            pyxel.text(5+self.step, 77+5*3, "   |   |      |    |   |      |", COLOR_TITLE_SPACE)
            pyxel.text(5+self.step, 77+5*4, "  |    |      |    |   |      |", COLOR_TITLE_SPACE)
            pyxel.text(5+self.step, 77+5*5, "||     |      |    |   ||||   ||||", COLOR_TITLE_SPACE)
        elif self.step <= 66:
            pyxel.text(self.step-50, 116+5*0, "||     |||||   |||||   |||||   |    |   ||     |||||   |||", COLOR_TITLE_DEFENDER)
            pyxel.text(self.step-50, 116+5*1, "| |    |       |       |       ||   |   | |    |       |  |", COLOR_TITLE_DEFENDER)
            pyxel.text(self.step-50, 116+5*2, "|  |   |||     |||     |||     | |  |   |  |   |||     |||", COLOR_TITLE_DEFENDER)
            pyxel.text(self.step-50, 117+5*3, "|  |   |       |       |       |  | |   |  |   |       |  |", COLOR_TITLE_DEFENDER)
            pyxel.text(self.step-50, 117+5*4, "| |    |       |       |       |   ||   | |    |       |  |", COLOR_TITLE_DEFENDER)
            pyxel.text(self.step-50, 117+5*5, "||     ||||    |       ||||    |    |   ||     ||||    |  |", COLOR_TITLE_DEFENDER)
            if self.step == 59:
                pyxel.text(SCREEN_WIDTH//2-20*2, 200, '    Arcade 2024\nNSI pyxel Contest', 7)
        elif 70 <=self.step <= 80:
            pyxel.rect(0, 0, SCREEN_WIDTH, (SCREEN_HEIGHT//20)*(self.step-69), 0)
            pyxel.rect(0, SCREEN_HEIGHT-((SCREEN_HEIGHT//20)*(self.step-69)), SCREEN_WIDTH, (SCREEN_HEIGHT//20)*(self.step-70), 0)
    
    def update(self):
        """met à jour l'écran de lancement"""
        if pyxel.frame_count % 4 == 0:
            self.progress += 1
            if self.step <= 80:
                self.step += 1
        if self.progress == 20:
            play_sound(MUSIC_MENU1)