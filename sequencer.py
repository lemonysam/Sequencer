import time
import os

from pynput import keyboard

from instrument import Instrument
from instrument_config import instrument_config
class Sequencer:
    # The method called when we start the sequencer, called a constructor and sets up the sequencer
    def __init__(self):
        # set some parameters
        self.bpm = 128
        self.bars = 4
        self.beats_per_bar = 4

        # '.' is an empty beat, this is an array of empty beats
        self.beats = ['.'] * self.total_ticks()

        # sets our initial tick at the beginning
        self.current_tick = 0

        self.build_instruments()
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
            if key.char in self.instruments.keys() or key.char == '.':
                self.beats[self.current_tick] = key.char

        except AttributeError:
            if  key == keyboard.Key.esc:
                self.looping = False

    # This loops constantly whilst the program is running
    def core_loop(self):
        self.looping = True

        while self.looping:
            # Outputs the display
            self.draw()
            # Outputs a sound
            if self.beats[self.current_tick] != '.':
                self.instruments[self.beats[self.current_tick]].voice()

            # wait the length of a beat - not ideal since it doesn't account for execution time of the above
            # because of Python's integer maths we have to cast bpm as a float
            time.sleep(60/float(self.bpm))
            self.current_tick = 0 if self.current_tick == self.total_ticks() - 1 else self.current_tick + 1

    # This draws the current state of the sequencer to the terminal
    def draw(self):
        # this clears the screen in between drawing the sequencer to the console
        clear = lambda: os.system('clear')
        clear()

        # The display is 4 bars in a form like 
        # '|..s.|..k.|..s.|..s.|' 
        # '|    |  ^ |    |    |' 
        # where '^' is the current tick
        display_line_1 = '|' 
        display_line_2 = '|' 

        # loop over the array of beats and append the current beatto the display string
        # idx is the current kkkkss
        for idx, beat in enumerate(self.beats):
            if idx == self.current_tick:
                display_line_2 = display_line_2 + '^'
            else:
                display_line_2 = display_line_2 + ' '

            display_line_1 = display_line_1 + beat

            # end of a bar
            if idx % self.beats_per_bar == self.beats_per_bar - 1:
                display_line_1 = display_line_1 + '|'
                display_line_2 = display_line_2 + '|'
        
        print(display_line_1 + "\n" + display_line_2)
        
    
    # builds a dictionary consisting of single letter keys and Instrument values
    def build_instruments(self):
        self.instruments = {}
        for instrument in instrument_config:
            self.instruments.update({instrument["key"]: Instrument(instrument["path"])})

    # How long to loop for
    def total_ticks(self):
        return self.bars * self.beats_per_bar

# this starts the program off by initialising the sequencer
s = Sequencer()
