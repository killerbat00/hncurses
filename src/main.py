#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from config import DevConfig as config
from utils import _dircheck, _filecheck
import json
import api
import gui
import threading
import traceback
import sys
from curses import KEY_ENTER, KEY_RESIZE

class ResizeException(Exception):
    def __init__(self):
        self.message = "Please resize your terminal to have >= 80 columns and restart."

def init():
    '''
    Initialize requisite directories and files.
    '''
    _dircheck(config.FULL_DIR)
    _filecheck(config.CACHE_FILE)

def main(api,screen):
    screen.draw_splash()

    stories = api.get_frontpage()
    screen.draw_header()

    screen.write_all(stories)

    while 1:
        event = screen.content.getch()

        if event == ord('k'):
            screen.move_up(screen.content)
        if event == ord('j'):
            screen.move_down(screen.content)
        if event == ord('l'):
            screen.open_link(False)
        if event == ord('h'):
            screen.open_link(True)
        if event == ord('?'):
            screen.show_help()
        if event == KEY_ENTER:
            screen.open_item()
        if event == KEY_RESIZE:
            screen.resize()

        if event == ord('q'):
            break

if __name__=="__main__":
    init()
    hn = api.HN(config)
    screen = gui.Screen(config.APP_VERSION)

    try:
        screen.check_dimensions()
    except ResizeException as resize:
        screen.end()
        print resize.message
        sys.exit(1)

    try:
        main(hn,screen)
        screen.end()
    except (ResizeException,Exception) as err:
        screen.end()
        if type(err) == ResizeException:
            print err.message
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)
