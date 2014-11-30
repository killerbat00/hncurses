# -*- coding: utf-8 -*-

import curses
import datetime
import webbrowser

def init_curses():
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    if curses.has_colors():
        curses.start_color()

def end_curses():
    curses.nocbreak()
    curses.echo()
    curses.endwin()

class Screen():
    def __init__(self, version):
        self.title = "HNCURSES v" + version

        self.root = curses.initscr()
        self.root_maxy, self.root_maxx = self.root.getmaxyx()

        self.header = curses.newwin(5, self.root_maxx, 0, 0)
        self.headery, self.headerx = self.header.getmaxyx()

        self.content = curses.newwin(self.root_maxy - self.headery - 1, self.root_maxx, self.headery, 0)

        self.footer = curses.newwin(1, self.root_maxx, self.root_maxy-1, 0)
    
        self.stories = []
        self.bottom_story = self.root_maxy - self.headery - 1

        self.timex  = self.root_maxx - 16
        self.namex  = self.timex - 14
        self.scorex = self.namex - 8
        self.titlen = self.scorex - 4
        self.titlex = 6

        self.root.keypad(1)
        self.header.keypad(1)
        self.content.keypad(1)
        self.content.scrollok(1)

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
        startx = int((self.root_maxx / 2.0) - len(self.title) / 2.0) #place title directly in center
        self.header.addstr(1, startx, self.title)
        self.header.hline(2, 1, "-", self.root_maxx - 2)
        self.header.refresh()
    
    def draw_footer(self):
        pass

    def draw_splash(self):
        from utils import LETTER_Y

        midy    = int(self.root_maxy / 2)
        midx    = int(self.root_maxx / 2)
        lettery = midy - (len(LETTER_Y) / 2)
        letterx = midx - (len(LETTER_Y[0][0]) / 2)

        for index,line in enumerate(LETTER_Y,start=lettery):
            self.root.addstr(index,letterx,"".join(line))

        self.root.refresh()

    def highlight(self, window,y):
        window.chgat(y, 0, curses.A_REVERSE)
        window.refresh()

    def undo_highlight(self, window,y):
        window.chgat(y, 0, curses.A_NORMAL)
        window.refresh()

    def move_up(self, window):
        cursy,cursx = window.getyx()
        newcursy    = cursy-1

        if newcursy < 0:
            return

        self.undo_highlight(window, cursy)
        window.move(newcursy,0)
        self.highlight(window, newcursy)

        window.refresh()

    def move_down(self, window):
        cursy,cursx = window.getyx()
        newcursy    = cursy+1

        if newcursy >= self.bottom_story:
            self.next_page(window)
            return

        self.undo_highlight(window, cursy)
        window.move(newcursy, 0)
        self.highlight(window, newcursy)

        window.refresh()

    def next_page(self, window):
        pass

    def _format_story_number(self, count):
        count_str = str(count)

        if len(count_str) == 1:
            num = count_str + "  "
        elif len(count_str) == 2:
            num = count_str + " "
        else:
            num = count_str

        return num.encode('ascii', 'ignore')
    
    def _format_score(self, score):
        score_str = str(score)

        if len(score_str) == 1:
            score = "| " + score_str + "    "
        elif len(score_str) == 2:
            score = "| " + score_str + "   "
        elif len(score_str) == 3:
            score = "| " + score_str + "  "
        else:
            score = "| " + score_str + " "

        return score.encode('ascii', 'ignore')

    def _format_time(self, story):
        created_at = datetime.datetime.fromtimestamp(int(story["time"]))
        delta      = datetime.datetime.now() - created_at
        hours      = int(delta.seconds/60/60)
        hours_ago  = str(hours) + "  Hours Ago" if hours/10 < 1 else str(hours) + " Hours Ago"

        return hours_ago

    def open_link(self,hn):
        cursy,cursx = self.content.getyx()

        if hn or self.stories[cursy]["url"] == "":
            url = "https://news.ycombinator.com/item?id=" + str(self.stories[cursy]["id"])
        else:
            url = self.stories[cursy]["url"]

        webbrowser.open_new_tab(url)

    def open_item(self):
        pass

    def resize(self):
        pass

    def show_help(self):
        pass

    def _draw_labels(self):
        self.header.addstr(3, self.titlex, "Title")
        self.header.addstr(3, self.scorex + 2, "Score")
        self.header.addstr(3, self.namex + 3, "By")
        self.header.addstr(3, self.timex + 3, "Time")
        self.header.refresh()

    def _calculate_dimensions(self):
        maxx, maxy = self.root.getmaxyx()
        self.timex  = self.root_maxx - 16
        self.namex  = self.timex - 14
        self.scorex = self.namex - 8
        self.titlen = self.scorex - 4


    def _write_story(self, window, index, story):

        count  = index + 1
        title  = story["title"].encode('ascii', 'ignore')

        window.addstr(index, 1, self._format_story_number(count))
        window.addnstr(index, self.titlex, title, self.titlen)
        window.addstr(index, self.scorex, self._format_score(story["score"]))
        window.addstr(index, self.namex, " | " + story["by"])
        window.addstr(index, self.timex, " | " + self._format_time(story))
        window.refresh()

    def write_all(self,stories):
        self.stories = stories

        #self._calculate_dimensions()
        self._draw_labels()

        for index,story in enumerate(self.stories):
            if index >= self.bottom_story:
                break
            self._write_story(self.content,index,story)
