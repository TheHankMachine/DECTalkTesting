import Phonemes
import Plotter
from LocalTypes import *


def reactive_clause_conscience_quantizer(notes: List[Note]) -> str:
    # This is the approach I am currently using

    # Constants
    COMMA_INSERTION_THRESHOLD = 100
    COMMA_PAUSE_NUM_FRAMES = 2
    DUMMY_VOWEL_NUM_FRAMES = 4
    MIN_INPUT_MS = 5
    FRAME_SIZE = 64
    SAMPLE_RATE = 10_000

    def fr_to_ms(fr: int) -> float:
        return 1_000 * (fr * FRAME_SIZE) / SAMPLE_RATE

    accumulative_error: float = 0
    total_duration: float = 0
    num_phonemes_in_clause: int = 0
    out_command: str = ""

    for i in range(len(notes)):
        note = notes[i]
        extra_frames = 0
        add_comma = False
        target_ms = note["duration"]

        num_phonemes_in_clause += 1
        if note["phoneme"] in Phonemes.PLOSIVES: # account for extra dummy vowel phoneme
            num_phonemes_in_clause += 1

        if i + 1 < len(notes) and note["phoneme"] in Phonemes.PLOSIVES and notes[i + 1]["phoneme"] == "_": # account for duration added by the dummy vowel
            extra_frames += DUMMY_VOWEL_NUM_FRAMES

        if note["phoneme"] == "_" and num_phonemes_in_clause > COMMA_INSERTION_THRESHOLD: # add a comma to ensure that a dummy vowel can always be inserted
            add_comma = True
            extra_frames += COMMA_PAUSE_NUM_FRAMES
            num_phonemes_in_clause = 0

            Plotter.plot_line(total_duration) # for testing

        input_ms = int((target_ms - accumulative_error - 5 - fr_to_ms(extra_frames)))

        if input_ms < MIN_INPUT_MS:
            input_ms = MIN_INPUT_MS

        out_frames = ((input_ms + 4) * 10) // FRAME_SIZE

        if note["phoneme"] == "_":
            out_command += f"{note["phoneme"]}<{input_ms}>"
        else:
            out_command += f"{note["phoneme"]}<{input_ms},{note["pitch"]}>"

        if add_comma:
            out_command += "],["

        out_frames += extra_frames
        out_ms = fr_to_ms(out_frames)

        total_duration += out_ms

        accumulative_error += (out_ms - target_ms)

    return out_command



def naive_quantizer(notes: List[Note]) -> str:
    out = ""
    for note in notes:
        out += f"{note["phoneme"]}<{int(note["duration"])},{note["pitch"]}>"

    return out

def reactive_error_quantizer(notes: List[Note]) -> str:
    # Old approach
    acc_err = 0

    out = ""
    for note in notes:

        target_ms = note["duration"]

        input_ms = int(target_ms - acc_err)

        out_frames = ((input_ms + 4) * 10) // 64

        if note["phoneme"] == "_":
            out += f"{note["phoneme"]}<{input_ms}>"
        else:
            out += f"{note["phoneme"]}<{input_ms},{note["pitch"]}>"

        out_ms = 1_000 * (out_frames * 64) / 10_000

        acc_err += (out_ms - target_ms)

    return out

