# Erae Touch Project

## Setup

<pre>pip install -r requirements.txt</pre>

You also need to download this repository and put it in the same parent folder as this repository to compute soundwaves and losses.
<pre>https://github.com/lylyhan/wave2shape/tree/80d93a54e49ecb0855b441af15661ae091358031</pre>

## Usage
### Start experiment

To start an experiment, run the following script:

<pre>python record.py</pre>

This will automatically detect the Akai APC40 and Erae Touch MIDI devices. To have control over which MIDI device to use, please refer to l.21 and l.22 of the script.

You can now start the experiment. The target parameters are located in the `target_parameters` Python dictionnary.

For each change in one of the two controllers, the value is stored in either `messages_Akai` or `messages_Erae` Python list and the `global_parameters` Python dictionnary is updated.

When you are done with the experiment, hit **Enter**. This will save 3 JSON files: `Akai_data.json`, `target.json` and `XYat.json`. If they already exist, they will be overwritten.

<i>note: performance-wise
- you may commentate l.60 to l.63 and output the sound in parallel using a DAW for instance (you will need to create virtual devices, look at loop-MIDI and MIDI-OX)
- you may also commentate l.64 to l.67 to remove the loss computation</i>

### Visualise data
#### Visualisation of the strokes

To visualise where and how hard the player hit the virtual instrument, run the following script:

<pre>python show_Erae.py</pre>

#### Visualisation of the performance

To visualise the changes on the controller and the loss value (computed on each stroke), run the following script:

<pre>python show_Akai_loss.py</pre>

If loss values were not previously computed, it will generate `json_loss.json` and `json_time.json` files because loss computation takes time (~1.7s). You need to delete those files if loss values need to be computed again.

If you want to visualise loss values or controller values separately, run:
<pre>python show_Loss.py</pre>
or
<pre>python show_Akai.py</pre>

If you want to change the loss metric, replace the l.44 in `show_Loss.py`.
