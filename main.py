import time
from pynput import keyboard

class Sequencer:


    def __init__(self):
        self.bpm = 128
        self.beats = ['.'] * 16
        self.current_beat = 0
        # Collect events until released
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()
        self.core_loop()


    def on_press(self, key):
        try:
            self.beats[self.current_beat % 16] = key
        except AttributeError:
            print('special key pressed: {0}'.format(
                key))

    def on_release(self, key):
        return
    
    def core_loop(self):
        
        while True:
            print(self.beats[self.current_beat % 16])
            if
            self.current_beat = self.current_beat + 1
            time.sleep(60/float(self.bpm))
s = Sequencer()