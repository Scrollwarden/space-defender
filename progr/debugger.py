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
        self.vars = {}

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
    
    def msg(self, text, note='MSG', location=None, condition=None):
        """
        Envoie dans le terminal le message donné

        INPUT
            text (str): le contenu du message.
            note (str): une note d'importance au début du message
            - MSG  : ce message est une information de débugage
            - INFO : ce message est une information sur le déroulé du programme.
            - WARN : ce message mérite une attention particulière
            - ERR  : ce message n'aurait pas dû être activé
            - DONE : ce message indique que le code a fonctionné
            - CHEAT : ce message indique qu'un cheat a été activé
            location (str) : where the msg is called. Line in Method from Class.
            args (tuple[str, any]): des variables a tester. A remplir sous la forme
            ('nom de la variable', variable)
        """
        if condition is None:
            condition = True
        elif not condition in self.vars.keys():
            print(f'{col.Fore.RED + col.Style.BRIGHT}DEBUGGER EXCEPTION:{col.Style.NORMAL} the condition {condition} is not define. Set on True.{col.Style.RESET_ALL}')
            condition = True
        else:
            condition = self.vars[condition]

        if self.active and condition:
            if self.filename is None:
                file = ''
            else:
                file = f'(in {col.Style.DIM}{self.filename}{col.Style.RESET_ALL})'
            
            color = col.Fore.WHITE
            if note == 'MSG':
                color = col.Fore.BLUE
            if note == 'INFO':
                color = col.Fore.BLACK
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
            if not location is None:
                print(f'{col.Style.DIM}{location}{col.Style.NORMAL}')
            print(color + col.Style.NORMAL + '----------------------------------')
            print(f'{col.Fore.WHITE}{text}')
            # for var in args:
            #     print(f'{var[0]} :', var[1])
            print('\n')

    def line(self, text):
        """Print a non formated line in the shell."""
        print(text)

    def set_var(self, name, value):
        """Define a variable for debug."""
        self.vars[name] = value

    def get_var(self, name):
        """Get a variable for debug."""
        return self.vars[name]
    
    def del_var(self, name):
        """Delete a variable registered for debug."""
        del self.vars[name]
 
    def clear_vars(self):
        """clear all variable registered in the debugger"""
        self.vars = {}