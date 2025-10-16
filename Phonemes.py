from typing import List


PLOSIVES     = ["P", "B", "T", "D", "K", "G"]
NASALS       = ["M", "N", "NX"]
FRICATIVES   = ["F", "V", "TH", "DH", "S", "Z", "SH", "ZH", "HX"]
AFFRICATIVES = ["CH", "JH"]
LIQUIDS      = ["L", "R"]
GLIDES       = ["W", "Y"]
SYLLABIC     = ["IY", "IH", "EY", "EH", "AE", "AA", "AY", "AW", "AH", "AO", "OW", "OY", "UH", "UW", "RR", "YU", "AX", "IX", "IR", "ER", "AR", "OR", "UR"]


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

