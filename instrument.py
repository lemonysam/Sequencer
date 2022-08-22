from playsound import playsound

class Instrument:
    def __init__(self, path):
        self.path = path

    def voice(self):
        playsound(self.path, False)
