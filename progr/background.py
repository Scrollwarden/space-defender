import pyxel

class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, game_speed):
        self.y += 0.5 * game_speed

    def draw(self):
        pyxel.rect(self.x, self.y, 1, 1, 7)