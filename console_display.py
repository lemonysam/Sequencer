import curses
import os
from display_adaptor import DisplayAdaptor

class ConsoleDisplay(DisplayAdaptor):
    def __init__(self, tracks, length, beats_per_bar):
        super().__init__(tracks, length, beats_per_bar)

        self.screen = curses.initscr()
        os.system("stty -echo")
        curses.nocbreak()
        curses.noecho()

    def display(self, current_tick, playing):
        # this clears the screen in between drawing the sequencer to the console

        self.screen.addstr(0,0,"Playing" if playing else "Editing")
        # The display is 4 bars in a form like 
        # '|..s.|..k.|..s.|..s.|' 
        # '|    |  ^ |    |    |' 
        # where '^' is the current tick
        click_track = '     |' 
        idx = 0
        while idx < self.length:
            if idx == current_tick:
                click_track = click_track + '^'
            else:
                click_track = click_track + ' '
            if idx % self.beats_per_bar == self.beats_per_bar - 1:
                click_track = click_track + '|'
            idx += 1

        for idx, track in enumerate(self.tracks.values()):
            self.display_track(idx+1, track)
        self.screen.addstr(self.tracks.__len__() + 1, 0, click_track)
        self.screen.refresh()

    def display_track(self, output_line, track):
        output = track.instrument.name[:4].ljust(5,' ') + '|'
        for idx, beat in enumerate(track.track):
            output = output + beat
            # end of a bar
            if idx % self.beats_per_bar == self.beats_per_bar - 1:
                output = output + '|'

        self.screen.addstr(output_line, 0, output)
