# Typhon

Typhon is a library (and a separate standalone VST plugin) that receives blocks of audio and midi data from
a VST plugin in realtime, processes them, and returns new audio and midi data to the VST which can output
it through a DAW like Ableton or FL Studio.

You define a callback like so:

```python
class DopeSynth:
    def __init__(self):
        # Do any setup
    def __call__(audio, midi, bpm, block_size):
        # do some processing
        return audio, midi
```

then (while the VST is running somewhere):

```python
from typhon import Typhon
t = Typhon(dope_synth)
t.connect() # Establish first-time connection to the VST
t.go() # Start streaming
```

## Limitations

* 16-bit audio only. Things were a little slow with 24-bit.
* Stereo (2 channel) audio is assumed.