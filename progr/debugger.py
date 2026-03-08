'''
Classe de débogage : objet activable/désactivable
pour éviter d'avoir à enlever les prints.
'''

import colorama as col
import pyxel

class Debugger:
    '''
    Tool : print activable

    ATTRIBUTES
    - filename (str) : the file from where the debugger is printing.

    METHODS
    - is_active()
    - toggle(state)
    - msg(text)
    - set_var(var_name, value)
    - get_var(var_name)
    - del_var(var_name)
    - clear_vars()
    - print_vars(specific_var_name)
    '''
    def __init__(self, active=False):
        self.active = active
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
        if self.active:
            print(f'{col.Fore.YELLOW + col.Style.BRIGHT}DEBUGGER ON:{col.Style.NORMAL} Debugger is currently active.{col.Style.RESET_ALL}\n')
        else:
            print(f'{col.Fore.BLACK + col.Style.BRIGHT}DEBUGGER OFF:{col.Style.NORMAL} Debugger is currently unactive.{col.Style.RESET_ALL}\n')
    
    def msg(self, text, note='MSG', location=None, condition=None):
        """
        Envoie dans le terminal le message donné

        INPUT
        - text (str): le contenu du message.
        - note (str): une note d'importance au début du message
           - MSG  : ce message est une information de débugage
           - INFO : ce message est une information sur le déroulé du programme.
           - WARN : ce message mérite une attention particulière
           - ERR  : ce message n'aurait pas dû être activé
           - DONE : ce message indique que le code a fonctionné
           - CHEAT : ce message indique qu'un cheat a été activé
        - location (str) : where the msg is called. Line in Method from Class.
        - condition (tuple[str]): la condition d'apparition du message (qui doit avoir été définie à l'avance). True par défaut.
        """
        if condition is None:
            condition = True
        elif not condition in self.vars.keys():
            print(f'{col.Fore.RED + col.Style.BRIGHT}DEBUGGER EXCEPTION:{col.Style.NORMAL} the condition {condition} is not define. Set on True.{col.Style.RESET_ALL}\n')
            condition = True
        else:
            condition = self.vars[condition]

        if self.active and condition:
            
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

            if location is None:
                location = ''
            else:
                location = '(in ' + location + ')'

            time = pyxel.frame_count # changer les imports et cette ligne selon le moteur et la lib utilisée
            print(f'{color + note}: {col.Style.RESET_ALL} at {time} {col.Style.DIM}{location}{col.Style.NORMAL}:')
            print(color + col.Style.NORMAL + '-- ', end='')
            print(f'{col.Fore.WHITE}{text}')

    def line(self, text):
        """Print a non formated line in the shell."""
        print('DEBUGGER: ' + text)

    def set_var(self, name, value):
        """Define a variable for debug."""
        self.vars[name] = value

    def get_var(self, name):
        """Get a variable value for debug."""
        return self.vars[name] and self.is_active()
    
    def del_var(self, name):
        """Delete a variable registered for debug."""
        del self.vars[name]
 
    def clear_vars(self):
        """clear all variable registered in the debugger"""
        self.vars = {}

    def print_vars(self, specific_vars=None):
        """
        Affiche toutes les variables et leurs valeurs dans le terminal
        
        Il est possible de spécifier une liste des variables attendues.
        """
        var_list = self.vars if specific_vars is None else specific_vars
        print(f'{col.Style.BRIGHT} All vars in debugger :{col.Style.RESET_ALL}')
        if var_list == []:
            print(f'{col.Fore.RED} No variable set in debugger.{col.Style.RESET_ALL}')
        else:
            for var in var_list:
                print(f'{var[0]} : {col.Style.DIM}{var[1]}{col.Style.RESET_ALL}')