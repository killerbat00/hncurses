# -*- coding: utf-8 -*-

import curses
import locale
import datetime
import webbrowser

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

        self.stories = []

        self.root.keypad(1)
        self.header.keypad(1)
        self.content.keypad(1)
        self.content.scrollok(1)

        self.min_highlight = 0
        init_curses()

    def check_dimensions(self):
        if self.root_maxx < 80:
            raise Exception
    
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
        window.chgat(y,1,self.root_maxx-4,curses.A_REVERSE)
        window.refresh()

    def undo_highlight(self,window,y):
        window.chgat(y,1,self.root_maxx-4,curses.A_NORMAL)
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

    def format_story_number(self,count):
        count_str = str(count)
        if len(count_str) == 1:
            num = str(count) + "  "
        elif len(count_str) ==2:
            num = str(count) + " "
        else:
            num = str(count)
        return num.encode('ascii','ignore')
    
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
        return score.encode('ascii','ignore')

    def open_link(self):
        cursy,cursx = self.content.getyx()
        webbrowser.open_new_tab(self.stories[cursy]["url"])

    def open_hn_item(self):
        cursy,cursx = self.content.getyx()
        webbrowser.open_new_tab("https://news.ycombinator.com/item?id=" + str(self.stories[cursy]["id"]))

    def write_story(self, window, story, count):

        index = count-1
        titlex = int(self.root_maxx*(2.0/3.0))
        namex = titlex + 12

        window.addstr(index,1,self.format_story_number(count),curses.A_BOLD)

        window.addstr(self.format_score(story["score"]))


        window.addnstr(story["title"].encode('ascii','ignore'),titlex)

        window.addstr(index,titlex,"| ")
        window.addnstr(story["by"].encode('ascii','ignore'),12)

        created_at = datetime.datetime.fromtimestamp(int(story["time"]))
        delta = datetime.datetime.now() - created_at
        hours = int(delta.seconds/60/60)
        hours_ago = str(hours) + " " + " Hours Ago" if hours/10 < 1 else str(hours) + " Hours Ago"
        window.addstr(index,namex," | " + hours_ago)
        window.refresh()

    def write_all(self,stories):
        self.stories = stories
        for index,story in enumerate(self.stories,start=1):
            self.write_story(self.content,story,index)
