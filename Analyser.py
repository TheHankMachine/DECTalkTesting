import DECTalk.DECTalk as DECTalk
import Plotter
from LocalTypes import *


def analyse(notes: List[Note], quantizers: DurationQuantizer | List[DurationQuantizer], beats:List[Note]=None) -> None:
    if not isinstance(quantizers, List):
        quantizers = [quantizers]

    for i, quantizer in enumerate(quantizers):
        out_path = "temp/out.wav"
        command = "[:phoneme on][" + quantizer(notes) + "]"

        DECTalk.say_to_path(command, out_path)

        Plotter.plot_wav_samples(out_path, offset=i*0.5)

    Plotter.plot_beat_lines(notes if beats is None else beats)

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