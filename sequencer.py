from time import sleep, time

import os
import sys

from pynput import keyboard
from threading import Thread
import curses
import termios

from instrument import Instrument
from track import Track
from instrument_config import instrument_config

clear = lambda: os.system('clear')

class Sequencer:
    # The method called when we start the sequencer, called a constructor and sets up the sequencer
    def __init__(self):
        # set some parameters
        self.bpm = 228
        self.bars = 16
        self.beats_per_bar = 4

        # sets our initial tick at the beginning
        self.current_tick = 0
        self.total_ticks = self.bars * self.beats_per_bar

        self.screen = curses.initscr()
        os.system("stty -echo")
        curses.nocbreak()
        curses.noecho()
        self.build_tracks()

        # Collect keyboard events
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

        # Start program loop
        self.core_loop()


    # This is probably the most complex bit of this so maybe ignore it for now...
    def on_press(self, key):
        try:
            if key.char in self.tracks.keys():
                self.tracks[key.char].toggle_voice(self.current_tick)

        except AttributeError:
            if key == keyboard.Key.esc:
                self.running = False
                self.playing = False
            elif key == keyboard.Key.enter:
                self.playing = not self.playing
            if self.playing == False:
                if key == keyboard.Key.right:
                    self.current_tick = (self.current_tick + 1) % self.total_ticks
                elif key == keyboard.Key.left:
                    self.current_tick = (self.current_tick - 1) % self.total_ticks

    def core_loop(self):
        try:
            self.playing = False
            self.running = True
            # self.screen.getch()

            while self.running:
                if self.playing:
                    self.play_loop()
                else:
                    self.draw()
        finally:
            termios.tcflush(sys.stdin, termios.TCIFLUSH)


    # This loops constantly whilst the program is running
    def play_loop(self):
        while self.playing:
            start_time = time()
            # Outputs a sound
            for track in self.tracks.values():
                t = Thread(target=track.beat, args=(self.current_tick,))
                t.start()
                # track.beat(self.current_tick)
            # Outputs the display
            self.draw()
            time_delta = time() - start_time
            sleep((60/float(self.bpm)) - time_delta)
            self.current_tick = 0 if self.current_tick == self.total_ticks - 1 else self.current_tick + 1

    # This draws the current state of the sequencer to the terminal
    def draw(self):
        # this clears the screen in between drawing the sequencer to the console

        self.screen.addstr(0,0,"Playing" if self.playing else "Editing")
        # The display is 4 bars in a form like 
        # '|..s.|..k.|..s.|..s.|' 
        # '|    |  ^ |    |    |' 
        # where '^' is the current tick
        click_track = '     |' 
        idx = 0
        while idx < self.total_ticks:
            if idx == self.current_tick:
                click_track = click_track + '^'
            else:
                click_track = click_track + ' '
            if idx % self.beats_per_bar == self.beats_per_bar - 1:
                click_track = click_track + '|'
            idx += 1

        for idx, track in enumerate(self.tracks.values()):
            self.screen.addstr(idx + 1, 0, track.display())
        self.screen.addstr(self.tracks.__len__() + 1, 0, click_track)

        self.screen.refresh()
        
    def build_tracks(self):
        self.tracks = {}
        for instrument in instrument_config:
            self.tracks.update({instrument["key"]: Track(
                Instrument(instrument["path"], instrument["name"]),
                self.total_ticks,
                self.beats_per_bar
            )})

# this starts the program off by initialising the sequencer
s = Sequencer()
