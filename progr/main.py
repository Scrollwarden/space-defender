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