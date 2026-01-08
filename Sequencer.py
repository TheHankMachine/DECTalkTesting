import Analyser
import Phonemes
import Quantizer
from CMUDict.CMUDict import CMUDict
from LocalTypes import *
from Phonemes import get_primary_phoneme

MAX_NOTE_DURATION = 20_000 # 20 seconds

VOICE_ONSET_TIME = 25 # (ms) this will probably need to be phoneme dependant
VOICE_RELEASE_TIME = 25 # (ms) also should be phoneme dependant

VOICE_ONSET_NUM_PHON_MULTIPLIER = 1.5
VOICE_RELEASE_NUM_PHON_MULTIPLIER = 1.5

DEFAULT_PHONEME = "UH"
REST_CHAR = "_"
SYLLABLE_BREAK_CHAR = "|"
SKIP_CHAR = "+"
LYRIC_SPREADABLE = [SKIP_CHAR, REST_CHAR]


class Note(TypedDict):
    pitch: int # midi pitch
    duration: float # ms
    hyphenated: bool # hyphenated to next note
    phonemic: bool # in phonemic mode
    lyric: str # lyric


def create_note(pitch: int, duration: float, hyphenated: bool, phonemic: bool, lyric: str):
    return Note(
        pitch=pitch,
        duration=duration,
        hyphenated=hyphenated,
        phonemic=phonemic,
        lyric=lyric
    )

def process(events: list[MusePlaybackEvent]) -> list[DecNote]:
    proc_events = pre_process_phonemic_events(events)

    aggregate_hyphenated_lyrics(proc_events)
    convert_to_phonemic_lyrics(proc_events)
    spread_lyrics(proc_events)

    notes = spread_phonemes(proc_events)

    # return notes
    # return Quantizer.reactive_clause_conscience_quantizer(notes)

    Analyser.analyse(notes, Quantizer.reactive_clause_conscience_quantizer, events)


def pre_process_phonemic_events(events: list[MusePlaybackEvent]) -> list[Note]:
    phonemic_mode = False
    result: list[Note] = []

    for event in events:
        if event["event_type"] == "REST":

            rest_duration = event["duration"]

            if result and result[-1]["lyric"] == REST_CHAR:
                max_comb_dur = min(MAX_NOTE_DURATION - result[-1]["duration"], rest_duration)

                result[-1]["duration"] += max_comb_dur
                rest_duration -= max_comb_dur

            if rest_duration > 0:
                # phonemic=True might be a bad idea
                result.append(create_note(0, rest_duration, False, True, REST_CHAR))

        elif event["event_type"] == "NOTE":

            if event["syllable"] and event["syllable"][0] == "[":
                phonemic_mode = True

            result.append(
                create_note(
                    event["pitch"],
                    event["duration"],
                    event["hyphenated"] and not phonemic_mode,
                    phonemic_mode,
                    SKIP_CHAR if not event["syllable"] else event["syllable"].removeprefix("[").removesuffix("]").upper()
                )
            )

            if event["syllable"] and event["syllable"][-1] == "]":
                phonemic_mode = False

    return result


def convert_to_phonemic_lyrics(notes: list[Note]) -> None:
    seen_lyric = False

    for note in notes:

        if note["lyric"] == REST_CHAR or note["lyric"] == SKIP_CHAR or note["lyric"] == SYLLABLE_BREAK_CHAR:
            if not seen_lyric:
                note["lyric"] = REST_CHAR
            continue

        seen_lyric = True

        if note["phonemic"]:
            note["lyric"] = " ".join(Phonemes.break_into_phonemes(note["lyric"]))

            if note["lyric"].strip() == "":
                note["lyric"] = DEFAULT_PHONEME
            continue

        if note["lyric"] in CMUDict:
            note["lyric"] = CMUDict[note["lyric"]]
        else:
            note["lyric"] = DEFAULT_PHONEME


def aggregate_hyphenated_lyrics(notes: list[Note]) -> None:
    i = 0
    while i < len(notes):
        if notes[i]["hyphenated"]:

            for j in range(i + 1, len(notes)):
                if notes[j]["lyric"] == REST_CHAR or notes[j]["lyric"] == SKIP_CHAR:
                    continue

                notes[i]["lyric"] += notes[j]["lyric"]
                notes[j]["lyric"] = "|"

                if not notes[j]["hyphenated"]:
                    i = j
                    break

        i += 1


def spread_lyrics(notes: list[Note]) -> None:

    for i in range(len(notes)):
        note = notes[i]
        lyric = note["lyric"]

        if lyric == REST_CHAR:
            continue

        syllables = lyric.split(" | ")

        j = 0
        while j < len(syllables):
            syllable = syllables[j]

            primary_phoneme = get_primary_phoneme(syllable)
            side_phonemes = syllable.split(primary_phoneme)

            notes[i]["lyric"] = side_phonemes[0] + primary_phoneme

            a, b = i + 1, i
            # TODO: make cleaner; this is shut
            while a < len(notes) and (
                notes[a]["lyric"] in LYRIC_SPREADABLE
                or (notes[a]["lyric"] == SYLLABLE_BREAK_CHAR and j == len(syllables) - 1)
            ):
                if notes[a]["lyric"] != REST_CHAR:
                    notes[a]["lyric"] = primary_phoneme

                    b = a

                a += 1

            notes[b]["lyric"] += side_phonemes[1]

            i = a

            if i >= len(notes) or notes[i]["lyric"] != SYLLABLE_BREAK_CHAR:
                break

            j += 1
            if j >= len(syllables):
                j = len(syllables) - 1

def dict_to_str(dict):
    if isinstance(dict, list):
        return "\n".join([dict_to_str(a) for a in dict])

    r = ""
    for key in dict.keys():
        r += f"{key[0:5]} : {dict[key]}\t"
    return r


def spread_phonemes(notes: list[Note]) -> list[DecNote]:
    result: list[DecNote] = []

    # traversing backwords through a list in python is still funky to me
    for i in range(len(notes) - 1, -1, -1):
        note = notes[i]

        if note["lyric"] == REST_CHAR:
            result.insert(0, create_decnote(0, note["duration"], REST_CHAR))
            continue

        primary_phoneme = get_primary_phoneme(note["lyric"])

        # print(note["lyric"], primary_phoneme)

        side_phonemes = note["lyric"].split(primary_phoneme)

        duration = note["duration"]

        if side_phonemes[1]:
            phonemes = side_phonemes[1][1:].split(" ")
            release_time = VOICE_RELEASE_TIME * (VOICE_RELEASE_NUM_PHON_MULTIPLIER ** (len(phonemes) - 1))

            duration -= release_time

            for phoneme in phonemes[::-1]:
                result.insert(0, create_decnote(note["pitch"], release_time / len(phonemes), phoneme))

        result.insert(0, create_decnote(note["pitch"], duration, primary_phoneme))

        if side_phonemes[0]:
            phonemes = side_phonemes[0][:-1].split(" ")

            onset_time = VOICE_ONSET_TIME * (VOICE_ONSET_NUM_PHON_MULTIPLIER ** (len(phonemes) - 1))

            if i > 0:
                notes[i - 1]["duration"] -= onset_time
            else:
                result[0]["duration"] -= onset_time

            for phoneme in phonemes[::-1]:
                result.insert(0, create_decnote(note["pitch"], onset_time / len(phonemes), phoneme))

    return result


# if __name__ == "__main__":
    # p = 25 - 12

    # process([
        # e_(-1, 700, "_"),
        # e_(p, 350, "you"),
        # e_(p, 700, "gave"),
        # e_(p, 350, "me"),
        # e_(p, 700, "some-"),
        # e_(p, 350, "thing"),
        # e_(-1, 1750, "_"),
        # e_(p + 2, 350, "I"),
        # e_(p + 2, 700, "und-"),
        # e_(p + 2, 350, "er"),
        # e_(p + 2, 1050, "stand"),
        # e_(-1, 1750, "_"),
        # e_(p, 350, "you"),
        # e_(p, 700, "gave"),
        # e_(p, 350, "me"),
        # e_(p, 700, "lov-"),
        # e_(p + 2, 350, "ing"),
        # e_(p + 5, 700, "in"),
        # e_(p + 9, 350, "the"),
        # e_(p + 7, 1050, "palm"),
        # e_(p + 7, 700, "of"),
        # e_(p + 7, 350, "my"),
        # e_(p + 7, 1050, "hand"),

        # e_(p, 1000, "fly"),
    # ])
