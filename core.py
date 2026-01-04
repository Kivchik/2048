import ctypes
from ctypes import wintypes
import os
import shutil
from time import sleep


class Window:
    def __init__(self):
        self.window_height = shutil.get_terminal_size().columns
        self.window_width = shutil.get_terminal_size().lines
        self.output = [[" " for _ in range(self.window_width+1)] for _ in range(self.window_height+1)]
        self.life_time = 0

        # self.lock_console_size()
        # self.disable_scroll()
        # self.disable_cursor()
        # self.time()

    @staticmethod
    def lock_console_size():
        # Получаем хэндл окна консоли (не буфера!)
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if not hwnd:
            return

        # Стили окна
        GWL_STYLE = -16
        WS_SIZEBOX = 0x00040000  # = WS_THICKFRAME
        WS_MAXIMIZEBOX = 0x00010000

        # Получаем текущие стили
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)

        # Убираем возможность изменения размера и максимизации
        style &= ~WS_SIZEBOX  # убираем растягивание за края
        style &= ~WS_MAXIMIZEBOX  # убираем кнопку "максимизировать"

        # Применяем новый стиль
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)

        # Обновляем окно
        ctypes.windll.user32.SetWindowPos(
            hwnd,
            0,
            0, 0, 0, 0,
            0x0001 | 0x0002 | 0x0020  # SWP_NOMOVE | SWP_NOSIZE | SWP_DRAWFRAME
        )

    @staticmethod
    def disable_scroll():
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE

        # Получаем информацию об окне консоли
        class ConsoleScreenBufferInfo(ctypes.Structure):
            _fields_ = [
                ("dwSize", wintypes._COORD),
                ("dwCursorPosition", wintypes._COORD),
                ("wAttributes", wintypes.WORD),
                ("srWindow", wintypes.SMALL_RECT),
                ("dwMaximumWindowSize", wintypes._COORD),
            ]

        info = ConsoleScreenBufferInfo()
        kernel32.GetConsoleScreenBufferInfo(handle, ctypes.byref(info))

        # srWindow — координаты видимой области:
        # left, top, right, bottom
        width = info.srWindow.Right - info.srWindow.Left + 1
        height = info.srWindow.Bottom - info.srWindow.Top + 1

        # Устанавливаем размер буфера = размеру окна
        kernel32.SetConsoleScreenBufferSize(handle, wintypes._COORD(width, height))

    @staticmethod
    def disable_cursor():
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

        # Получаем хэндл консоли
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE

        # Структура CONSOLE_CURSOR_INFO
        class ConsoleCursorInfo(ctypes.Structure):
            _fields_ = [('dwSize', wintypes.DWORD),
                        ('bVisible', wintypes.BOOL)]

        cursor_info = ConsoleCursorInfo(dwSize=1, bVisible=False)
        kernel32.SetConsoleCursorInfo(handle, ctypes.byref(cursor_info))

    @staticmethod
    def goto(position):
        print(f"\033[{position[0] + 1};{position[1] + 1}H", end="", flush=True)

    def draw_at(self, position, char):
        if position[0] in range(self.window_width) and position[1] in range (self.window_height):
            self.goto(position)
            self.output[position[0]][position[1]] = char
            print(char, end="", flush=True)

    # def draw_line(self, position1, position2, char, smoothness=4):
    #     x_len = position2[1] - position1[1]
    #     y_len = position2[0] - position1[0]
    #     x_step = 0 if x_len == 0 else 1 if y_len == 0 else (abs(x_len) / abs(y_len)) * 1 if x_len > 0 else -1
    #     y_step = 0 if y_len == 0 else 1 if x_len == 0 else (abs(y_len) / abs(x_len)) * 1 if y_len > 0 else -1
    #
    #     pos_function = lambda: [position1[0] + round(i / smoothness * y_step),
    #                             position1[1] + round(i / smoothness * x_step)]
    #     for i in range(abs((x_len if x_len > y_len else y_len) * smoothness)):
    #         self.draw_at(pos_function(), char)

    def draw_line(self, p1, p2, char):
        x0, y0 = p1[1], p1[0]  # col, row
        x1, y1 = p2[1], p2[0]

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            self.draw_at([y0, x0], char)  # [row, col]
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def draw_rectangle(self, position1, position2, char_set=('═', '║', '╔', '╗', '╚', '╝')):
        self.draw_line(position1, [position1[0], position2[1]], char_set[0])
        self.draw_line([position2[0], position1[1]], position2, char_set[0])
        self.draw_line(position1, [position2[0], position1[1]], char_set[1])
        self.draw_line([position1[0], position2[1]], position2, char_set[1])
        self.draw_at(position1, char_set[2])
        self.draw_at(position2, char_set[5])
        self.draw_at([position1[0], position2[1]], char_set[3])
        self.draw_at([position2[0], position1[1]], char_set[4])

    def redraw(self):
        os.system("cls" if os.name == "nt" else "clear")
        for line in range(len(self.output)):
            for column in range(len(self.output[line])):
                char = self.output[line][column]
                if char != " ": self.draw_at([line, column], self.output[line][column])

    # def test_lines(self):
    #     while True:
    #         for i in range(self.window_width*40):
    #             pos1 = [random.randint(0, self.window_height - 1), random.randint(0, self.window_width - 1)]
    #             pos2 = [random.randint(0, self.window_width - 1), random.randint(0, self.window_height - 1)]
    #             self.draw_line(pos1, pos2, "█")
    #         os.system("cls" if os.name == "nt" else "clear")

    def time(self, sleep_t=0.001):
        while True:
            sleep(sleep_t)
            self.life_time += sleep_t