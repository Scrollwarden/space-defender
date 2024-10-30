import pyxel
import random
from constants import SCREEN_WIDTH

class _Star:
    '''
    Entity : une étoile du background

    cette classe est interne à StarField.
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, game_speed):
        self.y += 0.5 * game_speed

    def draw(self):
        pyxel.rect(self.x, self.y, 1, 1, 7)

class StarField:
    '''
    Entity : Le background du jeu composé d'étoiles

    METHODS
    - update(game_speed)
    - draw()
    '''
    def __init__(self):
        self.stars = []
        self._generate_stars_base()

    def _generate_stars_base(self):
        """generate first stars taht fill all the background"""
        for y in range(1, 256):
            if random.randint(0, 10) < 6:
                self.stars.append(_Star(random.randint(0, SCREEN_WIDTH), y))

    def update(self, game_speed=1):
        self._generate_new_stars()
        self._update_stars(game_speed)

    def draw(self):
        for star in self.stars:
            star.draw()

    def _generate_new_stars(self):
        """generate new stars at the top of the screen"""
        if (pyxel.frame_count % 15 == 0):
            for _ in range(3):#random.randint(6, 10)):
                self.stars.append(_Star(random.randint(0, SCREEN_WIDTH), 0))

    def _update_stars(self, game_speed):
        """
        [methode interne de update]
        met à jour les étoiles en fond
        """
        for star in self.stars:
            star.update(game_speed)
            if star.y > 256:
                self.stars.remove(star)