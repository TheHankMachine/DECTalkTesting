import WavUtil
import matplotlib.pyplot as plt
from typing import List
from LocalTypes import Note
from wave import Wave_read


def plot_wav_samples(samples: List[int] | str | Wave_read, alpha=1, sample_rate=10000, color="tab:blue", offset=0):
    if isinstance(samples, str):
        samples = WavUtil.get_wav_from_path(samples)
    if isinstance(samples, Wave_read):
        samples = WavUtil.get_samples_of_wav(samples)

    x = [i / sample_rate for i in range(len(samples))]
    y = [sample / 2**16 + offset for sample in samples]

    plt.plot(x, y, alpha=alpha, color=color)

    plt.ylabel("value")
    plt.xlabel("time")


def plot_beat_lines(notes: List[Note]):
    colors = ["tab:blue", "tab:orange"]

    x = 0
    for i in range(len(notes)):
        plt.text((x + notes[i]["duration"] * 0.5) / 1000, 0, notes[i]["phoneme"], fontsize=5, ha='center', va='center')

        plt.axvspan(x / 1000, (x + notes[i]["duration"]) / 1000, color=colors[i % len(colors)], alpha=0.15)
        x += notes[i]["duration"]


def show():
    plt.show()

