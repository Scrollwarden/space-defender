#!/usr/bin/python3

'''
permet de jouer à un jeu style arcade retro-gaming
Auteurs : Matthew Batt
création : 05/04/2024
dernière modification : 17/06/2024
'''

# =========================================================
# == IMPORTS
# =========================================================

import pyxel
import random
import time

# =========================================================
# == GLOBALS
# =========================================================

from constant import SCREEN_HEIGHT, SCREEN_WIDTH
# taille de la fenetre
pyxel.init(SCREEN_HEIGHT, SCREEN_WIDTH, title="Space Defender I")

# =========================================================
 # == FUNCTIONS
# =========================================================

#from intro import update, draw
from run import update, draw

# =========================================================
# == RUN
# =========================================================

time.sleep(8)
pyxel.run(update, draw)
