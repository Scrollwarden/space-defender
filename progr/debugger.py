'''
Classe de débogage : objet activable/désactivable
pour éviter d'avoir à enlever les prints.
'''

import colorama as col

class Debugger:
    '''
    Tool : print activable

    ATTRIBUTES
    - filename (str) : the file from where the debugger is printing.

    METHODS
    - is_active()
    - toggle()
    - set_filename(filename)
    - msg(text)
    '''
    def __init__(self, filename=None, active=False):
        self.active = active
        self.filename = filename

    def is_active(self):
        """Renvoie si oui ou non le debugger est actif."""
        return self.active
    
    def toggle(self, state=None):
        """Change l'état du débugger."""
        if state is None:
            self.active = not self.active
        else:
            self.active = state

    def set_filename(self, filename):
        """redéfinie le nom du fichier d'où le message est envoyé"""
        self.filename = filename
    
    def msg(self, text, note='MSG', location=None):
        """
        Envoie dans le terminal le message donné

        INPUT
            text (str): le contenu du message.
            note (str): une note d'importance au début du message
            - MSG  : ce message est une information
            - ERR  : ce message n'aurait pas dû être activé
            - WARN : ce message mérite une attention particulière
            - DONE : ce message indique que le code a fonctionné
            - CHEAT : ce message indique qu'un cheat a été activé
            location (str) : where the msg is called. Line in Method from Class.
            kwargs (tuple[str, any]): des variables a tester. A remplir sous la forme
            ('nom de la variable', variable)
        """
        if self.active:
            if self.filename is None:
                file = ''
            else:
                file = f'(in {col.Style.DIM + self.filename + col.Style.RESET_ALL})'
            
            color = col.Fore.BLUE
            if note == 'WARN':
                color = col.Fore.YELLOW
            if note == 'ERR':
                color = col.Fore.RED
            if note == 'DONE':
                color = col.Fore.GREEN
            if note == 'CHEAT':
                color = col.Fore.CYAN
            color = color + col.Style.BRIGHT
            print(f'{color + note}: {col.Style.RESET_ALL}Debugger {file}:')
            print(color + col.Style.NORMAL + '----------------------------------')
            print(col.Fore.WHITE +text)
            # for var in kwargs:
            #     print(f'{var[0]} :', var[1])
            print('\n')

    def line(self, text):
        """Print a non formated line in the shell."""
        print(text)
 
# Debugger(active=True).msg('Debugger is working correctly.', 'DONE')