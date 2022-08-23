import simpleaudio as sa
class Instrument:
    def __init__(self, path, name):
        self.name = name
        self.sound = sa.WaveObject.from_wave_file(path)

    def voice(self):
       self.sound.play()
