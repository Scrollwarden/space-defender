"""
l'écran d'accueil du jeu et l'introduction avant le lancement du jeu
"""

# =========================================================
# == IMPORTS
# =========================================================

import pyxel
import random

# =========================================================
# == GLOBALS
# =========================================================

from constant import SCREEN_HEIGHT, SCREEN_WIDTH, BASE_LIFE, TIME_NPC_SPEAK

# salle a affcicher
room = 1

# animation de la porte
gate_open = 0

# initialisation de l'état des dialogues
dialogue_stat = 0

# animations de discussion
lips_anim = 0
time_speak = TIME_NPC_SPEAK

# initialisation des dialogues
dialogue_yissa_1 = ("INSTRUCTOR YISSA\n\nHello newby. We don't have much time, look at the screen.\n\n1. (next)",
    "INSTRUCTOR YISSA\n\nThis is a drone. It contain an explosive charge and go in only one defined trajectory.\nMillions are reaching our base at this time.\n\n1. (next)",
    "INSTRUCTOR YISSA\n\nThis one is a drone destroyer. It do not contain explosive charge but shot lasers randomly.\nThese things are difficult to destroy.\n\n1. (next)",
    "INSTRUCTOR YISSA\n\nWe need you to go facing them and destroying as many as possible.\nIf more than {} reach our base, we wont manage to resist.\nWe are communicating to you our life point, the green bar at the top of your screen.\n\n1. (next)".format(BASE_LIFE),
    "INSTRUCTOR YISSA\n\nNow follow me, we have to check about the spaceship controls.\n\n1. *Follow here*")

dialogue_daran = ("CAPITAIN DARAN\n\nOur base is under attack ! Drone raid !\nYou, you are new here ?\n\n1. Yes, I need to learn how the spaceship work.\n2. I'm able to move this pile of scrap, open the gate !",
    "CAPITAIN DARAN\n\nWell, go to the trainning room at your right !\nYissa will take care of it.\n\n1. *Go to the trainning room*",
    "CAPITAIN DARAN\n\nI open it, and then you go. No time to waste !\n\n1. *Go to the spaceship*\n2. Wait, actually I potentially need some reminders...")

# initialisation de l'écran pyxel
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, "test intro")

# chargement des ressources de l'éditeur
pyxel.load("PYXEL_RESSOURCE_FILE.pyxres")

# =========================================================
# == FUNCTIONS
# =========================================================

def print_logo():
    """affiche les logos de début de jeu"""
    pyxel.text((SCREEN_WIDTH//2)-20, SCREEN_HEIGHT//2, 'SPACE DEFENDER', 7)

def draw_dialogue(dialogue, nb_dialogue):
    """affiche les dialogues"""
    pyxel.rect(0, 15*8, SCREEN_WIDTH, SCREEN_HEIGHT - 15*8, 7)
    pyxel.text(10, 15*8 + 10, dialogue[nb_dialogue], 0)

def update_lips_anim(state, time):
    """change la bouche du personnage qui parle"""
    if (pyxel.frame_count % 4 == 0) and time >= 0:
        state = random.randint(0, 2)
        time -= 1
    elif time < 0:
        state = 0
    return state, time

def draw_room1(speak):
    """la salle dans laquelle le joueur se trouve au début du jeu"""
    pyxel.cls(13)
    pyxel.bltm(0, 0, 0, 0, 0, SCREEN_WIDTH, 15*8)
    pyxel.blt(8*8, 7*8, 0, 5*8, speak*8, 2*8, 8)
    if gate_open >= 1:
        pyxel.blt(17*8, 7*8, 0, 5*8, 3*8, 4*8, 8)
        pyxel.blt(17*8, 6*8, 0, 3*8, 9*8, 4*8, 8)
    if gate_open >= 2:
        pyxel.blt(17*8, 6*8, 0, 5*8, 3*8, 4*8, 8)
        pyxel.blt(17*8, 5*8, 0, 3*8, 9*8, 4*8, 8)
    if gate_open >= 3:
        pyxel.blt(17*8, 5*8, 0, 5*8, 4*8, 4*8, 8)
        pyxel.blt(17*8, 4*8, 0, 5*8, 5*8, 4*8, 8)

def room1_open_gate(dialogue_stat, gate_open):
    """ouvre progressivement la porte de la salle 1 qui mène au vaisseau"""
    if (pyxel.frame_count % 10 == 0) and dialogue_stat == 2:
        if gate_open < 3:
            gate_open += 1
    return gate_open

def draw_room2():
    """la salle dans laquelle le joueur est amené s'il veut apprendre les contrôles du jeu"""

def room2_change_board():
    """change le tableau affiché dans la salle 2"""

def draw_room3():
    """l'intérieur du vaisseau quand le joueur apprend les contrôles"""

def dialogue_captain(nb_dialogue, time_speak):
    """gère les dialogues du capitaine"""
    if pyxel.btnr(pyxel.KEY_1):
        if nb_dialogue == 0:
            nb_dialogue = 1
            time_speak = TIME_NPC_SPEAK
        elif nb_dialogue == 1:
            #room = 2
            pass
        elif nb_dialogue == 2:
            #launch game
            pass
    elif pyxel.btnr(pyxel.KEY_2):
        if nb_dialogue == 0:
            nb_dialogue = 2
            time_speak = TIME_NPC_SPEAK
        elif nb_dialogue == 2:
            nb_dialogue = 1
            time_speak = TIME_NPC_SPEAK

    return nb_dialogue, time_speak

def draw_instructor():
    """l'instructeur qui explique les contrôles (salles 2 et 3)"""

def dialogue_instructor():
    """gère les dialogues de l'instructeur"""

# =========================================================
# == UPDATE
# =========================================================

def update():
    """nothing inside"""
    global lips_anim, time_speak, gate_open
    global dialogue_daran, dialogue_yissa_1, dialogue_stat
    
    # update d'animation de parole
    lips_anim, time_speak = update_lips_anim(lips_anim, time_speak)
    
    # update des dialogues
    dialogue_stat, time_speak = dialogue_captain(dialogue_stat, time_speak)

    # update de la porte room 1
    gate_open = room1_open_gate(dialogue_stat, gate_open)

# =========================================================
# == DRAW
# =========================================================

def draw():
    """draw the draw to test"""
    if room == 1:
        draw_room1(lips_anim)
        draw_dialogue(dialogue_daran, dialogue_stat)
    elif room == 2:
        draw_room2(lips_anim)
        draw_dialogue(dialogue_yissa_1, dialogue_stat)
    elif room == 3:
        draw_room3(lips_anim)
        draw_dialogue(dialogue_yissa_2, dialogue_stat)

pyxel.run(update, draw)