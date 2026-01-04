import core
import pynput
import random

class Game:
    def __init__(self):
        self.Window = core.Window()

        self.state = [[0, 0, 0, 0] for _ in range(4)]
        self.score = 0
        self.max_score = 0
        self.max_tile = 2
        self.step = 0

        self.listener = pynput.keyboard.Listener(self.on_key_press, self.on_key_release)
        self.listener.start()

    def new_tiles(self):
        zeros = []
        for i in range(4):
            for j in range(4):
                if self.state[i][j] == 0:
                    zeros.append((i, j))

        if len(zeros) > 0:
            if len(zeros) > 1:
                tile = random.choice(zeros)
                self.Window.draw_at(tile, 2)
                self.state[tile[0]][tile[1]] = 2

            tile = random.choice(zeros)
            self.Window.draw_at(tile, 2)
            self.state[tile[0]][tile[1]] = 2

        else:
            self.state = [[0, 0, 0, 0] for _ in range(4)]

    def up(self):
        for i in range(1, 4):
            for j in range(4):
                if self.state[i][j] == 0:
                    self.state[i - 1][j] = self.state[i][j]
                    self.state[i][j] = 0
                elif self.state[i][j] == self.state[i - 1][j]:
                    self.state[i][j] = 0
                    self.state[i - 1][j] *= 2

    def down(self):
        pass


    def on_key_press(self, key):
        pass

    def on_key_release(self, key):
        pass



