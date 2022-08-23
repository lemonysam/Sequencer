from time import sleep, time

import os

from pynput import keyboard

from instrument import Instrument
from track import Track
from instrument_config import instrument_config
class Sequencer:
    # The method called when we start the sequencer, called a constructor and sets up the sequencer
    def __init__(self):
        # set some parameters
        self.bpm = 228
        self.bars = 4
        self.beats_per_bar = 4

        # sets our initial tick at the beginning
        self.current_tick = 0
        self.total_ticks = self.bars * self.beats_per_bar

        self.build_tracks()

        # Collect keyboard events
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

        # Start program loop
        self.core_loop()

    # This next method is an event triggered by the keyboard listener, 
    # it sets the currently pressed key to be the value if the current beat
    # if that value is a valid tone. 
    # 
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
        self.playing = False
        self.running = True

        while self.running:
            if self.playing:
                self.play_loop()
            else:
                self.draw()


    # This loops constantly whilst the program is running
    def play_loop(self):
        while self.playing:
            start_time = time()
            # Outputs the display
            self.draw()
            # Outputs a sound
            for track in self.tracks.values():
                track.beat(self.current_tick)

            time_delta = time() - start_time
            sleep((60/float(self.bpm)) - time_delta)
            self.current_tick = 0 if self.current_tick == self.total_ticks - 1 else self.current_tick + 1

    # This draws the current state of the sequencer to the terminal
    def draw(self):
        # this clears the screen in between drawing the sequencer to the console
        clear = lambda: os.system('clear')
        clear()

        title = "Playing" if self.playing else "Editing"
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
        
        display_tracks = []
        
        for track in self.tracks.values():
            display_tracks.append(track.display())

        print(title + "\n" + '\n'.join(display_tracks) + "\n" + click_track)
    
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
