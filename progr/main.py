"""
Space Defender
==============
Jeu de type space shooter
Créé : 5/10/2024
Auteur : Matthew batt

Ce fichier permet de lancer le programme.
"""

import pyxel
from run import Game
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

if __name__ == "__main__":
    game = Game()
    pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Space Defender")
    pyxel.fullscreen(True)
    pyxel.run(game.update, game.draw)


# TODO
# - Dev branch on Github
# - Rocket sound
# - sounds are to loud compared to musics
# - can't go over level 4
# - bakspace anytime during game