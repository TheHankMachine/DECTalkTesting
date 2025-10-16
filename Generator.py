import Phonemes
from CMUDict.CMUDict import CMUDict
from LocalTypes import *


def generate_from_lyrics(notes: List[Note], lyrics: List[str], distributor: PhonemeDistributor) -> List[Note]:
    out = []
    i = 0

    for lyric in lyrics:
        lyric = lyric.upper()

        if lyric == "_":
            out += [Note(phoneme="_", duration=notes[i]["duration"], pitch=notes[i]["pitch"])]
            i += 1
            continue

        if lyric not in CMUDict:
            continue

        syllables = CMUDict[lyric].split(" | ")
        for syllable in syllables:
            phonemes = syllable.split(" ")
            durations = distributor(notes[i]["duration"], phonemes)

            out += [Note(duration=duration, pitch=notes[i]["pitch"], phoneme=phoneme) for duration, phoneme in zip(durations, phonemes)]
            i += 1

    return out


def generate_phoneme_pulses(pulse_lens: List[float], repeat=1, phonemes=["ah", "_"], pitches=[10]) -> List[Note]:
    return [Note(duration=pulse_lens[i % len(pulse_lens)], pitch=pitches[i % len(pitches)], phoneme=phonemes[i % len(phonemes)]) for i in range(repeat)]

