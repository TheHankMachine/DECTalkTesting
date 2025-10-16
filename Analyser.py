import DECTalk.DECTalk as DECTalk
import Plotter
import os
from LocalTypes import *


TEMP_PATH = os.path.join(os.path.dirname(__file__), "temp")


def analyse(notes: List[Note], quantizer: DurationQuantizer, beats:List[Note]=None) -> None:
    out_path = os.path.join(TEMP_PATH, "out.wav")
    command = "[:phoneme on][" + quantizer(notes) + "]"

    DECTalk.say_to_path(command, out_path)
    Plotter.plot_wav_samples(out_path)
    Plotter.plot_beat_lines(notes)

    Plotter.plot_beat_regions(notes if beats is None else beats)
    Plotter.show()

    #TODO: add librosa beat detection maybe

# # old beat detection code:
# def add_beat_lines(wav_filepath):
#     y, sr = librosa.load(wav_filepath)
#
#     onset_frames = librosa.onset.onset_detect(
#         y=y,
#         sr=sr,
#         # backtrack=True
#     )
#
#     for onset in onset_frames:
#         plt.axvline(x=librosa.frames_to_time(onset, sr=sr) * sr, color="r")