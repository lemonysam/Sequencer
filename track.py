class Track:
    def __init__(self, instrument, length, beats_per_bar):
        self.instrument = instrument
        self.track = ['.'] * length
        self.beats_per_bar = beats_per_bar

    def beat(self, tick):
        if self.track[tick] == '*':
            self.instrument.voice()

    def toggle_voice(self, tick):
        self.track[tick] = '*' if self.track[tick] == '.' else '.'
