"""
Le fichier qui gère le jeu

CLASSES
- Niveau (controler)
- Game (Controler)
"""

import pyxel
import random
from player import Player
from enemies import Drone, Destroyer, Cruiser
from projectile import Explosion, Projectile
from background import Star
from constants import *

class Game:
    '''
    controler : le controleur global du jeu
    '''
    def __init__(self):
        self.niveau = Niveau()

    def update(self):
        self.niveau.update()
        # cheats
        if pyxel.btnr(pyxel.KEY_K) and pyxel.btn(pyxel.KEY_SHIFT):
            self.niveau.vies = 0
            self.niveau.check_collision(self.niveau.player, self.niveau.player)
        if pyxel.btnr(pyxel.KEY_L) and pyxel.btn(pyxel.KEY_SHIFT):
            self.niveau.table_points['score'] += 100
        # fonctionnel
        if pyxel.btnr(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnr(pyxel.KEY_RETURN) and (self.niveau.vies <= 0 or self.niveau.table_points['score'] >= 650 or self.niveau.base_life <= 0):
            self.niveau = Niveau()

    def draw(self):
        self.niveau.draw()

class Niveau:
    '''
    Controler : le contrôleur global d'un niveau

    ATTRIBUTS
    - player : le joueur

    METHODS
    - update
    - draw
    '''
    def __init__(self):
        self.player = Player()
        self.drones = []
        self.destroyer = Destroyer()
        self.cruiser = Cruiser()
        self.stars = []
        self.explosions = []
        self.table_points = {'score': 0,
                             'drones tués': 0,
                             'drones passés': 0,
                             'destroyer tués': 0,
                             'destroyer passés': 0, 'dégâts destroyer': 0,
                             'croiseur tués': 0, 'dégâts croiseur': 0}
        self.game_speed = GAME_SPEED
        self.vies = PLAYER_LIFE
        self.base_life = BASE_LIFE

        for y in range(1, 256):
            self.stars.append(Star(random.randint(GAME_SCREEN_WIDTH_START, SCREEN_WIDTH), y))

    def update(self):
        """Met à jour tout le jeu"""
        self.update_stars()
        self.player.update(self.game_speed, self.vies, self.table_points['score'])
        self.update_explosions()
        self.update_drones()
        self.update_destroyer_cruiser()
        self.check_all_collisions()
        self.remove_deads()

    def draw(self):
        """Dessine l'écran"""
        pyxel.cls(0)
        pyxel.rect(0, 0, GAME_SCREEN_WIDTH_START, SCREEN_HEIGHT, 0)
        pyxel.rect(0-2, 0, 2, SCREEN_HEIGHT, 13) # side bar. must be improved before release
        pyxel.text(SCREEN_WIDTH-25*2, 12, 'Quit app (Q)', 8)
        for star in self.stars:
            star.draw()
        if self.vies > 0:
            self.player.draw(self.table_points['score'])
        for drone in self.drones:
            drone.draw()
        self.destroyer.draw()
        self.destroyer.draw_projectiles()
        self.cruiser.draw()
        self.cruiser.draw_projectiles()
        for explosion in self.explosions:
            explosion.draw()
        if self.vies > 0 and self.base_life > 0 and self.table_points['score'] < SCORE_VICTOIRE:
            self.draw_player_ui()
            self.draw_score()
        else:
            self.draw_game_over()

    def update_explosions(self):
        """Met à jour les explosions"""
        for explosion in self.explosions:
            explosion.update()
    
    def update_drones(self):
        """Créé et met à jour les drones"""
        # creation
        if self.base_life > 0 and self.table_points['score'] < SCORE_VICTOIRE:
            if (pyxel.frame_count % 60 == 0):
                # point d'apparition d'un groupe
                rand_x = random.randint(GAME_SCREEN_WIDTH_START+16, SCREEN_WIDTH-30)
                rand_y = random.randint(-25, -5)
                # apparition de chaque entité du groupe
                for _ in range(random.randint(1, 4)):
                    self.drones.append(Drone(rand_x + random.randint(-15, 15), rand_y + random.randint(-15, 15)))
                if self.table_points['score'] >= SCORE_DRONE_ALONE1:
                    # apparition d'un drone supplémentaire hors du groupe
                    self.drones.append(Drone(random.randint(10, SCREEN_WIDTH-30), random.randint(-10, -5)))
                if self.table_points['score'] >= SCORE_DRONE_ALONE1:
                    # apparition d'un drone supplémentaire hors du groupe
                    self.drones.append(Drone(random.randint(10, SCREEN_WIDTH-30), random.randint(-10, -5)))

        # mise à jour des positions
        for drone in self.drones:
            drone.update(self.game_speed, self.table_points['score'])
            if drone.y > 247:
                self.drones.remove(drone)
                if self.vies > 0 and self.base_life > 0 and self.table_points['score'] < SCORE_VICTOIRE:
                    self.table_points['drones passés'] += 1
                    self.table_points['score'] -= 1
                    self.base_life -= 1

    def update_destroyer_cruiser(self):
        """Créé et met à jour les destroyers et les croiseurs."""
        # creation
        if self.base_life > 0 and self.table_points['score'] < SCORE_VICTOIRE :
            if self.table_points['score'] >= SCORE_DESTROYER and not self.destroyer.active:
                if (pyxel.frame_count % 60 == 0) and random.randint(0, 100) < DESTROYER_SPAWN_RATE:
                    self.destroyer.create()
            if self.table_points['score'] >= SCORE_CRUISER and not self.cruiser.active:
                if (pyxel.frame_count % 60 == 0) and random.randint(0, 100) < CRUISER_SPAWN_RATE:
                    self.cruiser.create()
        
        # mise à jour des positions
        for astronef in (self.destroyer, self.cruiser):
            astronef.update(self.game_speed, self.table_points['score'])
            astronef.update_projectiles(self.game_speed)
            if astronef.y > 247 and astronef.active:
                astronef.disactive()
                if self.vies > 0 and self.base_life > 0 and self.table_points['score'] < SCORE_VICTOIRE:
                    self.table_points['destroyer passés'] += 1
                    self.table_points['dégâts destroyer'] += astronef.health
                    self.table_points['score'] -= astronef.health
                    self.base_life -= astronef.health

    def update_stars(self):
        """met à jour les étoiles en fond"""
        # creation
        if (pyxel.frame_count % 15 == 0):
            for _ in range(random.randint(6, 10)):
                self.stars.append(Star(random.randint(GAME_SCREEN_WIDTH_START, SCREEN_WIDTH), 0))

        # deplacement
        for star in self.stars:
            star.update(self.game_speed)
            if star.y > 256:
                self.stars.remove(star)

    def check_all_collisions(self):
        """
        Vérifie les collisions des astronefs entre-eux et avec les projectiles
        """
        player = self.player
        destroyer = self.destroyer
        cruiser = self.cruiser
        lazerbeam_lazers = []
        for lazerbeam in self.player.lazerbeam_list:
            lazerbeam_lazers += lazerbeam.list_lazer
        lazers = self.player.lazer_liste + lazerbeam_lazers
        rockets = self.player.rockets_list
        lazerbeam_destlazer = []
        for lazerbeam in self.cruiser.lazerbeam_list:
            lazerbeam_destlazer += lazerbeam.list_lazer
        destlazers = self.destroyer.projectiles + lazerbeam_destlazer
        explosions = [expl for expl in self.explosions if expl.etype == 'damage']

        for drone in self.drones:
            # si le joueur percute un drone
            self.check_collision(player, drone)
            for lazer in lazers:
                # si un lazer percute un drone
                self.check_collision(lazer, drone)
            for rocket in rockets:
                # si une roquette percute un drone
                self.check_collision(rocket, drone)
            for explosion in explosions:
                # si une explosion percute un drone
                self.check_collision(explosion, drone)

        # si un lazer percute un destroyer ou un croiseur
        for lazer in lazers:
            self.check_collision(lazer, destroyer)
            self.check_collision(lazer, cruiser)
        # si une rocket percute un destroyer ou un croiseur
        for rocket in rockets:
            self.check_collision(rocket, destroyer)
            self.check_collision(rocket, cruiser)
        
        for explosion in explosions:
            # si le joueur percute une explosion
            self.check_collision(player, explosion)
            # si une explosion percute un destroyer ou un croiseur
            self.check_collision(explosion, destroyer)
            self.check_collision(explosion, cruiser)
        
        # si le joueur percute un destroyer ou un croiseur
        self.check_collision(player, destroyer)
        self.check_collision(player, cruiser)

        # si le joueur percute un lazer du destroyer
        for destlazer in destlazers:
            self.check_collision(player, destlazer)
    
    def check_collision(self, entity1, entity2):
        """
        vérifie les collisions entre deux entités

        entity1 (Player, Projectile.ptype=lazer, Projectile.ptype=rocket, Explosion.etype=damage) :
        la première entité à vérifier\n
        entity2 (Drone, Destroyer, Projectile.ptype=destlazer, Explosion.etype=damage) :
        la seconde entité à vérifier

        WARNING : if one of the argument do not contain one of the acceptable classes, the game will crash.
        """
        # si le vaisseau est mort, éviter les collisions fantomes sur l'écran de game over
        if type(entity1) == Player and self.vies <= -2000:
            return None

        # programme de collisions
        type1 = type(entity1)
        type2 = type(entity2)
        x1, y1 = entity1.x, entity1.y
        x2, y2 = entity2.x, entity2.y
        hb1_x, hb1_y, hb1_w, hb1_h = entity1.hitbox
        hb2_x, hb2_y, hb2_w, hb2_h = entity2.hitbox
        # hitbox
        if x1 + hb1_x <= x2 + hb2_w and x1 + hb1_w >= x2 + hb2_x \
        and y1 + hb1_y <= y2 + hb2_h and y1 + hb1_h >= y2 + hb2_y:
            # drone
            if type2 == Drone:
                entity2.dead = True
                self.explosions.append(Explosion(x2+(hb2_w//2), y2+(hb2_h//2)))
            # destroyer ou croiseur
            if type2 in (Destroyer, Cruiser):
                entity2.health -= 1
                self.explosions.append(Explosion(x2, y2))
                if entity2.health <= 0:
                    entity2.dead = True
            # lazer ou rocket
            if type1 == Projectile and type2 != Explosion:
                if entity1.ptype in ('lazer', 'rocket', 'destlazer'):
                    entity1.target_hit = True
            if type2 == Projectile and type1 != Explosion: # il s'agit forcément d'un destlazer
                entity2.target_hit = True
            # joueur
            if type1 == Player:
                if entity1.shield.active:
                    self.explosions.append(Explosion(x1, y1, color=13))
                    entity1.shield.power -= 1
                else:
                    self.explosions.append(Explosion(x1, y1, radius=2))
                    if self.base_life > 0 or self.table_points['score'] >= SCORE_VICTOIRE: # invincibliité après la mort de la base ou la victoire
                        self.vies -= 1
                        if self.vies <= 0 and self.vies >= -2000: # belle explosion pour la mort
                            self.explosions.append(Explosion(x1, y1, radius=2, etype='damage'))
                    
            

    def remove_deads(self):
        """
        Supprime les astronefs morts, et change le score en fonction
        Supprime les explosions finies
        Supprime les rockets (il faut ajouter les explosions ici)
        Les autres projectiles sont retirés dans les classes Player et Destroyer
        """
        # drones
        for drone in self.drones:
            if drone.dead:
                self.drones.remove(drone)
                if self.vies > 0 and self.base_life > 0 and self.table_points['score'] < SCORE_VICTOIRE:
                    self.table_points['drones tués'] += 1
                    self.table_points['score'] += 1
        # destroyers
        if self.destroyer.dead:
            if self.vies > 0 and self.base_life > 0 and self.table_points['score'] < SCORE_VICTOIRE:
                self.table_points['destroyer tués'] += 1
                self.table_points['score'] += DESTROYER_LIFE
            self.destroyer.disactive()
        # croiseur
        if self.cruiser.dead:
            if self.vies > 0 and self.base_life > 0 and self.table_points['score'] < SCORE_VICTOIRE:
                self.table_points['croiseur tués'] += 1
                self.table_points['score'] += CRUISER_HEALTH
            self.cruiser.disactive()
        # rockets
        for rocket in self.player.rockets_list:
            if rocket.target_hit:
                self.explosions.append(Explosion(rocket.x, rocket.y, radius=2, etype='damage'))
                self.player.rockets_list.remove(rocket)
        # explosions
        for explosion in self.explosions:
            if explosion.step >= 5:
                self.explosions.remove(explosion)

    def draw_score(self):
        """Dessine le score à l'écran et la vie de la base"""
        score = self.table_points['score']

        pyxel.text(2, 6, 'score : ' + str(self.table_points['score']), 7)
        pyxel.rect(2, 2, 8*self.base_life, 2, 11) # barre de vie de la base
        pyxel.text(8*self.base_life + 4, 1, str(self.base_life), 11)

        # répétitif. Doit tenir en boucle for
        message = ''
        if SCORE_DESTROYER-25 <= score <= SCORE_DESTROYER-25+4:
            message = 'Shield unlocked !'
        if SCORE_SPIDRONE-25 <= score <= SCORE_SPIDRONE-25+4:
            message = 'Detector unlocked !'
        if SCORE_ROCKET <= score <= SCORE_ROCKET+4:
            message = 'Rockets unlocked !'
        if SCORE_DOUBLE_TIR <= score <= SCORE_DOUBLE_TIR+4:
            message = 'Double-shoot unlocked !'
        if SCORE_DOUBLE_ROCKET <= score <= SCORE_DOUBLE_ROCKET+4:
            message = '2x rockets unlocked !'
        if SCORE_TRIPLE_TIR <= score <= SCORE_TRIPLE_TIR+4:
            message = 'Triple-shoot unlocked !'
        if SCORE_BOOSTER <= score <= SCORE_BOOSTER+4:
            message = 'Booster unlocked !'
        if SCORE_LAZERBEAM <= score <= SCORE_LAZERBEAM+4:
           message = 'Lazerbeam unlocked !'
        color = 10
        if SCORE_VICTOIRE-60 <= score <= SCORE_VICTOIRE-50: # work only for level 1 
            message = '\t\tLAST 50 POINTS.\n /!\\ CRUSADER INCOMMING /!\\'
            color = 14
        
        pyxel.text((SCREEN_WIDTH//2)-len(message)*2, 50, message, color)

    def draw_player_ui(self):
        """Dessine l'interface du joueur autour du vaisseau"""
        vies = self.vies
        x = self.player.x
        y = self.player.y
        score = self.table_points['score']
        rocket_waiter1 = self.player.rocket_waiter1
        rocket_waiter2 = self.player.rocket_waiter2
        lazerbeam_waiter = self.player.lazerbeam_waiter
        detector_dur = self.player.detector.duration

        if vies != PLAYER_LIFE:
            pyxel.rect(x+16, y-1, 2*vies, 1, 14) # barre de vie
        if rocket_waiter1 != 0:
            pyxel.text(x-14, y-2, str(rocket_waiter1), 10) # compteur de chargement du tube 1
        if rocket_waiter2 != 0:
            pyxel.text(x-14, y+2, str(rocket_waiter2), 10) # compteur de chargement du tube 2
        if detector_dur != MAX_DETECTOR_DURATION:
            pyxel.dither(0.5)
            pyxel.rect(x+16, y+1, detector_dur, 1, 11)
            pyxel.dither(1)
        pyxel.text(SCREEN_WIDTH//2, SCREEN_HEIGHT-18, 'Engine (ARROW) : Always', 10) #←↑↓→
        pyxel.text(0, SCREEN_HEIGHT-18, 'Canon (SPACE) : Always', 10)
        if score >= SCORE_ROCKET:
            state1, state2 = 'READY', ''
            if rocket_waiter1 != 0:
                state1 = rocket_waiter1
            if score >= SCORE_DOUBLE_ROCKET:
                state2 = ' | READY'
            if rocket_waiter2 != 0:
                state2 = ' | ' + str(rocket_waiter2)
            pyxel.text(0, SCREEN_HEIGHT-12, f'Rocket (R) : {state1}{state2}', 10)
        if score >= SCORE_LAZERBEAM:
            stateL = 'READY'
            if lazerbeam_waiter != 0:
                stateL = lazerbeam_waiter
            pyxel.text(0, SCREEN_HEIGHT-6, f'Lazerbeam (F) : {stateL}', 10)
        
        if score >= SCORE_DESTROYER-25:
            self.player.shield.draw_shield_ui()
        if score >= SCORE_SPIDRONE-25:
            self.player.detector.draw_detector_ui()
    
    def draw_game_over(self):
        """Dessine le game over à l'écran"""
        # tableau de score
        pyxel.text(64, 12, 'score : ' + str(self.table_points['score']), 7)
        pyxel.text(64, 19, 'drones tues : ' + str(self.table_points['drones tués']), 7)
        pyxel.text(64, 26, 'destroyers tues : ' + str(self.table_points['destroyer tués']), 7)
        pyxel.text(64, 33, 'drones passes : ' + str(self.table_points['drones passés']), 7)
        pyxel.text(64, 40, 'destroyers passes : ' + str(self.table_points['destroyer passés']) + ' (' + str(self.table_points['dégâts destroyer']) + ')', 7)
        # game over
        pyxel.text((GAME_SCREEN_WIDTH//2)-9*2, SCREEN_HEIGHT//2, 'GAME OVER', 7)
        if self.vies <= 0:
            pyxel.text((GAME_SCREEN_WIDTH//2)-30*2, (SCREEN_HEIGHT//2)+10, 'Votre vaisseau a ete detruit.', 9)
        if self.base_life <= 0:
            pyxel.text((GAME_SCREEN_WIDTH//2)-26*2, (SCREEN_HEIGHT//2)+10, 'La base a ete dementelee.', 8)
        if self.table_points['score'] >= SCORE_VICTOIRE:
            pyxel.text((GAME_SCREEN_WIDTH//2)-40*2, (SCREEN_HEIGHT//2)+10, 'Vous avez survecu a cette attaque !', 3)
        pyxel.text((GAME_SCREEN_WIDTH//2)-20*2, (SCREEN_HEIGHT//2)+40, '> RESTART (ENTER)', 3)