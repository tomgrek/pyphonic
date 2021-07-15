# Pyphonic

Pyphonic is a library (and a separate standalone VST plugin) that receives blocks of audio and midi data from
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
from Pyphonic import Pyphonic
p = Pyphonic(dope_synth)
p.connect() # Establish first-time connection to the VST
p.go() # Start streaming
```

## Remote use

You can specify `host` and `port` when initializing Pyphonic. This might be useful if say you have
a laptop for music making and another computer on a home network with a GPU that you use for deep learning.

```python
p = Pyphonic(dope_synth, host="192.168.1.102", port=11586)
```

## Limitations

* 16-bit audio only. Things were a little slow with 24-bit.
* Stereo (2 channel) audio is assumed.

## Building

From the top level dir: `python -m build`.
Then to upload to PyPI: `python -m twine upload dist/*`.