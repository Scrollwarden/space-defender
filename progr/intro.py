"""
Le fichier qui contiens l'écran d'accueil du jeu et les écrans de lancement

CLASSES
- MainsScreen
"""

import pyxel
from sounds import Musicien
from constants import *
# imports pour les animations
from background import StarField
from enemies import Drone
import random

DEBUGGER.set_filename('intro.py')


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
        self.play_the_sound = Musicien()

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
            self._draw_space()
        elif self.step <= 66:
            self._draw_defender()
            if self.step == 59:
                pyxel.text(SCREEN_WIDTH//2-20*2, 200, '    Arcade 2024\nNSI pyxel Contest', 7)
        elif 70 <=self.step <= 80:
            pyxel.rect(0, 0, SCREEN_WIDTH, (SCREEN_HEIGHT//20)*(self.step-69), 0)
            pyxel.rect(0, SCREEN_HEIGHT-((SCREEN_HEIGHT//20)*(self.step-69)), SCREEN_WIDTH, (SCREEN_HEIGHT//20)*(self.step-70), 0)

    def _draw_space(self):
        """
        [méthode interne de draw]
        dessine le mot SPACE à l'écran
        """
        pyxel.text(5+self.step, 76+5*0, "  ||   |||      ||     ||||   |||||", COLOR_TITLE_SPACE)
        pyxel.text(5+self.step, 76+5*1, " |     |  |    |  |    |      |    ", COLOR_TITLE_SPACE)
        pyxel.text(5+self.step, 76+5*2, "  |    |||    ||||||   |      |||  ", COLOR_TITLE_SPACE)
        pyxel.text(5+self.step, 77+5*3, "   |   |      |    |   |      |    ", COLOR_TITLE_SPACE)
        pyxel.text(5+self.step, 77+5*4, "  |    |      |    |   |      |    ", COLOR_TITLE_SPACE)
        pyxel.text(5+self.step, 77+5*5, "||     |      |    |   ||||   |||| ", COLOR_TITLE_SPACE)

    def _draw_defender(self):
        """
        [methode interne de draw]
        dessine le mot DEFENDER à l'écran
        """
        pyxel.text(self.step-50, 116+5*0, "||     |||||   |||||   |||||   |    |   ||     |||||   |||   ", COLOR_TITLE_DEFENDER)
        pyxel.text(self.step-50, 116+5*1, "| |    |       |       |       ||   |   | |    |       |  |  ", COLOR_TITLE_DEFENDER)
        pyxel.text(self.step-50, 116+5*2, "|  |   |||     |||     |||     | |  |   |  |   |||     |||   ", COLOR_TITLE_DEFENDER)
        pyxel.text(self.step-50, 117+5*3, "|  |   |       |       |       |  | |   |  |   |       |  |  ", COLOR_TITLE_DEFENDER)
        pyxel.text(self.step-50, 117+5*4, "| |    |       |       |       |   ||   | |    |       |  |  ", COLOR_TITLE_DEFENDER)
        pyxel.text(self.step-50, 117+5*5, "||     ||||    |       ||||    |    |   ||     ||||    |  |  ", COLOR_TITLE_DEFENDER)
    
    def update(self):
        """met à jour l'écran de lancement"""
        if pyxel.frame_count % 4 == 0:
            self.progress += 1
            if self.step <= 80:
                self.step += 1
        if self.progress == 20:
            self.play_the_sound.launching()


class MainScreen:
    '''
    Contrôleur : Écran d'accueil du jeu

    ATTRIBUTES

    METHODS
    - update
    - draw
    '''
    def __init__(self):
        self.background = StarField()
        self.background_entites = []

        DEBUGGER.msg('Menu screen displayed.', note='INFO')

    def update(self):
        self._update_background_anim()

    def draw(self):
        pyxel.cls(0)
        self.background.draw()
        for entity in self.background_entites:
            entity.draw()
        pyxel.rect(70, 30, SCREEN_WIDTH-70*2, SCREEN_HEIGHT-30*2, 0)
        pyxel.rectb(70, 30, SCREEN_WIDTH-70*2, SCREEN_HEIGHT-30*2, 10)
        self._draw_title()
        self._draw_buttons()
        self._draw_leaderboard_preview()
        self._draw_not_functional()

    def _draw_not_functional(self):
        """METHODE EPHEMERE : affiche un message d'erreur lors de l'utilisation d'un selecteur non implémenté"""
        if pyxel.btn(pyxel.KEY_L) or pyxel.btn(pyxel.KEY_T):
            pyxel.rect(100, 100, 100, 20, 0)
            pyxel.rectb(100, 100, 100, 20, 15)
            pyxel.text(105, 105, "OPTION INDISPONIBLE", 15)

    def _update_background_anim(self):
        """Animation en fond."""
        self.background.update()
        self._create_background_entities()
        for entity in self.background_entites:
            entity.update(1, 0)

    def _create_background_entities(self):
        """Mise à jour des entités en fond."""
        if pyxel.frame_count % 120 == 0:
            for _ in range(random.randint(1, 3)):
                x, y = (random.randint(0, SCREEN_WIDTH), -10)
                self.background_entites.append(Drone(x + random.randint(-10, 10), y + random.randint(-15, 15)))

    def _draw_title(self):
        """dessine le titre du jeu"""
        pyxel.load(LOGO_GAME)
        pyxel.blt(SCREEN_WIDTH//2-(16*2.5), SCREEN_HEIGHT//4-27, 0, 0, 0, 16*5, 16*2, scale=1)

    def _draw_buttons(self):
        """dessine les boutons"""
        mid_w = SCREEN_WIDTH//2
        mid_h = SCREEN_HEIGHT//4 +20
        i = 0
        for text, c in (('> TUTORIAL (T)', 11), ('> PLAY GAME (P)', 10), ('> SHOW LEADERBOARD (L)', 9), ('> QUIT GAME (Q)', 8)):
            pyxel.text(mid_w-(len(text)*2), mid_h+i, text, c)
            i += 10

    def _draw_leaderboard_preview(self):
        """dessine un aperçu du leaderboard"""
        pyxel.rect(74, 30*5, SCREEN_WIDTH-74*2, 60, 0)
        pyxel.rectb(74, 30*5, SCREEN_WIDTH-74*2, 60, 3)
        pyxel.text(78, 30*5 +5, 'LEADERBOARD (unfunctionnal)', 3)
        i = 1
        for player, score in (('Matthew #3', 1300), ('Matthew #2', 473), ('Matthew #1', 462)):
            pyxel.text(78, 30*5 +10+(i*8), f'{i}. {player} : {score}', 7)
            i += 1
