# Basic Python Drum Sequencer
This is a simple step sequencer written in Python. It is written in Python 3.

## To Run
The application runs in [Python 3](https://www.python.org/downloads/). It requires the `pynput` and `playsound` libraries. They can be installed using pip:
```
pip3 install pynput
pip3 install simpleaudio
pip3 install termios
pip3 install curses
```
To start the synthesiser run the following command:

```
python3 sequencer.py
```

## Sound files
You'll have to plumb in your own sound files and enter the Path to that file into the instrument_config file, this may be different in different OSs. You can add additional instruments this way. I got my samples from: https://www.echosoundworks.com/free-downloads

## To Use
Press the first letter of the instrument name to voice it on the current beat.

press `enter` to start and pause playback and press `escape` to quit.

You can edit in realtime by hitting keys during playback.
