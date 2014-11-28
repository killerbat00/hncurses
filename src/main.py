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

def init():
    '''
    Initialize requisite directories and files.
    '''
    _dircheck(config.FULL_DIR)
    _filecheck(config.CACHE_FILE)

def main(api,screen):
    stories = api.get_frontpage()

    screen.draw_header()
    screen.write_all(stories)

    screen.highlight(screen.content,0)

    while 1:
        event = screen.content.getch()

        if event == ord('k'):
            screen.move_up(screen.content)
        if event == ord('j'):
            screen.move_down(screen.content)
        if event == ord('l'):
            screen.open_link()
        if event == ord('h'):
            screen.open_hn_item()
        else:
            pass

if __name__=="__main__":
    init()
    hn = api.HN(config)
    screen = gui.Screen()

    try:
        screen.check_dimensions()
    except:
        screen.end()
        print "Please resize your terminal to have > 80 columns."
        sys.exit(1)

    try:
        main(hn,screen)
        screen.end()
    except:
        screen.end()
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)
