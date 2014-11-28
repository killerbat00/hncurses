# -*- coding: utf-8 -*-

import curses
import locale
import datetime

def init_curses():
    curses.cbreak()
    curses.noecho()

def end_curses():
    curses.nocbreak()
    curses.echo()
    curses.endwin()

class Screen():
    def __init__(self):
        locale.setlocale(locale.LC_ALL, '')
        self.code = locale.getpreferredencoding()

        self.root = curses.initscr()
        self.root_maxy,self.root_maxx=self.root.getmaxyx()

        self.header = self.root.subwin(3,self.root_maxx,0,0)
        self.content = curses.newwin(100,self.root_maxx,3,0)

        self.root.keypad(1)
        self.header.keypad(1)
        self.content.keypad(1)
        self.content.scrollok(1)

        self.min_highlight = 0
        init_curses()
    
    def end(self):
        self.root.keypad(0)
        self.header.keypad(0)
        self.content.keypad(0)
        end_curses()

    def draw_header(self):
        self.header.border(0)
        startx = (self.root_maxx/2)-4
        self.header.addstr(1,startx,"HNCURSES")
        self.header.refresh()

    def highlight(self,window,y):
        window.chgat(y,4,self.root_maxx-4,curses.A_REVERSE)
        window.refresh()

    def undo_highlight(self,window,y):
        window.chgat(y,4,self.root_maxx-4,curses.A_NORMAL)
        window.refresh()

    def move_up(self,window):
        cursy,cursx = window.getyx()
        newcursy = cursy-1
        self.undo_highlight(window,cursy)
        window.move(newcursy,0)
        self.highlight(window,newcursy)

    def move_down(self,window):
        cursy,cursx = window.getyx()
        newcursy = cursy+1
        self.undo_highlight(window,cursy)
        window.move(newcursy,0)
        self.highlight(window,newcursy)
    
    def format_score(self,score):
        score_str = str(score)
        if len(score_str) == 1:
            score = "| ("+score_str+")    "
        elif len(score_str) == 2:
            score = "| ("+score_str+")   "
        elif len(score_str) == 3:
            score = "| ("+score_str+")  "
        else:
            score = "| ("+score_str+") "
        return score

    def write_story(self, window, story, index):
        titlex = int(self.root_maxx*(2.0/3.0))

        window.addstr(self.format_score(story["score"]).encode('ascii','ignore'))

        window.addnstr(story["title"].encode('ascii','ignore'),titlex)

        window.addstr(index-1,titlex," | ")
        window.addnstr(story["by"].encode('ascii','ignore'),10)
        created_at = datetime.datetime.fromtimestamp(int(story["time"]))
        delta = datetime.datetime.now() - created_at
        hours = int(delta.seconds/60/60)
        hours_ago = str(hours) + " " + " Hours Ago" if hours/10 < 1 else str(hours) + " Hours Ago"
        window.addstr(index-1,titlex+20," | " + hours_ago)
        window.refresh()

    def write_all(self, stories):
        for index,story in enumerate(stories,start=1):
            num = str(index) + " " if index/10 < 1 else str(index)
            self.content.addstr(index-1, 1, num, curses.A_BOLD)
            self.write_story(self.content,story,index)
