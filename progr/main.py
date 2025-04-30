"""
Space Defender
==============
Jeu de type space shooter
Créé : 5/10/2024
Auteur : Matthew Batt
version : develop 2.1.2

Ce fichier permet de lancer le programme.
"""

import pyxel
from run import Game
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, DEBUGGER

if __name__ == "__main__":
    # debug side launching
    DEBUGGER.toggle(True)
    DEBUGGER.set_var('show hitbox', False)
    DEBUGGER.set_var('debug_boss', True)

    # game launching
    pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Space Defender", fps=30)
    pyxel.fullscreen(True)
    game = Game()
    pyxel.run(game.update, game.draw)
