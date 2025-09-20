import wave
# from pydub import AudioSegment # Only works if you have ffmpeg installed
from wave import Wave_read
from typing import List


def get_wav_from_path(filepath: str) -> Wave_read:
    return wave.open(filepath, "rb")


def get_samples_of_wav(wav: Wave_read) -> List[int]:
    # I wrote this some time ago to convert the raw little-endian bytes of a wave file to a list of integer samples.
    # It's messy, unclear, and probably really slow,
    # but it works...
    # so don't touch it!
    frames = list(wav.readframes(wav.getnframes()))
    sample_width = wav.getsampwidth()

    bit_width_size = 1 << (sample_width * 8)
    sign_bit_mask = bit_width_size >> 1

    sample_groups = [frames[sample_width * i:sample_width * (i + 1)] for i in range(len(frames) // sample_width)]
    samples = []
    for group in sample_groups:
        sample = sum([v << (i * 8) for i, v in enumerate(group)])

        if sample & sign_bit_mask == sign_bit_mask:
            sample -= bit_width_size

        samples.append(sample)

    return samples


# # Only works if you have ffmpeg installed (keeping in a comment in case I really need it later)
# def overlay_wavs_from_path(filepaths: List[Wave_read], out_path: str) -> None:
#     collection = None
#     for filepath in filepaths:
#         audio_seg = AudioSegment.from_file(filepath)
#         collection = audio_seg if collection is None else collection.overlay(audio_seg)
#
#     collection.export(out_path)