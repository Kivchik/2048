import core
import pynput
import random
import time

class Game:
    def __init__(self):
        self.Window = core.Window()

        self.state = [[0, 0, 0, 0] for _ in range(4)]
        self.score = 0
        self.max_score = 0
        self.max_tile = 2
        self.step = 0

        self.new_tiles()
        self.draw()

        self.listener = pynput.keyboard.Listener(self.on_key_press, self.on_key_release)
        self.listener.start()

        while True: time.sleep(0.01)


    # def draw(self):
    #     for i in range(4):
    #         for j in range(4):
    #             self.Window.draw_at((i,j), self.state[i][j])

    def draw(self):
        for i in self.state:
            print("\n",i)


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
                if self.state[i][j] != 0 and self.state[i - 1][j] == 0:
                    self.state[i - 1][j] = self.state[i][j]
                    self.state[i][j] = 0
                elif self.state[i][j] == self.state[i - 1][j]:
                    self.state[i][j] = 0
                    self.state[i - 1][j] *= 2

    def down(self):
        for i in range(1, 4):
            for j in range(4):
                if self.state[3 - i][j] != 0 and self.state[4 - i][j] == 0:
                    self.state[4 - i][j] = self.state[3 - i][j]
                    self.state[3 - i][j] = 0
                elif self.state[3 - i][j] == self.state[4 - i][j]:
                    self.state[3 - i][j] = 0
                    self.state[4 - i][j] *= 2

    def right(self):
        for i in range(4):
            for j in range(1, 4):
                if self.state[i][3 - j] != 0 and self.state[i][4 - j] == 0:
                    self.state[4 - i][j] = self.state[i][3 - j]
                    self.state[i][3 - j] = 0
                elif self.state[i][3 - j] == self.state[i][4 - j]:
                    self.state[i][3 - j] = 0
                    self.state[i][4 - j] *= 2

    def left(self):
        for i in range(4):
            for j in range(1, 4):
                if self.state[i][j] != 0 and self.state[i][j - 1] == 0:
                    self.state[i][j - 1] = self.state[i][j]
                    self.state[i][j] = 0
                elif self.state[i][j] == self.state[i][j - 1]:
                    self.state[i][j] = 0
                    self.state[i][j - 1] *= 2

    def on_key_press(self, key):
        pass

    def on_key_release(self, key):
        release_map = {
            pynput.keyboard.Key.up: self.up,
            pynput.keyboard.Key.down: self.down,
            pynput.keyboard.Key.right: self.right,
            pynput.keyboard.Key.left: self.left,
            "w": self.up,
            "s": self.down,
            "d": self.right,
            "a": self.left,
        }
        release_map[key]()
        self.new_tiles()
        self.draw()


Game()
