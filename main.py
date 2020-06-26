import sys
import curses
from curses import wrapper

from led import led
from config import config
from define import DEFINE

#main関数
def main():
    filename = get_config_filename()
    cfg = config(filename)
    l = led(cfg.config[DEFINE.KEY_PORT], cfg.config[DEFINE.KEY_MODE])
    if l.available == True:
        wrapper(cursesmain,l )
    del l

def get_config_filename():
    arg = sys.argv
    if len(arg) < 2:
        filename = None
    else:
        filename = arg[1]
    return filename
    
#curses.wrapperに渡すメイン関数
def cursesmain(stdscr, l):
    stdscr.nodelay(True)
    while True:
        l.blink()
        c = stdscr.getch()
        if c == ord('q'):
            return
        elif c == ord('m'):
            l.change_mode()
        elif c == ord('l'):
            filename = get_config_filename()
            cfg = config(filename)
            l.set_mode(cfg.config[DEFINE.KEY_MODE])
        else:
            pass

#実行
main()
