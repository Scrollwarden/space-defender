"""
Le fichier qui gère le jeu

CLASSES
- Game (Controler)
"""

import pyxel
import random
from player import Player
from enemies import Drone, Destroyer
from projectile import Explosion, Projectile
from background import Star
from constants import *

class Game:
    '''
    Controler : le contrôleur global du jeu

    ATTRIBUTS
    - player : le joueur
    - drones : la liste des drones
    - destroyer : le destroyer
    - stars : la liste des étoiles
    - explosions : la liste des explosions
    - table_points : le tableau des points
    - game_speed : la vitesse du jeu
    - vies : le nombre de vies du joueur
    - base_life : la vie de la base

    METHODS
    - update
    - draw
    - update_drones
    - update_destroyer
    - update_stars
    - check_all_collisions
    - check_collision
    - remove_deads
    - draw_score
    '''
    def __init__(self):
        self.player = Player()
        self.drones = []
        self.destroyer = Destroyer()
        self.stars = []
        self.explosions = []
        self.table_points = {'score': 0, 'drones tués': 0, 'drones passés': 0, 'destroyer tués': 0, 'destroyer passés': 0, 'dégâts destroyer': 0}
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
        self.update_destroyer()
        self.check_all_collisions()
        self.remove_deads()
        if pyxel.btnr(pyxel.KEY_K):
            self.vies = 0
            self.check_collision(self.player, self.player)
        if pyxel.btnr(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        """Dessine l'écran"""
        pyxel.cls(0)
        pyxel.rect(0, 0, GAME_SCREEN_WIDTH_START, SCREEN_HEIGHT, 0)
        pyxel.rect(0-2, 0, 2, SCREEN_HEIGHT, 13) # side bar. must be improved before release
        for star in self.stars:
            star.draw()
        if self.vies > 0:
            self.player.draw(self.table_points['score'])
        for drone in self.drones:
            drone.draw()
        self.destroyer.draw()
        self.destroyer.draw_projectiles()
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
                rand_x = random.randint(GAME_SCREEN_WIDTH_START+16, SCREEN_WIDTH-20)
                rand_y = random.randint(-25, -5)
                # apparition de chaque entité du groupe
                for _ in range(random.randint(1, 4)):
                    self.drones.append(Drone(rand_x + random.randint(-15, 15), rand_y + random.randint(-15, 15)))
                if self.table_points['score'] >= 100:
                    # niveau 1 : apparition d'un drone supplémentaire hors du groupe
                    self.drones.append(Drone(random.randint(10, 247), random.randint(0, 5)))

        # mise à jour des positions
        for drone in self.drones:
            drone.update(self.game_speed)
            if drone.y > 247:
                self.drones.remove(drone)
                if self.vies > 0 and self.base_life > 0 and self.table_points['score'] < SCORE_VICTOIRE:
                    self.table_points['drones passés'] += 1
                    self.table_points['score'] -= 1
                    self.base_life -= 1

    def update_destroyer(self):
        """Créé et met à jour les destroyers."""
        # creation
        if self.base_life > 0 and self.table_points['score'] < SCORE_VICTOIRE \
            and self.table_points['score'] >= SCORE_DESTROYER and not self.destroyer.active:
            if (pyxel.frame_count % 60 == 0) and random.randint(0, 100) < DESTROYER_SPAWN_RATE:
                self.destroyer.create()
        
        # mise à jour des positions
        self.destroyer.update(self.game_speed, self.table_points['score'])
        self.destroyer.update_projectiles(self.game_speed)
        if self.destroyer.y > 247 and self.destroyer.active:
            self.destroyer.disactive()
            if self.vies > 0 and self.base_life > 0 and self.table_points['score'] < SCORE_VICTOIRE:
                self.table_points['destroyer passés'] += 1
                self.table_points['dégâts destroyer'] += self.destroyer.health
                self.table_points['score'] -= self.destroyer.health
                self.base_life -= self.destroyer.health

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
        lazers = self.player.lazer_liste
        rockets = self.player.rockets_list
        destlazers = self.destroyer.projectiles
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

        # si un lazer percute un destroyer
        for lazer in lazers:
            self.check_collision(lazer, destroyer)
        # si une rocket percute un destroyer
        for rocket in rockets:
            self.check_collision(rocket, destroyer)
        
        for explosion in explosions:
            # si le joueur percute une explosion
            self.check_collision(player, explosion)
            # si une explosion percute un destroyer
            self.check_collision(explosion, destroyer)
        
        # si le joueur percute un destroyer
        self.check_collision(player, destroyer)

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
            # destroyer
            if type2 == Destroyer:
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
                    if self.base_life > 0: # invincibliité après la mort de la base
                        self.vies -= 1
                        if self.vies <= 0 and self.vies >= -1999: # belle explosion pour la mort
                            if self.vies >= -1:
                                self.explosions.append(Explosion(x1, y1, radius=5, etype='damage'))
                            if self.vies <= -100:
                                self.explosions.append(Explosion(x1, y1, radius=0, etype='damage'))
                    
            

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
        pyxel.text(2, 6, 'score : ' + str(self.table_points['score']), 7)
        pyxel.rect(2, 2, 8*self.base_life, 2, 11) # barre de vie de la base
        pyxel.text(8*self.base_life + 4, 1, str(self.base_life), 11)

        # répétitif. Doit tenir en boucle for
        if SCORE_DESTROYER-25 <= self.table_points['score'] <= SCORE_DESTROYER-25+4:
            pyxel.text((GAME_SCREEN_WIDTH//2)-19*2, 50, 'Shield unlocked !', 10)
        if SCORE_SPIDRONE-25 <= self.table_points['score'] <= SCORE_SPIDRONE-25+4:
            pyxel.text((GAME_SCREEN_WIDTH//2)-20*2, 50, 'Detector unlocked !', 10)
        if 100 <= self.table_points['score'] <= 104:
            pyxel.text((GAME_SCREEN_WIDTH//2)-19*2, 50, 'Rockets unlocked !', 10)
        if 200 <= self.table_points['score'] <= 204:
            pyxel.text((GAME_SCREEN_WIDTH//2)-22*2, 50, 'Double-shoot unlocked !', 10)
        if 300 <= self.table_points['score'] <= 304:
            pyxel.text((GAME_SCREEN_WIDTH//2)-22*2, 50, '2x rockets unlocked !', 10)
        if 400 <= self.table_points['score'] <= 404:
            pyxel.text((GAME_SCREEN_WIDTH//2)-22*2, 50, 'Triple-shoot unlocked !', 10)

        if 600-8 <= self.table_points['score'] <= 600:
            pyxel.text((SCREEN_WIDTH//2)-22*2, 50, 'LAST 50 POINTS.\n /!\\ CRUSADER INCOMMING /!\\', 14)

    def draw_player_ui(self):
        """Dessine l'interface du joueur autour du vaisseau"""
        vies = self.vies
        x = self.player.x
        y = self.player.y
        rocket_waiter1 = self.player.rocket_waiter1
        rocket_waiter2 = self.player.rocket_waiter2
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
        pyxel.text(0, SCREEN_HEIGHT-12, 'Canon (SPACE) : Always', 10)
        if self.table_points['score'] >= 100:
            state1, state2 = 'READY', ''
            if rocket_waiter1 != 0:
                state1 = rocket_waiter1
            if self.table_points['score'] >= 300:
                state2 = ' | READY'
            if rocket_waiter2 != 0:
                state2 = ' |' + str(rocket_waiter2)
            pyxel.text(SCREEN_WIDTH//2, SCREEN_HEIGHT-12, f'Rocket (R) : {state1}{state2}', 10)
    
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
            pyxel.text((GAME_SCREEN_WIDTH//2)-40*2, (SCREEN_HEIGHT//2)+10, 'Vous avez survecu a cette attaque', 3)