import playsound
import threading

G_nb_threads = 0

def play_sound(sound_file, priority=1, unique=False):
    """
    joue le son du fichier son donné en threading
    sound_file (str) : le chemin vers le son
    priority (int) : la priorité du son (1 par défaut) NOT IMPLEMENTED
    unique (bool) : si le son ne devrait pas être joué plusieurs fois en même temps (False par défaut) NOT IMPLEMENTED
    """
    global G_nb_threads

    if G_nb_threads < 20 and False: # just stopped it because sounds need to be reworked
        sound_thread = threading.Thread(target=_play_sound_whithout_thread, args=(sound_file,))
        sound_thread.start()
        G_nb_threads += 1

def _play_sound_whithout_thread(sound_file):
    """fonction inerne de play_sound"""
    global G_nb_threads
    try:
        playsound.playsound(sound_file)
    finally:
        G_nb_threads -=1