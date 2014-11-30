# -*- coding: utf-8 -*-

import curses
import datetime
import webbrowser

def init_curses():
    '''
    Executes basic curses initialization functions.
    '''
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    if curses.has_colors():
        curses.start_color()

def end_curses():
    '''
    Restores the terminal to a usable, pre-curses state.
    '''
    curses.nocbreak()
    curses.echo()
    curses.endwin()

class Screen():
    '''
    This object represents the GUI for the application.
    No API logic is called from this class, as it carries
    no reference to the api.
    It does, however, store the list of front page stories internally
    upon initially writing them out.

    The Screen is subdivided into 3 parts:
    Header
    Content
    Footer

    Currently, the Content window has no scrolling/paging capabilities.
    '''
    def __init__(self, version):
        '''
        Initializes a Screen instance. 
        In turn, creates all requisite windows and determines initial offsets for labels.

        Keyword arguments:
        version  - Current app version to use for title.
        '''
        self.title = "HNCURSES v" + version

        self.root = curses.initscr()
        self.root_maxy, self.root_maxx = self.root.getmaxyx()

        self.header = curses.newwin(2, self.root_maxx, 0, 0)
        self.headery, self.headerx = self.header.getmaxyx()

        self.content = curses.newwin(self.root_maxy - self.headery - 1, self.root_maxx, self.headery, 0)
        self.footer  = curses.newwin(1, self.root_maxx, self.root_maxy-1, 0)

        self.stories = []

        self.bottom_story = self.root_maxy - self.headery - 1

        # label offsets
        self.timex  = self.root_maxx - 16
        self.namex  = self.timex - 17
        self.scorex = self.namex - 7
        self.titlen = self.scorex - 4
        self.titlex = 6

        self.root.keypad(1)
        self.header.keypad(1)
        self.content.keypad(1)

        init_curses()

    def __del__(self):
        '''
        Clean ourselves up properly.
        '''
        self.end()

    def end(self):
        '''
        Called on the instance when the program is quitting.
        This ends all window related interactions and calls requisite
        functions to properly quit curses.
        '''
        self.root.keypad(0)
        self.header.keypad(0)
        self.content.keypad(0)
        end_curses()

    def check_dimensions(self):
        '''
        Determine if the terminal has enough characters to display satisfactorily.
        If not, raise an exception.
        '''
        if self.root_maxx < 80:
            raise Exception

    def draw_splash(self):
        '''
        Draws the splash screen.
        This screen only appears if the cache of stories has expired.
        It is not dynamic and is immediately overwritten once the stories
        have loaded and are ushered to screen.
        '''
        from utils import LETTER_Y

        midy    = int(self.root_maxy / 2)
        midx    = int(self.root_maxx / 2)
        lettery = midy - (len(LETTER_Y) / 2)
        letterx = midx - (len(LETTER_Y[0][0]) / 2)

        for index,line in enumerate(LETTER_Y,start=lettery):
            self.root.addstr(index,letterx,"".join(line))

        self.root.refresh()

    def draw_labels(self):
        '''
        Draws labels inside the header.
        '''
        self.header.addstr(1, self.titlex, "Title")
        self.header.addstr(1, self.scorex + 2, "Score")
        self.header.addstr(1, self.namex + 3, "By")
        self.header.addstr(1, self.timex + 3, "Time")

    def draw_header(self):
        '''
        Draws the headder on the top 2 lines of the screen.
        The header includes the title of the application and the column labels.
        '''
        startx = int((self.root_maxx / 2.0) - len(self.title) / 2.0) #place title directly in center

        self.header.addstr(0, startx, self.title)
        self.draw_labels()

        self.header.chgat(0, 0, self.root_maxx, curses.A_REVERSE)
        self.header.chgat(1, 0, self.root_maxx, curses.A_UNDERLINE)
        self.header.refresh()

    def draw_footer(self, story_title):
        '''
        Draws the footer on the bottom row of the screen.
        The foot shows the currently highlightd story's title as well
        as a brief help text for navigation.

        Keyword arguments:
        story_title    - Title of currently selected story.

        TODO: Add support to scroll story titles that are too wide.
        '''
        help_text = "(q): quit, (l): open link url, (h): open on HN"

        self.footer.clear()
        self.footer.addstr(story_title.encode('ascii', 'ignore'))
        self.footer.addstr(0, self.root_maxx - len(help_text) - 1, help_text)
        self.footer.chgat(0, 0, curses.A_REVERSE)
        self.footer.refresh()

    def write_all(self,stories):
        '''
        Fills up the screen with stories, calling _write_story to do the dirty work.

        If we reach the bottom of the screen, we stop writing stories.

        Keyword arguments:
        stories  - list of stories and their details

        TODO: Add the ability to start and end writing stories at specified indices.
        '''

        self.stories = stories

        for index,story in enumerate(self.stories):
            if index >= self.bottom_story:
                break
            self._write_story(self.content,index,story)

        self._highlight(self.content,0)
        self.draw_footer(self.stories[0]["title"])

    def move_up(self, window):
        '''
        Moves the cursr in window up by one line, highlighting the new line and
        unhighlighting the previously selected line.
        
        Keyword arguments:
        window   - Window in which to move cursor.

        TODO: Implement previous page mechanism to allow scrolling/paging.
        '''
        cursy,cursx = window.getyx()
        newcursy    = cursy - 1

        if newcursy < 0:
            return

        self.draw_footer(self.stories[newcursy]["title"])
        self._undo_highlight(window, cursy)
        window.move(newcursy, 0)
        self._highlight(window, newcursy)

        window.refresh()

    def move_down(self, window):
        '''
        Counterpart to move_up. Moves the cursor in window up by one line, highlighting
        and unhighlighting as necessary.

        Keyword arguments:
        window   - Window in which to move cursor.

        TODO: Implement next page mechanism to allow scrolling/paging.
        '''
        cursy,cursx = window.getyx()
        newcursy    = cursy + 1

        if newcursy >= self.bottom_story:
            self.next_page(window)
            return

        self.draw_footer(self.stories[newcursy]["title"])
        self._undo_highlight(window, cursy)
        window.move(newcursy, 0)
        self._highlight(window, newcursy)

        window.refresh()

    def previous_page(self, window):
        pass

    def next_page(self, window):
        pass

    def open_link(self,hn):
        '''
        Opens an item in the system default browser. 
        Item will open in a new tab if a browser is running, or a new window if not.

        If hn argument is present or the url is blank (Ask HN), the item will open on the HN site

        Keyword arguments:
        hn       - Determines whether to open item on HN or not.
        '''
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

    def _highlight(self, window, y):
        '''
        Highlights the entire specified line in the window. 

        Keyword arguments:
        window   - Window in which to highlight.
        y        - Line to highlight.
        '''
        window.chgat(y, 0, curses.A_REVERSE)
        window.refresh()

    def _undo_highlight(self, window, y):
        '''
        Restores the entire specified line in the window to a normal (non-highlighted) state.

        Keyword arguments:
        window   - Window in which to highlight.
        y        - Line to highlight.
        '''
        window.chgat(y, 0, curses.A_NORMAL)
        window.refresh()

    def _format_time(self, story_time):
        '''
        Formats time into that oh-so-fashionable $X hours ago format.

        Keyword arguments:
        story_time - Unix timestamp of story posting instant.

        Returns:
        String representing hours since story was posted.
        '''
        created_at = datetime.datetime.fromtimestamp(int(story_time))
        delta      = datetime.datetime.now() - created_at
        hours      = int(delta.seconds/60/60)
        hours_ago  = str(hours) + "  Hours Ago" if hours/10 < 1 else str(hours) + " Hours Ago"

        return hours_ago

    def _calculate_dimensions(self):
        '''
        Recalculates the necessarey column offsets.
        There are too many magic numbers, but oh well.
        '''
        maxx, maxy = self.root.getmaxyx()
        self.timex  = self.root_maxx - 16
        self.namex  = self.timex - 17
        self.scorex = self.namex - 7
        self.titlen = self.scorex - 4


    def _write_story(self, window, index, story):
        '''
        Auxiliary function that actually encodes and writes a story's details into a line.
        This function writes the specified story into the specified window on the
        specified line (index).

        Keyword arguments:
        window   - Window in which to write the story.
        index    - Line on which to write the story.
        story    - Story to write.
        '''
        count  = index + 1
        title  = story["title"].encode('ascii', 'ignore')

        window.addstr(index, 1, str(count))
        window.addnstr(index, self.titlex, title, self.titlen)
        window.addstr(index, self.scorex, " | " + str(story["score"]))
        window.addstr(index, self.namex, " | " + story["by"])
        window.addstr(index, self.timex, " | " + self._format_time(story["time"]))
        window.refresh()
