from LocalTypes import *


def pulse_generator(pulse_len: float, repeat=1, phonemes=["ah", "_"], pitches=[10]) -> List[Note]:
    return [Note(duration=pulse_len, pitch=pitches[i % len(pitches)], phoneme=phonemes[i % len(phonemes)]) for i in range(repeat)]

