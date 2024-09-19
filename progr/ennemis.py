"""
les fonctions qui gèrent les ennemis du joueur en jeu
"""
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
            ennemi[1] += 1
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
            boss[1] += 1
            if table_points['score'] > 299: # niveau 300
                ennemi[1] += 0.2
            if boss[1]>247:
                boss[2] = False
                table_points['score'] -= boss[3]
                table_points['boss passés'] += 1
                table_points['dégâts boss'] += boss[3]
    return (ennemis_liste, boss)

def boss_tirs_creation(x, y, boss_tirs):
    """création d'un tir depuis le boss"""
    # btnr pour eviter les tirs multiples
    if random.randint(0, 60) == 60 and boss[2] == True:
        boss_tirs.append([x-3, y+10])
        boss_tirs.append([x+3, y+10])
    return boss_tirs

def boss_tirs_deplacement(boss_tirs):
    """déplacement des tirs vers le bas et suppression s'ils sortent du cadre"""
    for tir in boss_tirs:
        tir[1] += 3
        if  tir[1] > 247:
            boss_tirs.remove(tir)
    return boss_tirs
   