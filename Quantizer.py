from LocalTypes import *


def naive_quantizer(notes: List[Note]) -> str:
    out = ""
    for note in notes:
        out += f"{note["phoneme"]}<{int(note["duration"])},{note["pitch"]}>"

    return out


def reactive_error_quantizer(notes: List[Note]) -> str:
    # This is the approach I am currently using
    acc_err = 0

    out = ""
    for note in notes:
        target_ms = note["duration"]

        input_ms = int((target_ms - acc_err - 10))

        if note["phoneme"] == "_":
            out += f"{note["phoneme"]}<{input_ms}>"
        else:
            out += f"{note["phoneme"]}<{input_ms},{note["pitch"]}>"

        # Dear David,
        #
        # I am sorry for the magic numbers.
        # so many of these numbers are arbitrary values from the DECTalk source code that I couldn't put into
        # cohesive variable names if I cared enough to try.
        #
        # sincerely,
        #  - Hank
        out_frames = ((input_ms + 4) * 10) // 64
        out_ms = 1_000 * (out_frames * 64) / 10_000

        acc_err += (out_ms - target_ms)

    return out

