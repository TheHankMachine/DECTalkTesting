import WavUtil
import matplotlib.pyplot as plt
from typing import List
from LocalTypes import Note
from wave import Wave_read


def plot_wav_samples_from_samples(samples: List[int], alpha=1, sample_rate=10000):
    x = [i / sample_rate for i in range(len(samples))]
    y = samples

    plt.plot(x, y, alpha=alpha)

    plt.ylabel("value")
    plt.xlabel("time")


def plot_wav_samples_from_path(filepath: str):
    plot_wav_samples_from_wav(WavUtil.get_wav_from_path(filepath))


def plot_wav_samples_from_wav(wav: Wave_read):
    plot_wav_samples_from_samples(WavUtil.get_samples_of_wav(wav))


def plot_beat_lines(notes: List[Note], color="r"):
    x = 0
    plt.axvline(x=x, color="r")
    for note in notes:
        x += note["duration"]
        plt.axvline(x=x / 1000, color="r")


def show():
    plt.show()

