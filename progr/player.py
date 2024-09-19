"""
les fonctions gérant les différentes fonctionnalités proposées au joueur en jeu.
"""

def vaisseau_deplacement(x, y):
    """déplacement avec les touches de directions"""
    if pyxel.btn(pyxel.KEY_RIGHT):
        if (x < 247) :
            x = x + PLAYER_SPEED
    if pyxel.btn(pyxel.KEY_LEFT):
        if (x > 8) :
            x = x - PLAYER_SPEED
    if pyxel.btn(pyxel.KEY_DOWN):
        if (y < 247) :
            y = y + PLAYER_SPEED
    if pyxel.btn(pyxel.KEY_UP):
        if (y > 8) :
            y = y - PLAYER_SPEED
    return x, y

def tirs_creation(x, y, tirs_liste, key):
    """création d'un tir avec la barre d'espace pour lazer, R pour une roquette et L pour rayon lazer"""
    global rocket_waiter
    # btnr pour eviter les tirs multiples
    if pyxel.btnr(key):
        if key == pyxel.KEY_R:
            if rocket_waiter == 0:
                tirs_liste.append([x-6, y-14])
                if table_points['score'] > 199:
                    tirs_liste.append([x-10, y])
                rocket_waiter = WAIT_AFTER_ROCKET
        else:
            tirs_liste.append([x, y-10])
            if table_points['score'] > 99:
                tirs_liste.append([x+4, y+(random.randint(10, 15))])
                if table_points['score'] > 299:
                    tirs_liste.append([x+8, y+(random.randint(0, 5))])
 
    return tirs_liste

def update_rocket_waiter(waiter):
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

#def bouclier_activation():
#    """Le joueur active un bouclier devant lui avec B"""
#    if pyxel.btnr(pyxel.KEY_B):
#        bouclier = [SHIELD_POWER, SHIELD_DURATION]