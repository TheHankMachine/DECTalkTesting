from typing import TypedDict, Callable, List
import random

PHONEMIC_PANGRAMS = [
    "The beige hue on the waters of the loch impressed all, including the French queen, before she heard that symphony again, just as young Arthur wanted",
    "That quick beige fox jumped in the air over each thin dog. Look out, I shout, for he's foiled you again, creating chaos",
    "The hungry purple dinosaur ate the kind, zingy fox, the jabbering crab, and the mad whale and started vending and quacking"
    "Catching weary dolphins on thin ice gives surly polar bears huge pleasure and ensures they now enjoy good meat unharmed"
]

HZ_ATTRIBUTES = ["AP", "B4", "B5", "BF", "F4", "F5", "HR", "SR"]
PERCENT_ATTRIBUTES = ["AS", "HS", "LA", "LX", "PR", "QU", "RI", "SM"]
DB_ATTRIBUTES = ["BR"]
SAMPLE_ATTRIBUTES = ["NF"]
SEX_ATTRIBUTES = ["SX"]

class Voice(TypedDict):
    AP: int # Average pitch, in Hz
    AS: int # Assertiveness, in %
    B4: int # Fourth formant bandwidth, in Hz
    B5: int # Fifth formant bandwidth, in Hz
    BF: int # Baseline fall, in Hz
    BR: int # Breathiness, in decibels (dB)
    F4: int # Fourth formant resonance frequency, in Hz
    F5: int # Fifth formant resonance frequency, in Hz
    HR: int # Hat rise, in Hz
    HS: int # Head size, in %
    LA: int # Laryngealization, in %
    LX: int # Lax breathiness, in %
    NF: int # Number of fixed samples of open glottis
    PR: int # Pitch range, in %
    QU: int # Quickness, in %
    RI: int # Richness, in %
    SM: int # Smoothness, in %
    SR: int # Stress rise, in Hz
    SX: int # Sex 1 (male) or 0 (female)

ZERO_VOICE = {
    "AP": 0,
    "AS": 0,
    "B4": 0,
    "B5": 0,
    "BF": 0,
    "BR": 0,
    "F4": 0,
    "F5": 0,
    "HR": 0,
    "HS": 0,
    "LA": 0,
    "LX": 0,
    "NF": 0,
    "PR": 0,
    "QU": 0,
    "RI": 0,
    "SM": 0,
    "SR": 0,
    "SX": 0
}

def voice_to_string(voice: Voice) -> str:
    result = "[:dv"
    for key in voice.keys():
        result += f" {key} {voice[key]}"

    result += "]"

    return result


def get_paul() -> Voice:
    return {
        "AP": 112,
        "AS": 100,
        "B4": 280,
        "B5": 330,
        "BF": 18,
        "BR": 0,
        "F4": 3300,
        "F5": 3650,
        "HR": 18,
        "HS": 100,
        "LA": 0,
        "LX": 0,
        "NF": 10,
        "PR": 100,
        "QU": 40,
        "RI": 70,
        "SM": 30,
        "SR": 25,
        "SX": 1
    }


def get_wendy() -> Voice:
    return {
        "AP": 195,
        "AS": 55,
        "B4": 300,
        "B5": 2048,
        "BF": 10,
        "BR": 45,
        "F4": 4600,
        "F5": 2500,
        "HR": 18,
        "HS": 100,
        "LA": 0,
        "LX": 80,
        "NF": 15,
        "PR": 100,
        "QU": 20,
        "RI": 70,
        "SM": 20,
        "SR": 22,
        # "SX": 0
        "SX": 0 # temporary sex change
    }


def get_perturbed_voice(voice: Voice) -> Voice:
    perturbation = voice.copy()

    for attribute in perturbation.keys():
        if attribute == "SX":
            continue

        d = int(max(abs(perturbation[attribute]) * 0.1, 20))
        perturbation[attribute] += random.randint(-d, d)

        if perturbation[attribute] < 0:
            perturbation[attribute] = 0

    return perturbation

def voice_diff(a: Voice, b: Voice) -> Voice:
    c = a.copy()

    for key in c.keys():
        c[key] -= b[key]

    return c


# print(len(get_paul()))