import time
import random
import curses


EMOJI = '💧'


def main(std_scr):
    curses.curs_set(0)
    std_scr.nodelay(1)

    emoji_len = len(EMOJI.encode('utf-8'))

    emojis = []
    max_emojis = 50

    while True:
        std_scr.clear()

        if len(emojis) < max_emojis and random.random() < 0.5:
            y, x = 0, random.randint(0, curses.COLS - emoji_len)
            emojis.append((y, x))

        # Move and display each emoji
        for i in range(len(emojis) - 1, -1, -1):
            y, x = emojis[i]

            if 0 <= y < curses.LINES and 0 <= x < curses.COLS:
                std_scr.move(y, x)
                std_scr.addstr(EMOJI, curses.A_BOLD)

            y += 1

            if y >= curses.LINES:
                emojis.pop(i)
            else:
                emojis[i] = (y, x)

        std_scr.refresh()

        time.sleep(.05)

        key = std_scr.getch()
        if key != -1:
            break


if __name__ == '__main__':
    curses.wrapper(main)
