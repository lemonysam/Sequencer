class DisplayAdaptor:
    def __init__(self, tracks, length, beats_per_bar):
        self.tracks = tracks
        self.length = length
        self.beats_per_bar = beats_per_bar
    
    def display_screen(self):
        raise NotImplementedError

