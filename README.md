# Pyphonic

Pyphonic is a library (and a [separate standalone VST plugin](https://github.com/tomgrek/PyphonicCPP)) that receives blocks of audio and midi data from a VST plugin in realtime, processes them, and returns new audio and midi data to the VST which can output it through a DAW like Ableton or FL Studio.

You define a callback like so:

```python
class DopeSynth:
    def __init__(self):
        # Do any setup
    def __call__(audio, midi, bpm, chunk_size):
        # do some processing
        return audio, midi
```

then (while the VST is running somewhere):

```python
from Pyphonic import Pyphonic
p = Pyphonic(DopeSynth)
p.connect() # Establish first-time connection to the VST
p.go() # Start streaming
```

## Usage

Start your DAW and load in the plugin, or open the standalone executable plugin.

In some other Python process (e.g. a Jupyter notebook), run the snippet above. It'll just return the audio and midi data as-is.

In the snippet,

`audio`: a 1d numpy array of size 2 channels * chunk_size, `float32`. You can reshape it to `(2, chunk_size)`.

`midi_data`: a 1d numpy array of size 300. A midi message is 4 bytes so this translates to 75 messages per chunk (10ms or so). Pyphonic uses the library mido to parse these messages.

`bpm`: the BPM coming from the DAW, e.g. `128`. 

`chunk_size`: Size of a block of data sent to the callback (e.g. `512`). This can be adjusted by the user in their DAW if they're fiddling with latency.

Your callback must return a tuple of (2d numpy array of shape `(2, chunk_size)`, 1d numpy array of size 300). Each 32-bit float in the audio tuple should be between -1 and +1.

## Remote use

You can specify `host` and `port` when initializing Pyphonic. This might be useful if say you have
a laptop for music making and another computer on a home network with a GPU that you use for deep learning.

```python
p = Pyphonic(dope_synth, host="192.168.1.102", port=11586)
```

## Limitations

* 16-bit audio only. Things were a little slow with 24-bit.
* Stereo (2 channel) audio is assumed.
* The built plugin (provided [here](https://github.com/tomgrek/PyphonicCPP)) doesn't output MIDI because I noticed some DAWs had issues with plugins that output both audio and midi. You can change the settings with JUCE's ProJucer and recompile, or bug me to upload the compiled midi-outputting (or dual output) version.

## Building

From the top level dir: `python -m build`.
Then to upload to PyPI: `python -m twine upload dist/*`.