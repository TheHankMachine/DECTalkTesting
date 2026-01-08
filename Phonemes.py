from typing import List

PLOSIVES     = ["P", "B", "T", "D", "K", "G"]
NASALS       = ["M", "N", "NX"]
FRICATIVES   = ["F", "V", "TH", "DH", "S", "Z", "SH", "ZH", "HX"]
AFFRICATIVES = ["CH", "JH"]
LIQUIDS      = ["L", "R"]
GLIDES       = ["W", "Y"]
SYLLABIC     = ["IY", "IH", "EY", "EH", "AE", "AA", "AY", "AW", "AH", "AO", "OW", "OY", "UH", "UW", "RR", "YU", "AX", "IX", "IR", "ER", "AR", "OR", "UR"]

PHONEMES = [
    *PLOSIVES,
    *NASALS,
    *FRICATIVES,
    *AFFRICATIVES,
    *LIQUIDS,
    *GLIDES,
    *SYLLABIC
]

PHONEMES.sort(key=len, reverse=True)

PHONEME_PRIORITY = {}
def misc_helper(ph, weight):
    for phoneme in ph:
        PHONEME_PRIORITY[phoneme] = weight

misc_helper(PLOSIVES, 0)
misc_helper(NASALS, 2)
misc_helper(FRICATIVES, 2)
misc_helper(AFFRICATIVES, 1)
misc_helper(LIQUIDS, 3)
misc_helper(GLIDES, 5)
misc_helper(SYLLABIC, 7)

def get_primary_phoneme(s: str) -> str:
    phonemes = s.split(" ")
    max = (-1, "")

    for phoneme in phonemes:
        # TODO: remove me
        if phoneme not in PHONEME_PRIORITY:
            continue

        if PHONEME_PRIORITY[phoneme] > max[0]:
            max = (PHONEME_PRIORITY[phoneme], phoneme)

    return max[1]


def break_into_phonemes(s: str) -> list[str]:
    result = []

    while len(s) > 0:
        for phoneme in PHONEMES:
            if s.startswith(phoneme):
                s = s[len(phoneme) - 1:]
                result.append(phoneme)
                break
        s = s[1:]

    return result


def proportional_distributor(total_duration: float, phonemes: List[str], syllabic_prop=0.85) -> List[float]:
    if len(phonemes) == 1:
        return [total_duration]

    return [total_duration * (syllabic_prop if phoneme in SYLLABIC else (1 - syllabic_prop) / (len(phonemes) - 1)) for phoneme in phonemes]


def fixed_plosive_proportional_distributor(total_duration: float, phonemes: List[str], plosive_duration=30, syllabic_prop=0.75) -> List[float]:
    # this is the approach I am currently using
    if len(phonemes) == 1:
        return [total_duration]

    num_plosive = sum([phoneme in PLOSIVES for phoneme in phonemes])
    plosive_time = num_plosive * plosive_duration

    total_duration -= plosive_time

    syllabic_time = total_duration if len(phonemes) - 1 - num_plosive == 0 else total_duration * syllabic_prop
    consonant_time = 0 if len(phonemes) - 1 - num_plosive == 0 else total_duration * (1 - syllabic_prop) / (len(phonemes) - 1 - num_plosive)

    return [[consonant_time, plosive_duration, syllabic_time][(phoneme in PLOSIVES) + 2 * (phoneme in SYLLABIC)] for phoneme in phonemes]

