"""
Le fichier qui gère le jeu

CLASSES
- Niveau (controler)
- Game (Controler)
"""

import pyxel
import random
from sounds import Musicien
from intro import MainScreen, LaunchingScreen
from player import Player
from enemies import Drone, Destroyer, Cruiser, Frigat, Spidrone, Dreadnought
from projectile import Explosion, Projectile
from background import StarField
from constants import *

DEBUGGER.set_filename('run.py')

class Game:
    '''
    controler : le controleur global du jeu

    ATTRIBUTES
    - score (dict) : le score du joueur
    - current_screen (LaunchingScreen | MainScreen | Niveau) : l'écran en cours d'execution
    - nb_levels (int) : le nombre de niveaux déjà gagnés

    METHODS
    - update()
    - draw()
    '''
    def __init__(self):
        self.score = {
            'score': 0,
            'classe I tues': 0,
            'classe II tues': 0,
            'ennemis passes': 0,
            'degats totaux': 0
        }
        self.current_screen = LaunchingScreen()
        self.nb_levels = 0
        self.musicien = Musicien()

        DEBUGGER.msg('Game Launched.', note='INFO')

    def update(self):
        """met à jour le jeu"""
        self.current_screen.update()
        if type(self.current_screen) == LaunchingScreen:
            self._update_launching()
        if type(self.current_screen) == MainScreen:
            self._update_main_screen()
            if pyxel.btnr(pyxel.KEY_Q):
                DEBUGGER.msg('ON QUIT\nGame was stopped on user commande Q.', note='INFO')
                pyxel.quit()
        if type(self.current_screen) == Niveau:
            # cheats
            if DEBUGGER.is_active():
                self._key_cheats()
            # fonctionnel
            #   others keys
            self._key_reset()
            self._key_continue()
            #   quit app
            if pyxel.btnr(pyxel.KEY_M):
                DEBUGGER.msg('ON KEY M\nLevel was stopped. Go back to Menu.', note='INFO')
                self.current_screen = MainScreen()

    def _update_launching(self):
        """
        [methode interne de update]
        Met à jour l'écran d'accueil
        """
        if self.current_screen.progress >= self.current_screen.duration:
            self.current_screen = MainScreen()
    
    def _update_main_screen(self):
            """
            [methode interne de update]
            Met à jour le menu du jeu
            """
            if pyxel.btnr(pyxel.KEY_P):
                for key in self.score.keys(): # on remet tout à zéro
                    self.score[key] = 0
                self.current_screen = Niveau(self.score, self.nb_levels) # le niveau actuel est le niveau 1
            if pyxel.btnr(pyxel.KEY_Q):
                DEBUGGER.msg('ON QUIT\nGame was stopped on user commande Q.', note='INFO')
                pyxel.quit()
    
    def _key_reset(self):
        """
        [methode interne de update]
        Gère les interactions avec les écrans de fin pour recommencer le niveau
        """
        if (self.current_screen.vies <= 0 \
        or self.current_screen.table_points['score'] >= (SCORE_VICTOIRE * self.current_screen.current_level) \
        or self.current_screen.base_life <= 0) \
        and pyxel.btnr(pyxel.KEY_BACKSPACE): # marche aussi pour l'écran de victoire si volonté de reset
            for key in self.score.keys(): # on remet tout à zéro
                self.score[key] = 0
            self.score['score'] = SCORE_VICTOIRE * self.nb_levels
            self.current_screen = Niveau(self.score, self.nb_levels)

    def _key_continue(self):
        """
        [methode interne de update]
        Gère les interactions avec les écrans de fin pour continuer au niveau suivant
        """
        if self.current_screen.table_points['score'] >= (SCORE_VICTOIRE * self.current_screen.current_level) \
        and pyxel.btnr(pyxel.KEY_RETURN):
            self.nb_levels += 1
            self.current_screen = Niveau(self.score, self.nb_levels)

    def _key_cheats(self):
        """
        [methode interne de update]
        Gère les interactions de type cheat durant le jeu
        """
        if pyxel.btn(pyxel.KEY_SHIFT):
            if pyxel.btnr(pyxel.KEY_K): # kill self
                DEBUGGER.msg('ON SELF KILL\nPlayer should be destroyed.', note='CHEAT')
                self.current_screen.vies = 0
                self.current_screen._check_collision(self.current_screen.player, self.current_screen.player) # collision avec lui-même pour conserver l'animation
            if pyxel.btnr(pyxel.KEY_L): # level up
                if pyxel.btn(pyxel.KEY_C):
                    DEBUGGER.msg('ON CHECKPOINT UP\nPlayer should gain 650 points and reach next Level Checkpoint.', note='CHEAT')
                    self.score['score'] += 650
                else:
                    DEBUGGER.msg('ON LEVEL UP\nPlayer sould gain 100 points.', note='CHEAT')
                    self.score['score'] += 100

    def draw(self):
        """dessine le jeu à l'écran"""
        self.current_screen.draw()

class Niveau:
    '''
    Controler : le contrôleur global d'un niveau

    ATTRIBUTS
    - current_level (int) : le niveau en cours
    - table_point (dict) : le dictionnaire des scores marqués pendant la partie

    METHODS
    - update()
    - draw()
    '''
    def __init__(self, score, level):
        self.current_level = level+1
        self.play_the_sound = Musicien()
        self.player = Player()
        self.drones = []
        self.destroyer = Destroyer()
        self.cruiser = Cruiser()
        self.background = StarField()
        self.explosions = []
        self.table_points = score
        self.game_speed = GAME_SPEED
        self.vies = PLAYER_LIFE
        self.base_life = BASE_LIFE

        DEBUGGER.msg(f'LEVEL CREATION\nLevel {self.current_level} is starting.', note='INFO')

    def update(self):
        """Met à jour tout le jeu"""
        self.background.update(self.game_speed)
        self.player.update(self.game_speed, self.vies, self.table_points['score'])
        self._update_explosions()
        self._update_drones()
        self._update_destroyer_cruiser()
        self._check_all_collisions()
        self._remove_deads()

    def draw(self):
        """Dessine l'écran"""
        pyxel.cls(0)
        # pyxel.rect(0, 0, GAME_SCREEN_WIDTH_START, SCREEN_HEIGHT, 0)
        # pyxel.rect(0-2, 0, 2, SCREEN_HEIGHT, 13) # side bar. must be improved before release
        self.background.draw()
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

        if self.vies > 0 and self.base_life > 0 \
        and not self.table_points['score'] >= (SCORE_VICTOIRE*self.current_level):
            DEBUGGER.set_var('game over', False)
            self._draw_player_ui()
            self._draw_score()
            pyxel.text(SCREEN_WIDTH-25*2, 12, 'Quit game (M)', 8)
        else:
            DEBUGGER.set_var('game over', True)
            self.draw_game_over() # may move to Game class

    def _update_explosions(self):
        """
        [methode interne de update]
        Met à jour les explosions
        """
        for explosion in self.explosions:
            explosion.update()
    
    def _update_drones(self):
        """
        [methode interne de update]
        Créé et met à jour les drones
        """
        # creation
        if self.base_life > 0 \
        and not self.table_points['score'] >= (SCORE_VICTOIRE*self.current_level):
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
            if drone.y > SCREEN_HEIGHT+10:
                self.drones.remove(drone)
                if self.vies > 0 and self.base_life > 0 \
                and not self.table_points['score'] >= (SCORE_VICTOIRE*self.current_level):
                    self.play_the_sound.base_hit()
                    self.table_points['ennemis passes'] += 1
                    self.table_points['degats totaux'] += 1
                    self.table_points['score'] -= 1
                    self.base_life -= 1

    def _update_destroyer_cruiser(self):
        """
        [methode interne de update]
        Créé et met à jour les destroyers et les croiseurs.
        """
        # creation
        if self.base_life > 0 \
        and not self.table_points['score'] >= (SCORE_VICTOIRE*self.current_level) :
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
            if astronef.y > SCREEN_HEIGHT+10 and astronef.active:
                self.play_the_sound.base_hit()
                if self.vies > 0 and self.base_life > 0 \
                and not self.table_points['score'] >= (SCORE_VICTOIRE*self.current_level):
                    self.table_points['ennemis passes'] += 1
                    self.table_points['degats totaux'] += astronef.health
                    self.table_points['score'] -= astronef.health
                    self.base_life -= astronef.health
                astronef.disactive()

    def _check_all_collisions(self):
        """
        [methode interne de update]
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
            self._check_collision(player, drone)
            for lazer in lazers:
                # si un lazer percute un drone
                self._check_collision(lazer, drone)
            for rocket in rockets:
                # si une roquette percute un drone
                self._check_collision(rocket, drone)
            for explosion in explosions:
                # si une explosion percute un drone
                self._check_collision(explosion, drone)

        # si un lazer percute un destroyer ou un croiseur
        for lazer in lazers:
            self._check_collision(lazer, destroyer)
            self._check_collision(lazer, cruiser)
        # si une rocket percute un destroyer ou un croiseur
        for rocket in rockets:
            self._check_collision(rocket, destroyer)
            self._check_collision(rocket, cruiser)
        
        for explosion in explosions:
            # si le joueur percute une explosion
            self._check_collision(player, explosion)
            # si une explosion percute un destroyer ou un croiseur
            self._check_collision(explosion, destroyer)
            self._check_collision(explosion, cruiser)
        
        # si le joueur percute un destroyer ou un croiseur
        self._check_collision(player, destroyer)
        self._check_collision(player, cruiser)

        # si le joueur percute un lazer du destroyer
        for destlazer in destlazers:
            self._check_collision(player, destlazer)
    
    def _check_collision(self, entity1, entity2):
        """
        [methode interne de _check_all_collisions]
        vérifie les collisions entre deux entités

        INPUT
            entity1 (Player | Projectile.ptype=lazer | Projectile.ptype=rocket | Explosion.etype=damage) :
        la première entité à vérifier
            entity2 (Drone | Destroyer | Projectile.ptype=destlazer | Explosion.etype=damage) :
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
                self.play_the_sound.ennemi_hit()
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
                    #play_sound(SOUND_PLAYER_HIT)
                    if self.base_life > 0 \
                    or not self.table_points['score'] >= (SCORE_VICTOIRE*self.current_level): # invincibliité après la mort de la base ou la victoire
                        self.vies -= 1
                        DEBUGGER.set_var('player dead', self.vies <= -2000)
                        DEBUGGER.msg(f'Player died at {pyxel.frame_count}. Game is Over.', note='INFO', condition='player dead')
                        if self.vies <= 0 and self.vies >= -2000: # belle explosion pour la mort
                            self.explosions.append(Explosion(x1, y1, radius=2, etype='damage'))
                    
    def _remove_deads(self):
        """
        [methode interne de update]
        Supprime les astronefs morts, et change le score en fonction
        Supprime les explosions finies
        Supprime les rockets (il faut ajouter les explosions ici)
        Les autres projectiles sont retirés dans les classes Player et Destroyer
        """
        # drones
        for drone in self.drones:
            if drone.dead:
                self.drones.remove(drone)
                self.play_the_sound.ennemi_hit()
                if self.vies > 0 and self.base_life > 0 \
                and not self.table_points['score'] >= (SCORE_VICTOIRE*self.current_level):
                    self.table_points['classe I tues'] += 1
                    self.table_points['score'] += 1
        # destroyers
        if self.destroyer.dead:
            if self.vies > 0 and self.base_life > 0 \
            and not self.table_points['score'] >= (SCORE_VICTOIRE*self.current_level):
                self.table_points['classe II tues'] += 1
                self.table_points['score'] += DESTROYER_LIFE
            self.play_the_sound.ennemi_hit()
            self.destroyer.disactive()
        # croiseur
        if self.cruiser.dead:
            if self.vies > 0 and self.base_life > 0 \
            and not self.table_points['score'] >= (SCORE_VICTOIRE*self.current_level):
                self.table_points['classe II tues'] += 1
                self.table_points['score'] += CRUISER_HEALTH
            self.play_the_sound.ennemi_hit()
            self.cruiser.disactive()
        # rockets
        for rocket in self.player.rockets_list:
            if rocket.target_hit:
                self.explosions.append(Explosion(rocket.x, rocket.y, radius=2, etype='damage'))
                self.play_the_sound.explosion()
                self.player.rockets_list.remove(rocket)
        # explosions
        for explosion in self.explosions:
            if explosion.step >= 5:
                self.explosions.remove(explosion)

    def _draw_score(self):
        """
        [fonction interne de draw]
        Dessine le score à l'écran et la vie de la base
        """
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
        if (SCORE_VICTOIRE*self.current_level)-70 <= score <= (SCORE_VICTOIRE*self.current_level)-50: # work only for level 1 
            message = '/!\\ DREADNOUGHT INCOMMING /!\\'
            color = 14
        
        pyxel.text((SCREEN_WIDTH//2)-len(message)*2, 50, message, color)

    def _draw_player_ui(self):
        """
        [methode interne de draw]
        Dessine l'interface du joueur autour du vaisseau
        """
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
        """
        [methode interne de draw] # may move to Game ?
        Dessine le game over à l'écran
        """
        mid = (GAME_SCREEN_WIDTH//2)
        # tableau de score
        pyxel.text(mid-16, 12, f'NIVEAU {self.current_level}', 7)
        tab_score = 48
        pyxel.text(mid-48, tab_score + 12, 'score : ' + str(self.table_points['score']), 7)
        pyxel.text(mid-48, tab_score + 19, 'Classe I tues : ' + str(self.table_points['classe I tues']), 7)
        pyxel.text(mid-48, tab_score + 26, 'Classe II tues : ' + str(self.table_points['classe II tues']), 7)
        pyxel.text(mid-48, tab_score + 40, 'Ennemis passes : ' + str(self.table_points['ennemis passes']) + ' (' + str(self.table_points['degats totaux']) + ')', 7)
        # game over
        pyxel.text(mid-9*2, SCREEN_HEIGHT//2, 'GAME OVER', 7)
        if self.vies <= 0:
            pyxel.text(mid-30*2, (SCREEN_HEIGHT//2)+10, 'Votre vaisseau a ete detruit.', 9)
        if self.base_life <= 0:
            pyxel.text(mid-26*2, (SCREEN_HEIGHT//2)+10, 'La base a ete dementelee.', 8)
        if self.table_points['score'] >= (SCORE_VICTOIRE*self.current_level):
            pyxel.text(mid-40*2, (SCREEN_HEIGHT//2)+10, 'Vous avez survecu a cette attaque !', 3)
            pyxel.text(mid-18*2, (SCREEN_HEIGHT//2)+30, '> CONTINUE (ENTER)',9)
            pyxel.text(mid-18, 24, 'COMPLETED', 10)
        else:
            pyxel.text(mid-12, 24, 'FAILED', 10)
        pyxel.text(mid-21*2, (SCREEN_HEIGHT//2)+40, '> RESTART (BACKSPACE)', 3)
        pyxel.text(mid-18*2, (SCREEN_HEIGHT//2)+60, '> QUIT TO MENU (M)', 8)