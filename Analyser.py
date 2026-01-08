import DECTalk.DECTalk as DECTalk
import Plotter
import os
from LocalTypes import *


TEMP_PATH = os.path.join(os.path.dirname(__file__), "temp")


def analyse(notes: List[DecNote], quantizer: DurationQuantizer, beats:List[DecNote]=None) -> None:
    out_path = os.path.join(TEMP_PATH, "out.wav")
    command = "[:phoneme on][" + quantizer(notes) + "]"

    DECTalk.say_to_path(command, out_path)
    Plotter.plot_wav_samples(out_path)
    Plotter.plot_beat_lines(notes)

    Plotter.plot_beat_regions(notes if beats is None else beats)
    Plotter.show()

def analyse_raw(input: str, beats: List[int] = []) -> None:
        out_path = os.path.join(TEMP_PATH, "out.wav")
        command = "[:phoneme on]" + input
        # command = input

        DECTalk.say_to_path(command, out_path)
        Plotter.plot_wav_samples(out_path)

        for beat in beats:
            Plotter.plot_line(beat)

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