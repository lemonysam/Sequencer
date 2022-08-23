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

    def display(self):
        output = self.instrument.name[:4].ljust(5,' ') + '|'
        for idx, beat in enumerate(self.track):
            output = output + beat
            # end of a bar
            if idx % self.beats_per_bar == self.beats_per_bar - 1:
                output = output + '|'
        return output
