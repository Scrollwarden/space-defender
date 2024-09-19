"""
la boucle du jeu (lancé après l'intro)
"""

# =========================================================
# == IMPORTS
# =========================================================

import pyxel
import random

# =========================================================
# == GLOBALS
# =========================================================

from constant import *

# initialisation des table_points
table_points = {'score':0, 'tués':0, 'passés':0, 'boss tués':0, 'boss passés':0, 'dégâts boss':0}

# position initiale du vaisseau
vaisseau_x = START_POSITION_X
vaisseau_y = START_POSITION_Y

# vitesse du jeu
game_speed = GAME_SPEED

# initialisation des stimulants (working on)
stim = [False, 0, 0] # activé ou non, nombre déjà pris, niveau d'overdose
stim_effect = DURATION_STIMS

# vies
vies = PLAYER_LIFE

# initialisation des tirs
lazer_liste = []

# initialisation des rockets
rockets_list = []
rocket_waiter = 0

# initialisation des ondes de roquettes
boom_list = []

# initialisation du bouclier
shield = [0, 0]
shield_waiter = 0

# initialisation des ennemis
ennemis_liste = []

# initialisation du boss
# x, y, affichage, pv
boss = [0, 0, False, BOSS_LIFE]
boss_tirs = []

# initialisation du détecteur
detector = False
detector_duration = MAX_DETECTOR_DURATION

# animation de dégât
crash_list = []

# animations
anim_reacteurs = [0, True]

liste_etoiles = []
for y in range(1, 256):
    liste_etoiles.append([random.randint(0, 256), y])

# =========================================================
# == FUNCTIONS
# =========================================================

def vaisseau_deplacement(x, y):
    """déplacement avec les touches de directions"""
    if pyxel.btn(pyxel.KEY_RIGHT):
        if (x < 247) :
            x = x + PLAYER_SPEED * game_speed
    if pyxel.btn(pyxel.KEY_LEFT):
        if (x > 8) :
            x = x - PLAYER_SPEED * game_speed
    if pyxel.btn(pyxel.KEY_DOWN):
        if (y < 247) :
            y = y + PLAYER_SPEED * game_speed
    if pyxel.btn(pyxel.KEY_UP):
        if (y > 8) :
            y = y - PLAYER_SPEED * game_speed
    return x, y

def tirs_creation(x, y, tirs_liste, key):
    """création d'un tir avec la barre d'espace pour lazer et R pour une roquette"""
    global rocket_waiter
    # btnr pour eviter les tirs multiples
    if pyxel.btnr(key):
        if key == pyxel.KEY_R:
            if rocket_waiter == 0:
                tirs_liste.append([x-6, y-14])
                if table_points['score'] > 199:
                    tirs_liste.append([x-10, y])
                rocket_waiter = ROCKET_RELOAD
        else:
            tirs_liste.append([x, y-10])
            if table_points['score'] > 99:
                tirs_liste.append([x+4, y+(random.randint(10, 15))])
                if table_points['score'] > 299:
                    tirs_liste.append([x+8, y+(random.randint(0, 5))])
 
    return tirs_liste

def update_waiter(waiter):
    if (pyxel.frame_count % 30 == 0) and waiter != 0:
        waiter -= 1
    return waiter

def tirs_deplacement(tirs_liste, speed):
    """déplacement des tirs vers le haut et suppression s'ils sortent du cadre"""
    for tir in tirs_liste:
        tir[1] -= speed
        if  tir[1] < -8:
            tirs_liste.remove(tir)
    return tirs_liste

def bouclier_activation(shield, key):
    """Le joueur active un bouclier devant lui avec B"""
    global shield_waiter

    if pyxel.btnr(key) and shield_waiter == 0:
        shield[0] = SHIELD_POWER
        shield[1] = SHIELD_DURATION
        shield_waiter = SHIELD_RELOAD
    return shield

#def take_stim(stim):
#    """Le joueur s'ingecte un stimulant avec S et réduit la vitesse du jeu"""
#    if pyxel.btnr(pyxel.KEY_S):
#        if stim[1] <= 4:
#            stim[0] = True
#            stim[1] += 1
#
#    return stim

#def change_speed_stim(stim, stim_effect, game_speed):
#    """change la vitesse de jeu tant qu'un stim est actif"""
#    game_speed = GAME_SPEED
#    if stim[0] and stim_effect >= 0:
#        game_speed = GAME_SPEED * 0.5
#    elif stim_effect <= 0:
#        stim[0] = False
#        game_speed = end_stim(stim)
#    
#    return stim, game_speed

#def end_stim(stim):
#    """ramène le jeu a sa vitesse de base ou double la vitesse si le joueur a fait une overdose de stim"""
#    game_speed = GAME_SPEED
#    if stim[2] == 2:
#        game_speed = GAME_SPEED * 2
#    if stim[1] == 2:
#        if random.randint(0, 1) <= 0.3:
#            game_speed = GAME_SPEED * 2
#            stim[2] = 1
#    if stim[1] == 3:
#        if random.randint(0, 1) <= 0.65:
#            if stim[2]:
#                game_speed = GAME_SPEED * 4
#                stim[2] = 2
#            else:
#                game_speed = GAME_SPEED * 2
#                stim[2] = 1
#    if stim[1] == 4:
#        if stim[2]:
#            game_speed = GAME_SPEED * 4
#            stim[2] = 2
#        else:
#            game_speed = GAME_SPEED * 2
#            stim[2] = 1
#    
#    return game_speed

def ennemis_creation(ennemis_liste, boss):
    """création aléatoire des ennemis"""
    if vies > 0 and (table_points['passés'] + table_points['dégâts boss']) < BASE_LIFE:
        # un ennemi par 2 seconde
        if (pyxel.frame_count % 60 == 0):
            rand_x = random.randint(16, 233)
            rand_y = random.randint(5, 25)
            for _ in range(random.randint(1, 4)):
                ennemis_liste.append([rand_x + random.randint(-15, 15), rand_y + random.randint(-15, 15)])
            # un de plus si le niveau 100 est passé
            if table_points['score'] > 99: 
                ennemis_liste.append([random.randint(10, 247),random.randint(0, 5)])
            
            # boss
            if boss[2] == False and random.randint(0, 15) == 15:
                boss = [rand_x, rand_y-20, True, BOSS_LIFE]
    return (ennemis_liste, boss)

def ennemis_deplacement(ennemis_liste, boss):
    """déplacement des ennemis vers le bas et suppression s'ils sortent du cadre"""
    global table_points

    if vies > 0 and (table_points['passés'] + table_points['dégâts boss']) < BASE_LIFE:
        for ennemi in ennemis_liste:
            ennemi[1] += 1 * game_speed
            # plus rapide si le niveau 200 est passé
            if table_points['score'] > 199:
                ennemi[1] += 0.2
            if table_points['score'] > 299: # niveau 300
                ennemi[1] += 0.2

            # retirer le vaisseau s'il arrive au bout
            if  ennemi[1]>247:
                ennemis_liste.remove(ennemi)
                table_points['passés'] += 1
                table_points['score'] -= 1
        if boss[2] == True:
            boss[1] += 1 * game_speed
            if table_points['score'] > 299: # niveau 300
                boss[1] += 0.2
            if boss[1]>247:
                boss[2] = False
                table_points['score'] -= boss[3]
                table_points['boss passés'] += 1
                table_points['dégâts boss'] += boss[3]
    return (ennemis_liste, boss)

def boss_tirs_creation(x, y, boss_tirs):
    """création d'un tir depuis le boss"""
    global table_points

    tir_reccurence = 20
    if table_points['score'] >= 399: # niveau 400
        tir_reccurence = 30
    if random.randint(0, tir_reccurence) == 0 and boss[2] == True:
        boss_tirs.append([x-3, y+10])
        boss_tirs.append([x+3, y+10])
    return boss_tirs

def boss_tirs_deplacement(boss_tirs):
    """déplacement des tirs vers le bas et suppression s'ils sortent du cadre"""
    for tir in boss_tirs:
        tir[1] += 3 * game_speed
        if  tir[1] > 247:
            boss_tirs.remove(tir)
    return boss_tirs
    
def vaisseau_suppression(vies):
    """disparition du vaisseau et d'un ennemi si contact"""
    global table_points, shield

    for ennemi in ennemis_liste:
        if ennemi[0] <= vaisseau_x+7 and ennemi[1] <= vaisseau_y and ennemi[0]+8 >= vaisseau_x-7 and ennemi[1]+8 >= vaisseau_y-8:
            crash_list.append([ennemi[0], ennemi[1], 0, 8])
            ennemis_liste.remove(ennemi)
            table_points['tués'] += 1
            table_points['score'] += 1
            if shield[0] > 0:
                crash_list.append([vaisseau_x, vaisseau_y, 0, 11])
                shield[0] -= 1
            else:
                crash_list.append([vaisseau_x, vaisseau_y, 0, 8])
                vies -= 1
    if boss[2] == True:
        for tirs in boss_tirs:
            if tirs[0] <= vaisseau_x+7 and tirs[1] <= vaisseau_y and tirs[0]+1 >= vaisseau_x-7 and tirs[1]+3 >= vaisseau_y-8:
                boss_tirs.remove(tirs)
                if shield[0] > 0:
                    crash_list.append([vaisseau_x, vaisseau_y, 0, 11])
                    shield[0] -= 1
                else:
                    crash_list.append([vaisseau_x, vaisseau_y, 0, 8])
                    vies -= 1
        if boss[0]-8 <= vaisseau_x+7 and boss[1] <= vaisseau_y and boss[0]+8 >= vaisseau_x-7 and boss[1]+4 >= vaisseau_y-8:
            if shield[0] > 0:
                crash_list.append([vaisseau_x, vaisseau_y, 0, 11])
                shield[0] -= boss[3]
            else:
                crash_list.append([vaisseau_x, vaisseau_y, 0, 8])
                vies -= boss[3]
            crash_list.append([boss[0], boss[1], 0, 8])
            boss[2] = False
            table_points['boss tués'] += 1
            table_points['score'] += BOSS_LIFE
    return vies

def ennemis_suppression():
    """disparition d'un ennemi et d'un tir si contact"""
    global table_points

    if vies > 0 and (table_points['passés'] + table_points['dégâts boss']) < BASE_LIFE:
        for ennemi in ennemis_liste:
            for tir in lazer_liste:
                if ennemi[0] <= tir[0]+1 and ennemi[0]+8 >= tir[0] and ennemi[1]+8 >= tir[1] and ennemi[1] <= tir[1]:
                    crash_list.append([tir[0], tir[1], 0, 8])
                    lazer_liste.remove(tir)
                    crash_list.append([ennemi[0], ennemi[1], 0, 8])
                    ennemis_liste.remove(ennemi)
                    table_points['score'] += 1
                    table_points['tués'] += 1
            for zone in boom_list:
                if ennemi[0]-5 <= zone[0]+1 and ennemi[0]+8+5 >= zone[0] and ennemi[1]+8 >= zone[1] and ennemi[1] <= zone[1]:
                    crash_list.append([ennemi[0], ennemi[1], 0, 8])
                    ennemis_liste.remove(ennemi)
                    table_points['score'] += 1
                    table_points['tués'] += 1
            for tir in rockets_list:
                if ennemi[0] <= tir[0]+1 and ennemi[0]+8 >= tir[0] and ennemi[1]+8 >= tir[1] and ennemi[1] <= tir[1]:
                    boom_list.append([tir[0], tir[1], 0]) # le 3e numéro est la durée d'affichage qui fait 0 -> TAILLE_EXPLOSION
                    rockets_list.remove(tir)
                    # les ennemis ne prennent pas de dégâts, c'est l'explosion qui en donne

def boss_suppression():
    "update de la vie et disparition du boss et des tirs au contact"
    global table_points

    if vies > 0 and (table_points['passés'] + table_points['dégâts boss']) < BASE_LIFE:
        if boss[2] == True:
            for tir in lazer_liste:
                if tir[0] <= boss[0]+5 and tir[1] <= boss[1] and tir[0] >= boss[0]-5 and tir[1] >= boss[1]-8:
                    boss[3] -= 1
                    crash_list.append([tir[0], tir[1], 0, 8])
                    lazer_liste.remove(tir)
            for zone in boom_list:
                if zone[0] <= boss[0]+5 and zone[1] <= boss[1] and zone[0] >= boss[0]-5 and zone[1] >= boss[1]-8:
                    crash_list.append([boss[0], boss[1], 0, 8])
                    boss[3] -= 1
            for tir in rockets_list:
                if tir[0] <= boss[0]+5 and tir[1] <= boss[1] and tir[0] >= boss[0]-5 and tir[1] >= boss[1]-8:
                    boom_list.append([tir[0], tir[1], 0]) # le 3e numéro est la durée d'affichage qui fait 0 -> TAILLE_EXPLOSION
                    rockets_list.remove(tir)
                    # les ennemis ne prennent pas de dégâts, c'est l'explosion qui en donne
            if boss[3] <= 0:
                crash_list.append([boss[0], boss[1], 0, 8])
                boss[2] = False
                table_points['score'] += BOSS_LIFE
                table_points['boss tués'] += 1

def remove_boom(boom_list):
    """retire les explosions au bout d'un certain temps"""
    if (pyxel.frame_count % 5 == 0):
        for boom in boom_list:
            if boom[2] >= TAILLE_EXPLOSION:
                boom_list.remove(boom)
            else:
                boom[2] += 1
    return boom_list

def remove_crash(crash_list):
    """retire les crash au bout d'un certain temps"""
    if (pyxel.frame_count % 2 == 0):
        for crash in crash_list:
            if crash[2] >= 2:
                crash_list.remove(crash)
            else:
                crash[2] += 1
                crash[3] += 1

def etoile_creation(liste_etoiles):
    """affiche des étoiles aléatoirement sur la carte"""
    if (pyxel.frame_count % 15 == 0):
        for _ in range(random.randint(6, 10)):
            liste_etoiles.append([random.randint(0, 256), 0])
    return liste_etoiles

def etoile_deplacement(liste_etoiles):
    """déplace les étoiles affichées sur la carte"""
    for star in liste_etoiles:
        star[1] += 0.5 * game_speed
        if  star[1]>256:
            liste_etoiles.remove(star)
    return liste_etoiles

def toggle_detector(detector):
    """D active/désactive une aide à la visée qui encadre les ennemis dans une certaine portée et les relient à une ligne s'ils sont face à un canon"""
    if pyxel.btnr(pyxel.KEY_D):
        detector = not(detector)
    return detector

def update_detector_power(detector_duration):
    """Change la durée d'activation du détecteur"""
    global detector
    if (pyxel.frame_count % 30 == 0):
        if detector and detector_duration > 0:
            detector_duration -= 1
            if detector_duration == 0:
                detector = False
        elif not(detector) and detector_duration < MAX_DETECTOR_DURATION:
            detector_duration += 1
    return detector_duration


# =========================================================
# == UPDATE
# =========================================================

def update():
    """mise à jour des variables (30 fois par seconde)"""
    global vaisseau_x, vaisseau_y, vies, game_speed
    global detector, detector_duration, shield, stim
    global shield_waiter, rocket_waiter, stim_effect
    global lazer_liste, rockets_list, boom_list
    global ennemis_liste, boss, boss_tirs
    global anim_reacteurs, liste_etoiles, crash_list

    # mise à jour de la position du vaisseau
    vaisseau_x, vaisseau_y = vaisseau_deplacement(vaisseau_x, vaisseau_y)

    # creation des lazers et des rockets en fonction de la position du vaisseau
    lazer_liste = tirs_creation(vaisseau_x, vaisseau_y, lazer_liste, pyxel.KEY_SPACE)
    rockets_list = tirs_creation(vaisseau_x, vaisseau_y, rockets_list, pyxel.KEY_R)
    # mise a jour des positions des lazers et rockets
    lazer_liste = tirs_deplacement(lazer_liste, 4 * game_speed)
    rockets_list = tirs_deplacement(rockets_list, 3 * game_speed)

    # création du bouclier
    shield = bouclier_activation(shield, pyxel.KEY_B)

    # activation des stims (working on)
    #stim = take_stim(stim)
    #stim, game_speed = change_speed_stim(stim, stim_effect, game_speed)

    # mise à jour des compteurs
    rocket_waiter = update_waiter(rocket_waiter)
    shield_waiter = update_waiter(shield_waiter)
    stim_effect = update_waiter(stim_effect)
    
    # creation des ennemis
    ennemis_liste, boss = ennemis_creation(ennemis_liste, boss)

    # deplacement des ennemis
    ennemis_liste, boss = ennemis_deplacement(ennemis_liste, boss)

    # suppression des ennemis et tirs si contact
    ennemis_suppression()
    boss_suppression()

    # suppression des booms si temps écoulé
    remove_boom(boom_list)
    remove_crash(crash_list)

    # suppression du vaisseau et ennemi si contact
    vies = vaisseau_suppression(vies)

    # update detecteur
    detector = toggle_detector(detector)
    detector_duration = update_detector_power(detector_duration)

    # animation des étoiles
    liste_etoiles = etoile_creation(liste_etoiles)
    liste_etoiles = etoile_deplacement(liste_etoiles)

    # animation des réacteurs
    if anim_reacteurs[1] == True:
        anim_reacteurs[0] += 1
        if anim_reacteurs[0] > 3:
            anim_reacteurs[1] = False
    else:
        anim_reacteurs[0] -= 1
        if anim_reacteurs[0] < 1:
            anim_reacteurs[1] = True

# =========================================================
# == DRAW
# =========================================================

def draw_vaisseau():
    """vaisseau du joueur"""
    pyxel.rect(vaisseau_x-4, vaisseau_y+7, 3, 3+anim_reacteurs[0], 6) # réacteur de poupe babord
    pyxel.rect(vaisseau_x+2, vaisseau_y+7, 3, 3+anim_reacteurs[0], 6) # réacteur de poupe tribord
    pyxel.circ(vaisseau_x, vaisseau_y, 8, 7) # armature
    pyxel.tri(vaisseau_x-4, vaisseau_y+6, vaisseau_x+3, vaisseau_y+6, vaisseau_x, vaisseau_y, 2) # détail
    pyxel.rect(vaisseau_x, vaisseau_y-9, 1, 4, 13) # canon de proue
    pyxel.rect(vaisseau_x-6, vaisseau_y-8, 4, 10, 13) # tube lance-roquettes
    pyxel.rect(vaisseau_x-5, vaisseau_y-4, 1, 5, 10-rocket_waiter) # chargeur roquettes
    # upgrade
    if table_points['score'] > 99:
        pyxel.rect(vaisseau_x+4, vaisseau_y-9, 1, 4, 13) # [upgrade](niv1) 2e canon de proue
    if table_points['score'] > 199:
        pyxel.rect(vaisseau_x-10, vaisseau_y-4, 4, 10, 13) # [upgrade](niv2) 2e tube lance-roquettes
    if table_points['score'] > 299:
        pyxel.rect(vaisseau_x+8, vaisseau_y-7, 1, 5, 13) # [upgrade](niv3) 3e canon de proue
    # informations
    if vies != PLAYER_LIFE:
        pyxel.rect(vaisseau_x-((2*vies)//2), vaisseau_y+15, 2*vies, 1, 3) # barre de vie
    if rocket_waiter != 0:
        pyxel.text(vaisseau_x-14, vaisseau_y-4, str(rocket_waiter), 10) # compteur de chargement des roquettes
    if detector_duration != MAX_DETECTOR_DURATION:
        pyxel.rect(vaisseau_x-(detector_duration//2), vaisseau_y+17, detector_duration, 1, 11)
    # bouclier
    if shield[0] > 0 and shield[1] > 0:
        pyxel.rect(vaisseau_x-(shield[0]//2), vaisseau_y+13, shield[0], 1, 12)
        pyxel.dither(0.3)
        pyxel.circb(vaisseau_x, vaisseau_y, 9, 12)
        pyxel.circb(vaisseau_x, vaisseau_y, 8, 12)
        pyxel.dither(1)
    if shield_waiter > 0:
        pyxel.text(vaisseau_x-3, vaisseau_y+15, str(shield_waiter), 12)

def draw_detector(x, y, type_detected):
    """afficahge des infos du detecteur"""
    if detector and detector_duration > 0:
        pyxel.text(4, 18, 'DETECTOR [ACTIVE]\nenergie : ' + str(detector_duration), 11)
        if type_detected == 'ennemi':
            if vaisseau_x - 60 <= x and vaisseau_x + 60 >= x:
                color = 11
                if (pyxel.frame_count % 2 == 0) and x-4 <= vaisseau_x and x+4 >= vaisseau_x:
                    pyxel.rect(x+5, y, 5, 1, 14)
                    pyxel.rect(x, y+5, 1, 5, 14)
                    pyxel.rect(x-10, y, 5, 1, 14)
                    pyxel.rect(x, y-10, 1, 5, 14)
                    pyxel.text(4, 34, '> TARGET LOCKED', 14)
                    color = 14
                if rocket_waiter == 0 and x <= vaisseau_x and x >= vaisseau_x-10:
                    pyxel.text(4, 40, '> ROCKET READY', 14)
                    pyxel.rect(vaisseau_x-5, y, 1, vaisseau_y-y, 14)
                    for i in range(1, 4):
                        pyxel.circb(vaisseau_x-5, y-(i*2), 2*i, 14)
                    if (pyxel.frame_count % 2 == 0):
                        color = 14
                # coin haut gauche
                pyxel.rect(x-6, y-6, 3, 1, color)
                pyxel.rect(x-6, y-5, 1, 2, color)
                # coin haut droit
                pyxel.rect(x+(6-3), y-6, 3, 1, color)
                pyxel.rect(x+(6-1), y-5, 1, 2, color)
                # coin bas gauche
                pyxel.rect(x-6, y+6, 3, 1, color)
                pyxel.rect(x-6, y+4, 1, 2, color)
                # coin bas droit
                pyxel.rect(x+(6-3), y+6, 3, 1, color)
                pyxel.rect(x+(6-1), y+4, 1, 2, color)
                for tir in lazer_liste:
                    if (pyxel.frame_count % 2 == 0) and x-4 <= tir[0] and x+4 >= tir[0]:
                        pyxel.circ(x+6, y-4, 2, 4)
                for tir in rockets_list:
                    if (pyxel.frame_count % 2 == 0) and x-4 <= tir[0] and x+4 >= tir[0]:
                        pyxel.rect(x+6, y, 4, 4, 4)
        elif type_detected == 'shoot':
            if (pyxel.frame_count % 2 == 0) and x <= vaisseau_x+20 and x >= vaisseau_x-20:
                pyxel.trib(x+2, y, x+7, y, x+5, y-4, 4)
                pyxel.rect(x, y, 1, vaisseau_y-y, 4)
                pyxel.text(vaisseau_x-24, vaisseau_y-80, '      /!\\     \n   WARNING    \nSHOOT INCOMING\n      /!\\     ', 4)

def draw_gadget_info():
    pyxel.text(180, 232, 'SPACE : Lazer', 8)
    if shield_waiter == 0:
        shield_ready = 'READY'
    else:
        shield_ready = '{}'.format(shield_waiter)
    pyxel.text(180, 238, 'B : Shield ({})'.format(shield_ready), 12)
    if rocket_waiter == 0:
        rocket_ready = 'READY'
    else:
        rocket_ready = '{}'.format(rocket_waiter)
    pyxel.text(180, 244, 'R : Rocket ({})'.format(rocket_ready), 10)
    pyxel.text(180, 250, 'D : Detector ({} energie)'.format(detector_duration), 11)

def draw():
    """création des objets (30 fois par seconde)"""
    # vide la fenetre
    pyxel.cls(0)

    # étoiles
    for star in liste_etoiles:
        pyxel.rect(star[0], star[1], 1, 1, 7)
    
    # si le vaisseau possede des vies le jeu continue
    if vies > 0 and (table_points['passés'] + table_points['dégâts boss']) < BASE_LIFE:
        # tirs
        for lazer in lazer_liste:
            pyxel.rect(lazer[0], lazer[1], 1, 4, 8)
        # rocket
        for rocket in rockets_list:
            pyxel.rect(rocket[0], rocket[1], 4, 12, 10)
        # vaisseau
        draw_vaisseau()
        # tirs du boss 
        for tir in boss_tirs:
            pyxel.rect(tir[0], tir[1], 1, 4, 6)
            draw_detector(tir[0], tir[1], 'shoot')
        # ennemis
        for ennemi in ennemis_liste:
            pyxel.rect(ennemi[0], ennemi[1], 8, 8, 13) # armature
            pyxel.tri(ennemi[0]+1, ennemi[1]+8, ennemi[0]+6, ennemi[1]+8, ennemi[0]+4, ennemi[1]+4, 0) # trou arrière pour les ailes
            pyxel.tri(ennemi[0]+1, ennemi[1], ennemi[0]+6, ennemi[1], ennemi[0]+4, ennemi[1]+4, 0) # trou avant pour les ailes
            pyxel.rect(ennemi[0]+4, ennemi[1]-anim_reacteurs[0], 1, 2+anim_reacteurs[0 ], 10) # réacteur de poupe central
            draw_detector(ennemi[0]+4, ennemi[1]+4, 'ennemi')
        # boss
        if boss[2] == True:
            pyxel.rect(boss[0], boss[1]-4-anim_reacteurs[0], 2, 3+anim_reacteurs[0 ], 10) # réacteur de poupe central
            pyxel.rect(boss[0]-6, boss[1], 12, 2, 13) # barre de soutien des ailes
            pyxel.circ(boss[0], boss[1], 4, 13) # armature
            pyxel.rect(boss[0]-6, boss[1]-4, 2, 8, 13) # aile babord
            pyxel.rect(boss[0]+6, boss[1]-4, 2, 8, 13) # aile tribord
            draw_detector(boss[0], boss[1], 'ennemi')
            if boss[3] != BOSS_LIFE:
                pyxel.rect(boss[0]-((1*boss[3])//2), boss[1]+10, 1*boss[3], 1, 3) # barre de vie
        # explosions
        for boom in boom_list:
            if boom[2] < TAILLE_EXPLOSION:
                pyxel.circ(boom[0], boom[1], 2*boom[2], 10)
            else:
                pyxel.circb(boom[0], boom[1], 2*boom[2], 9)
                pyxel.circ(boom[0], boom[1], boom[2], 10)
        # crashs
        for crash in crash_list:
            pyxel.circb(crash[0], crash[1], crash[2], crash[3])
        # info gadgets
        draw_gadget_info()
        # affichage du score
        pyxel.text(2, 6, 'score : ' + str(table_points['score']), 7)
        # affichage de la vie de la base
        pyxel.rect(2, 2, 8*(BASE_LIFE - (table_points['passés'] + table_points['dégâts boss'])), 2, 11)
        pyxel.text(8*(BASE_LIFE - (table_points['passés'] + table_points['dégâts boss'])) + 4, 1, str(BASE_LIFE - (table_points['passés'] + table_points['dégâts boss'])), 11)
    # sinon: GAME OVER
    else:
        # tableau de score
        pyxel.text(2, 2, 'score : ' + str(table_points['score']), 7)
        pyxel.text(2, 9, 'chasseurs tues : ' + str(table_points['tués']), 7)
        pyxel.text(2, 16, 'destroyers tues : ' + str(table_points['boss tués']), 7)
        pyxel.text(2, 23, 'chasseurs passes : ' + str(table_points['passés']), 7)
        pyxel.text(2, 30, 'destroyers passes : ' + str(table_points['boss passés']) + ' (' + str(table_points['dégâts boss']) + ')', 7)
        # game over
        pyxel.text((SCREEN_WIDTH//2)-20, SCREEN_HEIGHT//2, 'GAME OVER', 7)
