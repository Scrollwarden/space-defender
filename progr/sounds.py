import playsound
import threading
import random
from constants import *

class Musicien:
    '''
    Controler : Classe permettant de jouer des sons en threading en utilisant _Instruments
    '''
    def __init__(self):
        self.instruments = _Instruments()
        choices_musics = list(self.instruments.musics.keys())
        self.choices_menu = [audio for audio in choices_musics if 'Menu' in audio]
        self.choices_game = [audio for audio in choices_musics if 'Game' in audio]
        self.choices_boss = [audio for audio in choices_musics if 'Boss' in audio]
        self.music_launching = 'Launching'
        self.music_death = 'Death'
        self.music_win = 'Win'

    def launching(self):
        """joue le son de lancement du jeu"""
        self.instruments.play_music(self.music_launching)

    def menu(self):
        """joue les sons du menu"""
        audio = self.choices_menu[random.randint(0, len(self.choices_menu))]
        self.instruments.play_music(audio)

    def game(self):
        """joue les sons des niveaux"""
        audio = self.choices_game[random.randint(0, len(self.choices_game))]
        self.instruments.play_music(audio)

    def boss(self):
        """joue les sons de boss de niveau"""
        audio = self.choices_boss[random.randint(0, len(self.choices_boss))]
        self.instruments.play_music(audio)

    def defeat(self):
        """joue le son de la défaite"""
        self.instruments.play_music(self.music_death, impose=True)

    def win(self):
        """joue le son de la victoire"""
        self.instruments.play_music(self.music_win, impose=True)

    def lazer(self):
        """joue le son du tir lazer"""
        self.instruments.play_sound('LazerShoot')

    def rocket(self):
        """joue le son du tir d'une roquette"""
        self.instruments.play_sound('RocketShoot', priority=2)

    def lazerbeam(self):
        """joue le son du tir d'un rayon lazer"""
        self.instruments.play_sound('LazerbeamShoot', priority=3)

    def rocket_flight(self):
        """joue le son de la rocket en vol"""
        self.instruments.play_sound('RocketFlight')

    def lazebeam_load(self):
        """joue le son de chargement du rayon lazer"""
        pass # self.instruments.play_sound('LazerbeamLoad', priority=3)

    def explosion(self):
        """joue le son d'explosion destructrice"""
        self.instruments.play_sound('Explosion', priority=3)

    def ennemi_hit(self):
        """joue le son d'explosion lorsqu'un ennemi est touché"""
        self.instruments.play_sound('EnnemiHit', priority=2)

    def player_hit(self):
        """joue le son d'explosion quand le joueur est touché"""
        self.instruments.play_sound('PlayerHit', priority=3)

    def shield_hit(self):
        """joue le son d'explosion lorsque le bouclier du joueur est endommagé"""
        self.instruments.play_sound('ShieldHit', priority=2)

    def base_hit(self):
        """joue le son d'explosion lorsqu'un vaisseau ennemi atteint la base"""
        self.instruments.play_sound('BaseHit', priority=4, unique=True)


class _Instruments:
    '''
    Entity : Classe contenant les sons à jouer.
    Elle lance les sons en threading.
    Ne devrait être utilisée que dans Musicien

    ATTRIBUTES
    - sounds (dict) : dictionnaire des sons accessibles
    - musics (dict) : dictionnaire des musiques accessibles
    - current_tracks (dict) : dictionnaire des sons en cours de lecture

    METHODS
    - play_sound(sound_type, priority)
    - play_music(music_type, impose)
    '''
    def __init__(self):
        self.sounds = {
            'Explosion': SOUND_EXPLOSION_DESTROY,
            'EnnemiHit': SOUND_ENNEMI_HIT,
            'PlayerHit': SOUND_PLAYER_HIT,
            'ShieldHit': SOUND_PLAYER_HIT,
            'BaseHit': SOUND_PLAYER_BASE_DESTROYED,
            'LazerShoot': SOUND_SHOOT,
            'RocketShoot': SOUND_ROCKET_FIRE,
            'LazerbeamShoot': SOUND_LASERBEAM_FIRE,
            'LazerbeamLoad': SOUND_LASERBEAM_LOAD,
            'RocketFlight': SOUND_ROCKET_FLIGHT,
            'SpieDroneInvisibility': None,
            'ShieldActive': None,
            'DetectorActive': None,
            'BoosterActive': None,
            'ButtonSelected': None,
            'NewLevel': None,
            'QuitSelected': None
        }
        self.musics = {
            'Launching': MUSIC_MENU1,
            'Menu1': MUSIC_MENU1,
            'Menu2': None,
            'Game1': None,
            'Game2': MUSIC_GAME2,
            'Game3': None,
            'Boss1': MUSIC_GAME_BOSS1,
            'Boss2': None,
            'Death': MUSIC_LOSE,
            'Win': MUSIC_WIN
        }
        self.current_tracks = {'music': None, 'sounds': {1:[], 2:[]}}
        # priority must be in a dict in order to allow devs to use sounds of high priority while those of lower priority aren't in the interable yet.

    def play_music(self, music, impose=False):
        """
        Appel la musique demandée en threading

        INPUT
            music (str) : la musique demandée parmi
                (Launching, Menu, Game, Boss, Death, Win)
            impose (bool) : si True, la musique sera jouée immédiatement et toutes les autres seront coupées.
        """
        if SOUNDS_ALLOWED:
            # a way to play the music many times (random lenght)
            self.current_tracks['music'] = music
            music_thread = threading.Thread(target=self._play_music_in_thread, args=(music,))
            music_thread.start()

            # if impose: # acctualy doesn't work
            #     self.current_tracks['music'] = music
            #     music_thread = threading.Thread(target=self._play_music_in_thread, args=(music,))
            #     music_thread.start()
            # else:
            #     while self.current_tracks['music'] != None:
            #         pass # c'est déguelasse, je trouverai mieux plus tard
            #     self.current_tracks['music'] = music
            #     music_thread = threading.Thread(target=self._play_music_in_thread, args=(music,))
            #     music_thread.start()

    def play_sound(self, sound, priority=1, unique=False):
        """
        Appel le son demandé en threading

        INPUT
            sound (str) : le son demandé parmi self.sounds
            priority (int) : la priorité du son (1 par défaut)
            unique (bool) : si le son ne devrait pas être joué plusieurs fois en même temps (False par défaut)
        """
        if not priority in self.current_tracks['sounds'].keys(): # check for the existance of the priority list
                self.current_tracks['sounds'][priority] = []
        if SOUNDS_ALLOWED and len(self.current_tracks['sounds'][priority]) < MAX_SOUNDS:
            if (not unique) or (unique and sound in self.current_tracks['sounds'][priority]): # if the sound is unique it can't be added when already in the list
                sound_thread = threading.Thread(target=self._play_sound_in_thread, args=(sound, priority))
                sound_thread.start()
            # add the sound to current_tracks
            self.current_tracks['sounds'][priority].append(sound)

    def _play_sound_in_thread(self, sound, priority):
        """
        [méthode inerne de play_sound]
        
        Joue le son donné et le retire de current_track lorsqu'il finit.

        INPUT
            sound (str) : le son à jouer
            priority (int) : la priorité du son.
        """
        try:
            playsound.playsound(self.sounds[sound])
        finally:
            self.current_tracks['sounds'][priority].remove(sound)

    def _play_music_in_thread(self, music):
        """
        [méthode inerne de play_music]
        
        Joue le son donné et le retire de current_track lorsqu'il finit.

        INPUT
            music (str) : le son à jouer
        """
        try:
            playsound.playsound(self.musics[music])
        finally:
            self.current_tracks['music'] = None

    # notes pour plus tard : 
    # - parcourir current_trak pour jouer les sons au lieu de les donner dans les
    # méthodes qui remplissent current_track. 
    # - besoin d'un thread parent pour contrôler le reste et couper les musiques lors d'impose.
