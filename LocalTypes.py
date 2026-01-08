from typing import TypedDict, Callable, List


class DecNote(TypedDict):
    pitch: int # pitch in half steps from Ab1 (C4=28, min A1=1, max E5=47))
    duration: float # duration in milliseconds
    phoneme: str # phoneme


class MusePlaybackEvent(TypedDict):
    pitch: int # DECTalk pitch (would be midi pitch in MuseScore)
    event_type: str # "REST" or "NOTE" (is obviously an enum in MuseScore)
    duration: float # duration in milliseconds
    syllable: str # lyric associated with the playback event
    hyphenated: bool # whether the lyric is hyphenated to the next non-rest event


def create_decnote(pitch: int, duration: float, lyric: str) -> DecNote:
    return DecNote(
        pitch=pitch,
        duration=duration,
        phoneme=lyric,
    )

def create_event(pitch: int, duration: float, lyric: str) -> MusePlaybackEvent:
    event_type = "REST" if pitch <= 0 or lyric == "_" else "NOTE"
    hyphenated = lyric.endswith("-")
    lyric = lyric.replace("-", "")

    return MusePlaybackEvent(
        pitch=pitch,
        event_type=event_type,
        duration=duration,
        syllable=lyric,
        hyphenated=hyphenated
    )


type DurationQuantizer = Callable[[List[DecNote]], str]
type NoteGenerator = Callable[[], List[DecNote]]
type PhonemeDistributor = Callable[[float, List[str]], List[float]]

